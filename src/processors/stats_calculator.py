from datetime import datetime, timezone, timedelta
import logging
from typing import Dict, List, Any, Optional
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
    
    def _get_last_commit_date(self, repository: Dict) -> Optional[datetime]:
        """Get the date of the last commit from any branch"""
        last_date = None
        
        for branch in repository.get('branches', []):
            if 'last_commit' in branch:
                commit_date = branch['last_commit'].get('date')
                if commit_date:
                    # Convertir la date string en datetime
                    date = datetime.fromisoformat(commit_date.replace('Z', '+00:00'))
                    if not last_date or date > last_date:
                        last_date = date
                        
        return last_date

    def calculate_repository_health(self, repository: Dict) -> Dict:
        """Calculate repository health metrics with weighted components"""
        metrics = {
            'documentation_score': self._calculate_documentation_score(repository),
            'maintenance_score': self._calculate_maintenance_score(repository),
            'activity_score': self._calculate_activity_score(repository),
            'community_score': self._calculate_community_score(repository)
        }
        
        # Pondération différente selon l'importance relative
        weights = {
            'documentation_score': 0.3,    # 30% - Important mais pas critique
            'maintenance_score': 0.35,     # 35% - Très important
            'activity_score': 0.25,        # 25% - Important
            'community_score': 0.1         # 10% - Bonus
        }
        
        metrics['overall_score'] = sum(score * weights[key] for key, score in metrics.items())
        return metrics

    def _calculate_documentation_score(self, repository: Dict) -> float:
        """Calculate documentation health score (0.0 to 1.0)"""
        score = 0.0
        max_points = 0.0
        
        # README - 40% du score
        if repository.get('readme_content'):
            readme_length = len(repository.get('readme_content', ''))
            # Plus réaliste pour la taille du README
            score += min(readme_length / 1000, 1.0) * 0.4
            max_points += 0.4
        
        # Documentation dans le code - 30%
        doc_files = sum(1 for f in repository.get('files', []) 
                    if any(ext in f.lower() for ext in ['.md', '.rst', '.txt', 'readme', 'doc']))
        if doc_files > 0:
            score += min(doc_files / 3, 1.0) * 0.3
            max_points += 0.3
        
        # Wiki ou autres docs - 30%
        if repository.get('has_wiki') or any('docs/' in f for f in repository.get('files', [])):
            score += 0.3
            max_points += 0.3
            
        return score / max(max_points, 1.0)

    def _calculate_maintenance_score(self, repository: Dict) -> float:
        """Calculate maintenance score"""
        score = 0.0
        
        # Activité récente (50% du score)
        last_commit = self._get_last_commit_date(repository)
        if last_commit:
            days_since = (datetime.now(timezone.utc) - last_commit).days
            if days_since <= 30:  # Dernier mois
                score += 0.5
            elif days_since <= 90:  # Dernier trimestre
                score += 0.3
            elif days_since <= 180:  # Dernier semestre
                score += 0.2
        
        # Issues et PRs (30%)
        issues = repository.get('issues', [])
        if issues:
            recent_issues = sum(1 for i in issues if self._is_recently_updated(i, 90))
            score += min(recent_issues / 5, 1.0) * 0.3
        
        # Branches protégées et structure (20%)
        if repository.get('branches'):
            score += 0.2
        
        return score

    def _calculate_activity_score(self, repository: Dict) -> float:
        """Calculate activity score"""
        score = 0.0
        
        # Commits réguliers (40%)
        commit_frequency = repository.get('activity', {}).get('commit_frequency', {})
        if commit_frequency.get('monthly', 0) > 0:
            score += 0.4
        
        # Issues actives (30%)
        if repository.get('issues'):
            active_issues = sum(1 for i in repository.get('issues', [])
                            if self._is_recently_updated(i, 30))
            score += min(active_issues / 3, 1.0) * 0.3
        
        # PRs et discussions (30%)
        if repository.get('pull_requests') or repository.get('discussions'):
            score += 0.3
        
        return score

    def _calculate_community_score(self, repository: Dict) -> float:
        """Calculate community score"""
        score = 0.0
        
        # Stars et Forks (40%)
        stats = repository.get('statistics', {})
        stars = stats.get('stars', 0)
        forks = stats.get('forks', 0)
        
        score += min(stars / 20, 1.0) * 0.2  # 20 stars = max
        score += min(forks / 5, 1.0) * 0.2   # 5 forks = max
        
        # Contributeurs (40%)
        contributors = len(repository.get('contributors', []))
        score += min(contributors / 3, 1.0) * 0.4  # 3 contributeurs = max
        
        # Fichiers communautaires (20%)
        community_files = ['contributing', 'code_of_conduct', 'security']
        files = [f.lower() for f in repository.get('files', [])]
        for cf in community_files:
            if any(cf in f for f in files):
                score += 0.2 / len(community_files)
        
        return score
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
                try:
                    # Gestion des différents formats de date
                    week = week_data.get('week')
                    if isinstance(week, (int, float)):
                        timestamp = int(week)
                    elif isinstance(week, str):
                        # Conversion de la date ISO en timestamp
                        try:
                            dt = datetime.fromisoformat(week.replace('Z', '+00:00'))
                            timestamp = int(dt.timestamp())
                        except ValueError:
                            continue
                    elif isinstance(week, datetime):
                        timestamp = int(week.timestamp())
                    else:
                        continue  # Skip invalid data
                    
                    trend_data.append({
                        'date': datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d'),
                        'count': int(week_data.get('total', 0))
                    })
                except (ValueError, TypeError, AttributeError) as e:
                    self.logger.warning(f"Error processing week data: {e}")
                    continue
                
        # Sort by date and combine data points for same dates
        sorted_data = {}
        for point in trend_data:
            date = point['date']
            if date in sorted_data:
                sorted_data[date]['count'] += point['count']
            else:
                sorted_data[date] = point
                
        return list(sorted_data.values())
    
    # Dans stats_calculator.py

    def calculate_activity_kpi(self, repositories: List[Dict]) -> Dict[str, List[Dict]]:
        """Calculate activity KPIs for all repositories"""
        now = datetime.now(timezone.utc)
        activity_ranking = {
            'daily': [],
            'weekly': [],
            'monthly': []
        }
        
        for repo in repositories:
            commits = repo.get('activity', {}).get('recent_commits', [])
            issues = []
            for branch in repo.get('branches', []):
                issues.extend(branch.get('issues', []))
            
            # Calculer l'activité
            daily_activity = self._calculate_period_activity(repo, commits, issues, days=1)
            weekly_activity = self._calculate_period_activity(repo, commits, issues, days=7)
            monthly_activity = self._calculate_period_activity(repo, commits, issues, days=30)
            
            # Ajouter aux classements
            activity_ranking['daily'].append({
                'name': repo['name'],
                'type': repo['type'],
                'score': daily_activity,
                'details': {
                    'commits': daily_activity['commits'],
                    'issues': daily_activity['issues'],
                    'comments': daily_activity['comments']
                }
            })
            
            activity_ranking['weekly'].append({
                'name': repo['name'],
                'type': repo['type'],
                'score': weekly_activity,
                'details': {
                    'commits': weekly_activity['commits'],
                    'issues': weekly_activity['issues'],
                    'comments': weekly_activity['comments']
                }
            })
            
            activity_ranking['monthly'].append({
                'name': repo['name'],
                'type': repo['type'],
                'score': monthly_activity,
                'details': {
                    'commits': monthly_activity['commits'],
                    'issues': monthly_activity['issues'],
                    'comments': monthly_activity['comments']
                }
            })
        
        # Trier chaque période par score d'activité
        for period in activity_ranking:
            activity_ranking[period] = sorted(
                activity_ranking[period],
                key=lambda x: x['score']['total'],
                reverse=True
            )
        
        return activity_ranking

    def _calculate_period_activity(self, repo: Dict, commits: List[Dict], issues: List[Dict], days: int) -> Dict:
        """Calculate activity score for a specific period"""
        now = datetime.now(timezone.utc)
        start_date = now - timedelta(days=days)
        
        # Compter les commits
        commit_count = sum(1 for commit in commits 
                        if datetime.fromisoformat(commit['date'].replace('Z', '+00:00')) > start_date)
        
        # Compter les issues et commentaires
        issue_count = sum(1 for issue in issues 
                        if datetime.fromisoformat(issue['created_at'].replace('Z', '+00:00')) > start_date)
        
        # Calculer le score total
        # Les poids peuvent être ajustés selon l'importance relative
        weights = {
            'commits': 3,    # Un commit vaut 3 points
            'issues': 2,     # Une issue vaut 2 points
            'comments': 1    # Un commentaire vaut 1 point
        }
        
        activity_score = {
            'commits': commit_count,
            'issues': issue_count,
            'comments': 0,  # À implémenter si vous voulez compter les commentaires
            'total': (commit_count * weights['commits'] + 
                    issue_count * weights['issues'])
        }
        
        return activity_score