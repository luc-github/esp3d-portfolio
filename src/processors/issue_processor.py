import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional
from collections import defaultdict
from ..utils.constants import DAYS_IN_WEEK, DAYS_IN_MONTH, IssuePriority

class IssueProcessor:
    def __init__(self, config_manager):
        self.logger = logging.getLogger("portfolio.issues")
        self.config = config_manager
        
    def process_repository_issues(self, repository_data: Dict) -> Dict:
        """Process and enrich issues data for a repository"""
        enriched_data = repository_data.copy()
        
        for branch in enriched_data.get('branches', []):
            branch['issues'] = self._process_branch_issues(
                branch['issues'],
                repository_data['name'],
                branch['name']
            )
            branch['issue_summary'] = self._generate_issue_summary(branch['issues'])
            
        return enriched_data
   
    def _process_branch_issues(self, issues: List[Dict], repo_name: str, branch_name: str) -> List[Dict]:
        """Process and enrich individual issues"""
        processed_issues = []
    
        for issue in issues:
            try:
                processed_issue = self._enrich_issue_data(issue, repo_name, branch_name)
                processed_issues.append(processed_issue)
            except Exception as e:
                self.logger.error(
                    f"Error processing issue #{issue.get('number')} - {issue.get('title', 'No title')}: {e}"
                )
        
        # Définir une date par défaut pour le tri
        def get_sort_date(issue):
            updated_at = issue.get('updated_at')
            if not updated_at:
                return datetime.min
            try:
                return datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                return datetime.min

        # Sort issues by priority and update date
        return sorted(
            processed_issues,
            key=lambda x: (
                self._priority_sort_key(x.get('priority', 'low')),
                get_sort_date(x),
            ),
            reverse=True
        )

    def _enrich_issue_data(self, issue: Dict, repo_name: str, branch_name: str) -> Dict:
        """Enrich issue data with additional information"""
        enriched = issue.copy()
        
        # Calculate age and activity metrics
        created_at = datetime.fromisoformat(issue['created_at'].replace('Z', '+00:00'))
        updated_at = datetime.fromisoformat(issue['updated_at'].replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        
        age_days = (now - created_at).days
        days_since_update = (now - updated_at).days
        
        enriched.update({
            'age_days': age_days,
            'days_since_update': days_since_update,
            'is_stale': days_since_update > DAYS_IN_MONTH,
            'is_recent': days_since_update <= DAYS_IN_WEEK,
            'activity_status': self._determine_activity_status(days_since_update),
            'size_estimate': self._estimate_issue_size(issue),
            'complexity': self._estimate_complexity(issue),
            'related_issues': self._find_related_issues(issue),
            'suggested_priority': self._suggest_priority(issue, age_days, days_since_update),
            'lifecycle_stage': self._determine_lifecycle_stage(issue)
        })
        
        return enriched
    
    def _determine_activity_status(self, days_since_update: int) -> str:
        """Determine the activity status of an issue"""
        if days_since_update <= DAYS_IN_WEEK:
            return 'active'
        elif days_since_update <= DAYS_IN_MONTH:
            return 'inactive'
        else:
            return 'stale'
    
    def _estimate_issue_size(self, issue: Dict) -> str:
        """Estimate the size/effort of an issue"""
        # Assurer que body n'est jamais None
        body = (issue.get('body') or '').lower()
        labels = issue.get('labels', [])
        
        # Size estimation based on content and labels
        if any(label in labels for label in ['epic', 'large']):
            return 'large'
        elif any(label in labels for label in ['medium']):
            return 'medium'
        elif any(label in labels for label in ['small', 'trivial']):
            return 'small'
        
        # Estimate based on content length
        if len(body) > 1000:
            return 'large'
        elif len(body) > 300:
            return 'medium'
        else:
            return 'small'
    def _estimate_complexity(self, issue: Dict) -> str:
        """Estimate the complexity of an issue"""
        # Assurer que body n'est jamais None
        body = (issue.get('body') or '').lower()
        labels = issue.get('labels', [])
        
        # Complexity indicators in labels
        if any(label in labels for label in ['complex', 'hard']):
            return 'high'
        elif any(label in labels for label in ['medium']):
            return 'medium'
        elif any(label in labels for label in ['easy', 'good first issue']):
            return 'low'
        
        # Complexity indicators in content
        complexity_indicators = {
            'high': ['complex', 'difficult', 'major change', 'restructure', 'redesign'],
            'medium': ['enhance', 'improve', 'update', 'modify'],
            'low': ['fix', 'simple', 'minor', 'typo', 'documentation']
        }
        
        for level, indicators in complexity_indicators.items():
            if any(indicator in body for indicator in indicators):
                return level
        
        return 'medium'  # Default complexity
    
    def _find_related_issues(self, issue: Dict) -> List[str]:
        """Find related issues based on content analysis"""
        related = []
        body = issue.get('body') or ''  # S'assurer que body n'est jamais None
        
        # Look for issue references (#123)
        import re
        references = re.findall(r'#(\d+)', body)
        related.extend(references)
        
        # Look for "Related to" or "Depends on" statements
        related_patterns = [
            r'(?:related to|depends on|blocks|blocked by) #(\d+)',
            r'(?:fixes|resolves|closes) #(\d+)'
        ]
        
        for pattern in related_patterns:
            matches = re.findall(pattern, body, re.IGNORECASE)
            related.extend(matches)
        
        return list(set(related))  # Remove duplicates
    
    def _suggest_priority(self, issue: Dict, age_days: int, days_since_update: int) -> str:
        """Suggest priority based on various factors"""
        labels = issue.get('labels', [])
        
        # Priority from labels
        if any(label in labels for label in ['critical', 'urgent', 'priority']):
            return IssuePriority.CRITICAL.value
        elif any(label in labels for label in ['high', 'important']):
            return IssuePriority.HIGH.value
        elif any(label in labels for label in ['low', 'minor']):
            return IssuePriority.LOW.value
        
        # Priority based on age and activity
        if age_days > DAYS_IN_MONTH * 3 and days_since_update < DAYS_IN_WEEK:
            return IssuePriority.HIGH.value
        elif age_days > DAYS_IN_MONTH * 6:
            return IssuePriority.MEDIUM.value
        
        return IssuePriority.MEDIUM.value
    
    def _determine_lifecycle_stage(self, issue: Dict) -> str:
        """Determine the lifecycle stage of an issue"""
        if issue.get('state') == 'closed':
            return 'completed'
            
        labels = issue.get('labels', [])
        assignee = issue.get('assignee')
        
        if 'wontfix' in labels or 'invalid' in labels:
            return 'rejected'
        elif 'in progress' in labels or assignee:
            return 'in_progress'
        elif 'ready' in labels:
            return 'ready'
        else:
            return 'new'
    
    def _generate_issue_summary(self, issues: List[Dict]) -> Dict:
        """Generate a summary of issues for a branch"""
        summary = {
            'total': len(issues),
            'open': sum(1 for i in issues if i['state'] == 'open'),
            'closed': sum(1 for i in issues if i['state'] == 'closed'),
            'priorities': defaultdict(int),
            'ages': {
                'recent': 0,  # < 1 week
                'active': 0,  # 1 week - 1 month
                'stale': 0    # > 1 month
            },
            'complexity': defaultdict(int),
            'size': defaultdict(int),
            'lifecycle': defaultdict(int)
        }
        
        for issue in issues:
            summary['priorities'][issue['priority']] += 1
            summary['complexity'][issue['complexity']] += 1
            summary['size'][issue['size_estimate']] += 1
            summary['lifecycle'][issue['lifecycle_stage']] += 1
            
            if issue['days_since_update'] <= DAYS_IN_WEEK:
                summary['ages']['recent'] += 1
            elif issue['days_since_update'] <= DAYS_IN_MONTH:
                summary['ages']['active'] += 1
            else:
                summary['ages']['stale'] += 1
        
        return dict(summary)
    
    def _priority_sort_key(self, priority: str) -> int:
        """Get sort key for priority"""
        priority_order = {
            IssuePriority.CRITICAL.value: 0,
            IssuePriority.HIGH.value: 1,
            IssuePriority.MEDIUM.value: 2,
            IssuePriority.LOW.value: 3
        }
        return priority_order.get(priority, 999)
    
    def get_issue_trends(self, issues: List[Dict], days: int = 30) -> Dict:
        """Calculate issue trends over time"""
        now = datetime.now(timezone.utc)
        trends = {
            'creation_rate': [],  # Issues created per day
            'closure_rate': [],   # Issues closed per day
            'backlog_growth': []  # Net change in backlog per day
        }
        
        for day in range(days):
            date = now - timezone.timedelta(days=day)
            date_str = date.strftime('%Y-%m-%d')
            
            created = sum(1 for i in issues 
                         if datetime.fromisoformat(i['created_at'].replace('Z', '+00:00')).date() == date.date())
            
            closed = sum(1 for i in issues 
                        if i.get('closed_at') and 
                        datetime.fromisoformat(i['closed_at'].replace('Z', '+00:00')).date() == date.date())
            
            trends['creation_rate'].append({'date': date_str, 'count': created})
            trends['closure_rate'].append({'date': date_str, 'count': closed})
            trends['backlog_growth'].append({'date': date_str, 'count': created - closed})
        
        return trends