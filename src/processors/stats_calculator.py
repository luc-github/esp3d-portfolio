from datetime import datetime, timezone, timedelta
import logging
from typing import Dict, List, Any
from collections import defaultdict
from ..utils.constants import SECONDS_IN_DAY, DAYS_IN_WEEK, DAYS_IN_MONTH

class StatsCalculator:
    def __init__(self, config_manager):
        self.logger = logging.getLogger("portfolio.stats")
        self.config = config_manager
        
    def calculate_portfolio_stats(self, repositories_data: List[Dict]) -> Dict[str, Any]:
        """Calculate overall portfolio statistics"""
        stats = {
            'repositories': self._calculate_repository_stats(repositories_data),
            'issues': self._calculate_issue_stats(repositories_data),
            'activity': self._calculate_activity_stats(repositories_data),
            'trends': self._calculate_trend_stats(repositories_data)
        }
        
        return stats
    
    def _calculate_repository_stats(self, repositories: List[Dict]) -> Dict:
        """Calculate repository-level statistics"""
        total_repos = len(repositories)
        main_repos = sum(1 for r in repositories if r['type'] == 'main')
        
        stats = {
            'total_count': total_repos,
            'main_projects': main_repos,
            'dependencies': total_repos - main_repos,
            'languages': self._count_languages(repositories),
            'total_size': sum(r.get('statistics', {}).get('size', 0) for r in repositories),
            'total_stars': sum(r.get('statistics', {}).get('stars', 0) for r in repositories),
            'total_forks': sum(r.get('statistics', {}).get('forks', 0) for r in repositories),
            'branches': self._calculate_branch_stats(repositories)
        }
        
        return stats
    
    def _calculate_issue_stats(self, repositories: List[Dict]) -> Dict:
        """Calculate issue-related statistics"""
        all_issues = []
        for repo in repositories:
            for branch in repo.get('branches', []):
                all_issues.extend(branch.get('issues', []))
        
        now = datetime.now(timezone.utc)
        
        open_issues = [i for i in all_issues if i['state'] == 'open']
        closed_issues = [i for i in all_issues if i['state'] == 'closed']
        
        stats = {
            'total_count': len(all_issues),
            'open_count': len(open_issues),
            'closed_count': len(closed_issues),
            'close_rate': (len(closed_issues) / len(all_issues)) if all_issues else 0,
            'avg_age_days': self._calculate_average_age(open_issues),
            'avg_resolution_time': self._calculate_average_resolution_time(closed_issues),
            'priority_distribution': self._calculate_priority_distribution(all_issues),
            'recent_activity': {
                'last_day': sum(1 for i in all_issues if self._is_recently_updated(i, days=1)),
                'last_week': sum(1 for i in all_issues if self._is_recently_updated(i, days=7)),
                'last_month': sum(1 for i in all_issues if self._is_recently_updated(i, days=30))
            }
        }
        
        return stats
    
    def _calculate_activity_stats(self, repositories: List[Dict]) -> Dict:
        """Calculate activity-related statistics"""
        all_commits = []
        for repo in repositories:
            activity = repo.get('activity', {})
            all_commits.extend(activity.get('recent_commits', []))
        
        stats = {
            'total_commits': len(all_commits),
            'commit_frequency': self._calculate_commit_frequency(repositories),
            'active_contributors': self._count_active_contributors(repositories),
            'activity_heatmap': self._generate_activity_heatmap(repositories)
        }
        
        return stats
    
    def _calculate_trend_stats(self, repositories: List[Dict]) -> Dict:
        """Calculate trend statistics"""
        trends = {
            'issue_creation_trend': self._calculate_issue_creation_trend(repositories),
            'issue_resolution_trend': self._calculate_issue_resolution_trend(repositories),
            'commit_trend': self._calculate_commit_trend(repositories)
        }
        
        return trends
    
    def _calculate_average_age(self, issues: List[Dict]) -> float:
        """Calculate average age of issues in days"""
        if not issues:
            return 0
            
        now = datetime.now(timezone.utc)
        ages = []
        
        for issue in issues:
            created_at = datetime.fromisoformat(issue['created_at'].replace('Z', '+00:00'))
            age = (now - created_at).total_seconds() / SECONDS_IN_DAY
            ages.append(age)
            
        return sum(ages) / len(ages) if ages else 0
    
    def _calculate_average_resolution_time(self, closed_issues: List[Dict]) -> float:
        """Calculate average time to resolution in days"""
        if not closed_issues:
            return 0
            
        resolution_times = []
        
        for issue in closed_issues:
            if issue['closed_at'] and issue['created_at']:
                created_at = datetime.fromisoformat(issue['created_at'].replace('Z', '+00:00'))
                closed_at = datetime.fromisoformat(issue['closed_at'].replace('Z', '+00:00'))
                resolution_time = (closed_at - created_at).total_seconds() / SECONDS_IN_DAY
                resolution_times.append(resolution_time)
                
        return sum(resolution_times) / len(resolution_times) if resolution_times else 0
    
    def _count_languages(self, repositories: List[Dict]) -> Dict[str, int]:
        """Count repositories by primary language"""
        language_counts = defaultdict(int)
        for repo in repositories:
            if repo.get('language'):
                language_counts[repo['language']] += 1
        return dict(language_counts)
    
    def _calculate_branch_stats(self, repositories: List[Dict]) -> Dict:
        """Calculate branch-related statistics"""
        production_branches = 0
        development_branches = 0
        protected_branches = 0
        
        for repo in repositories:
            for branch in repo.get('branches', []):
                if branch.get('is_production'):
                    production_branches += 1
                else:
                    development_branches += 1
                if branch.get('protected'):
                    protected_branches += 1
                    
        return {
            'production': production_branches,
            'development': development_branches,
            'protected': protected_branches
        }
    
    def _calculate_priority_distribution(self, issues: List[Dict]) -> Dict[str, int]:
        """Calculate distribution of issues by priority"""
        priority_counts = defaultdict(int)
        for issue in issues:
            priority_counts[issue.get('priority', 'normal')] += 1
        return dict(priority_counts)
    
    def _is_recently_updated(self, item: Dict, days: int) -> bool:
        """Check if an item was updated within the specified number of days"""
        now = datetime.now(timezone.utc)
        updated_at = datetime.fromisoformat(item['updated_at'].replace('Z', '+00:00'))
        return (now - updated_at).total_seconds() < (days * SECONDS_IN_DAY)
    
    def _calculate_commit_frequency(self, repositories: List[Dict]) -> Dict:
        """Calculate commit frequency statistics"""
        frequencies = {
            'daily': 0,
            'weekly': 0,
            'monthly': 0
        }
        
        for repo in repositories:
            activity = repo.get('activity', {}).get('commit_activity', [])
            if activity:
                # Calculate averages from the activity data
                total_commits = sum(week.get('total', 0) for week in activity)
                weeks = len(activity)
                if weeks > 0:
                    frequencies['daily'] += total_commits / (weeks * 7)
                    frequencies['weekly'] += total_commits / weeks
                    frequencies['monthly'] += (total_commits * 4) / weeks
                    
        return frequencies
    
    def _count_active_contributors(self, repositories: List[Dict]) -> Dict[str, int]:
        """Count active contributors in different time periods"""
        active_contributors = {
            'last_week': set(),
            'last_month': set(),
            'total': set()
        }
        
        for repo in repositories:
            contributors = repo.get('contributors', [])
            for contributor in contributors:
                active_contributors['total'].add(contributor['login'])
                # Additional logic could be added here to check recent activity
                
        return {period: len(contributors) for period, contributors in active_contributors.items()}
    
    def _generate_activity_heatmap(self, repositories: List[Dict]) -> List[List[int]]:
        """Generate a weekly activity heatmap"""
        heatmap = [[0 for _ in range(24)] for _ in range(7)]  # 7 days x 24 hours
        
        for repo in repositories:
            activity = repo.get('activity', {}).get('commit_activity', [])
            for week in activity:
                for day, commits in enumerate(week.get('days', [])):
                    if commits > 0:
                        # Simplified distribution across hours
                        commits_per_hour = commits / 24
                        for hour in range(24):
                            heatmap[day][hour] += commits_per_hour
                            
        return heatmap
    
    def calculate_repository_health(self, repository: Dict) -> Dict:
        """Calculate repository health metrics"""
        health_metrics = {
            'documentation_score': self._calculate_documentation_score(repository),
            'maintenance_score': self._calculate_maintenance_score(repository),
            'activity_score': self._calculate_activity_score(repository),
            'community_score': self._calculate_community_score(repository)
        }
        
        health_metrics['overall_score'] = sum(health_metrics.values()) / len(health_metrics)
        return health_metrics
    
    def _calculate_documentation_score(self, repository: Dict) -> float:
        """Calculate documentation health score (0.0 to 1.0)"""
        score = 0.0
        max_score = 5.0  # Total number of criteria
        
        # Check for README presence and quality
        if repository.get('readme_content'):
            readme_length = len(repository['readme_content'])
            score += min(readme_length / 2000, 1.0)  # Score based on README length, max at 2000 chars
            
        # Check for Wiki
        if repository.get('has_wiki'):
            score += 1.0
            
        # Check for documentation in specific formats
        doc_patterns = ['.md', '.rst', '.txt', '.doc', 'docs/', 'documentation/']
        doc_files = sum(1 for pattern in doc_patterns if any(pattern in f for f in repository.get('files', [])))
        score += min(doc_files / 3, 1.0)  # Score based on documentation files, max at 3 files
        
        # Check for code comments (if available)
        if repository.get('code_analysis', {}).get('comment_ratio'):
            comment_ratio = repository['code_analysis']['comment_ratio']
            score += min(comment_ratio / 0.2, 1.0)  # Score based on comment ratio, max at 20%
            
        # Check for license presence
        if repository.get('license'):
            score += 1.0
            
        return score / max_score
    
    def _calculate_maintenance_score(self, repository: Dict) -> float:
        """Calculate maintenance health score (0.0 to 1.0)"""
        score = 0.0
        max_score = 5.0
        
        now = datetime.now(timezone.utc)
        
        # Recent commit activity
        try:
            # Chercher la dernière mise à jour dans les branches
            last_update = None
            for branch in repository.get('branches', []):
                branch_commit = branch.get('last_commit', {}).get('date')
                if branch_commit:
                    branch_date = datetime.fromisoformat(branch_commit.replace('Z', '+00:00'))
                    if not last_update or branch_date > last_update:
                        last_update = branch_date
            
            if last_update:
                days_since_last_commit = (now - last_update).days
                score += max(0, 1 - (days_since_last_commit / 30))  # Full score if updated within last month
            
        except Exception as e:
            self.logger.warning(f"Error calculating commit activity score: {e}")
            score += 0  # No score for this metric if there's an error
            
        # Issue response time
        if repository.get('issues'):
            try:
                avg_response_time = self._calculate_average_issue_response_time(repository['issues'])
                score += max(0, 1 - (avg_response_time / 7))  # Full score if responded within a week
            except Exception as e:
                self.logger.warning(f"Error calculating issue response time score: {e}")
                
        # Branch health
        try:
            if repository.get('branches'):
                protected_branches = sum(1 for b in repository['branches'] if b.get('protected'))
                score += min(protected_branches / 2, 1.0)  # Score for protected branches, max at 2
        except Exception as e:
            self.logger.warning(f"Error calculating branch health score: {e}")
            
        # Au moins un point minimal si le repository existe et est accessible
        score = max(score, 0.5)
            
        return score / max_score
    
    def _calculate_activity_score(self, repository: Dict) -> float:
        """Calculate activity health score (0.0 to 1.0)"""
        score = 0.0
        max_score = 5.0
        
        # Commit frequency
        if repository.get('activity', {}).get('commit_frequency'):
            weekly_commits = repository['activity']['commit_frequency']['weekly']
            score += min(weekly_commits / 10, 1.0)  # Full score for 10+ commits per week
            
        # Issue activity
        if repository.get('issues'):
            monthly_issue_activity = sum(1 for i in repository['issues'] 
                                       if self._is_recently_updated(i, 30))
            score += min(monthly_issue_activity / 10, 1.0)  # Full score for 10+ active issues
            
        # PR activity
        if repository.get('pull_requests'):
            monthly_pr_activity = sum(1 for pr in repository['pull_requests'] 
                                    if self._is_recently_updated(pr, 30))
            score += min(monthly_pr_activity / 5, 1.0)  # Full score for 5+ active PRs
            
        # Discussion activity
        if repository.get('discussions'):
            monthly_discussions = sum(1 for d in repository['discussions'] 
                                    if self._is_recently_updated(d, 30))
            score += min(monthly_discussions / 5, 1.0)  # Full score for 5+ active discussions
            
        # Contributor activity
        monthly_active_contributors = len(repository.get('activity', {}).get('active_contributors', []))
        score += min(monthly_active_contributors / 3, 1.0)  # Full score for 3+ active contributors
        
        return score / max_score
    
    def _calculate_community_score(self, repository: Dict) -> float:
        """Calculate community health score (0.0 to 1.0)"""
        score = 0.0
        max_score = 5.0
        
        # Number of contributors
        total_contributors = len(repository.get('contributors', []))
        score += min(total_contributors / 5, 1.0)  # Full score for 5+ contributors
        
        # Stars and forks
        stars = repository.get('statistics', {}).get('stars', 0)
        forks = repository.get('statistics', {}).get('forks', 0)
        score += min(stars / 100, 1.0)  # Full score for 100+ stars
        score += min(forks / 20, 1.0)   # Full score for 20+ forks
        
        # Community engagement
        if repository.get('issues'):
            issue_participants = self._count_unique_participants(repository['issues'])
            score += min(issue_participants / 10, 1.0)  # Full score for 10+ participants
            
        # Community guidelines presence
        community_files = [
            'CONTRIBUTING.md',
            'CODE_OF_CONDUCT.md',
            'SECURITY.md',
            'SUPPORT.md',
            'GOVERNANCE.md'
        ]
        
        community_docs = sum(1 for f in community_files 
                           if any(f in path for path in repository.get('files', [])))
        score += min(community_docs / len(community_files), 1.0)
        
        return score / max_score
    
    def _calculate_workflow_success_rate(self, workflows: List[Dict]) -> float:
        """Calculate the success rate of CI/CD workflows"""
        if not workflows:
            return 0.0
            
        recent_runs = [w for w in workflows if self._is_recently_updated(w, 30)]
        if not recent_runs:
            return 0.0
            
        successful_runs = sum(1 for w in recent_runs if w.get('conclusion') == 'success')
        return successful_runs / len(recent_runs)
    
    def _calculate_average_release_interval(self, releases: List[Dict]) -> float:
        """Calculate average interval between releases in days"""
        if len(releases) < 2:
            return float('inf')
            
        intervals = []
        sorted_releases = sorted(releases, key=lambda x: x['published_at'])
        
        for i in range(1, len(sorted_releases)):
            current = datetime.fromisoformat(sorted_releases[i]['published_at'].replace('Z', '+00:00'))
            previous = datetime.fromisoformat(sorted_releases[i-1]['published_at'].replace('Z', '+00:00'))
            interval = (current - previous).days
            intervals.append(interval)
            
        return sum(intervals) / len(intervals)
    
    def _count_unique_participants(self, issues: List[Dict]) -> int:
        """Count unique participants in issues"""
        participants = set()
        
        for issue in issues:
            participants.add(issue.get('user', {}).get('login'))
            for comment in issue.get('comments', []):
                participants.add(comment.get('user', {}).get('login'))
                
        participants.discard(None)
        return len(participants)
    
    def _calculate_average_issue_response_time(self, issues: List[Dict]) -> float:
        """Calculate average time to first response on issues in days"""
        response_times = []
        
        for issue in issues:
            created_at = datetime.fromisoformat(issue['created_at'].replace('Z', '+00:00'))
            
            if issue.get('comments'):
                first_comment = min(
                    (c for c in issue['comments']),
                    key=lambda x: datetime.fromisoformat(x['created_at'].replace('Z', '+00:00'))
                )
                first_response = datetime.fromisoformat(first_comment['created_at'].replace('Z', '+00:00'))
                response_time = (first_response - created_at).days
                response_times.append(response_time)
                
        return sum(response_times) / len(response_times) if response_times else float('inf')
    
    def _calculate_issue_creation_trend(self, repositories: List[Dict]) -> List[Dict]:
        """Calculate trend of issue creation over time"""
        trend_data = []
        now = datetime.now(timezone.utc)
        
        # Analyze last 12 months
        for month in range(12):
            start_date = now - timedelta(days=30 * month)
            end_date = start_date - timedelta(days=30)
            
            month_count = 0
            for repo in repositories:
                for branch in repo.get('branches', []):
                    month_count += sum(
                        1 for issue in branch.get('issues', [])
                        if end_date <= datetime.fromisoformat(issue['created_at'].replace('Z', '+00:00')) < start_date
                    )
            
            trend_data.append({
                'date': end_date.strftime('%Y-%m'),
                'count': month_count
            })
            
        return trend_data

    def _calculate_issue_resolution_trend(self, repositories: List[Dict]) -> List[Dict]:
        """Calculate trend of issue resolution over time"""
        trend_data = []
        now = datetime.now(timezone.utc)
        
        # Analyze last 12 months
        for month in range(12):
            start_date = now - timedelta(days=30 * month)
            end_date = start_date - timedelta(days=30)
            
            month_count = 0
            for repo in repositories:
                for branch in repo.get('branches', []):
                    month_count += sum(
                        1 for issue in branch.get('issues', [])
                        if issue.get('closed_at') and
                        end_date <= datetime.fromisoformat(issue['closed_at'].replace('Z', '+00:00')) < start_date
                    )
            
            trend_data.append({
                'date': end_date.strftime('%Y-%m'),
                'count': month_count
            })
            
        return trend_data

    def _calculate_commit_trend(self, repositories: List[Dict]) -> List[Dict]:
        """Calculate trend of commits over time"""
        trend_data = []
        
        for repo in repositories:
            activity = repo.get('activity', {}).get('commit_activity', [])
            for week_data in activity:
                if isinstance(week_data['week'], datetime):
                    timestamp = int(week_data['week'].timestamp())
                else:
                    timestamp = week_data['week']
                    
                trend_data.append({
                    'date': datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d'),
                    'count': week_data['total']
                })
                
        # Sort by date and combine data points for same dates
        sorted_data = {}
        for point in trend_data:
            date = point['date']
            if date in sorted_data:
                sorted_data[date]['count'] += point['count']
            else:
                sorted_data[date] = point
                
        return list(sorted_data.values())