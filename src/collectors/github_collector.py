import logging
from typing import Dict, List, Optional
from github import Github, GithubException
from datetime import datetime, timezone
from dateutil.parser import parse
from ..utils.constants import MAX_RETRIES, RETRY_DELAY, ProjectType
import time

class GitHubCollector:
    def __init__(self, token: str, config_manager, cache_manager):
        self.logger = logging.getLogger("portfolio.github")
        self.github = Github(token)
        self.config = config_manager
        self.cache = cache_manager
        
    def _retry_on_failure(self, func, *args, **kwargs):
        """Retry function on failure with exponential backoff"""
        for attempt in range(MAX_RETRIES):
            try:
                return func(*args, **kwargs)
            except GithubException as e:
                if e.status == 403:  # Rate limit exceeded
                    reset_time = int(self.github.rate_limiting_resettime)
                    wait_time = reset_time - time.time()
                    if wait_time > 0:
                        self.logger.warning(f"Rate limit exceeded. Waiting {wait_time:.0f} seconds...")
                        time.sleep(wait_time + 1)
                        continue
                if attempt < MAX_RETRIES - 1:
                    wait_time = RETRY_DELAY * (2 ** attempt)
                    self.logger.warning(f"GitHub API error: {e}. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise
                    
    def collect_repository_data(self, repo_name: str) -> Dict:
        """Collect all data for a repository"""
        cache_key = f"repo_{repo_name}"
        cached_data = self.cache.get(cache_key)
        if cached_data:
            return cached_data
            
        self.logger.info(f"Collecting data for repository: {repo_name}")
        repo_config = self.config.get_repository_config(repo_name)
        if not repo_config:
            raise ValueError(f"No configuration found for repository: {repo_name}")
            
        try:
            repo = self._retry_on_failure(self.github.get_repo, f"{self.github.get_user().login}/{repo_name}")
            
            repo_data = {
                'name': repo.name,
                'type': repo_config.type,
                'description': repo.description,
                'url': repo.html_url,
                'language': repo.language,
                'created_at': repo.created_at.isoformat(),
                'updated_at': repo.updated_at.isoformat(),
                'branches': self._collect_branches_data(repo, repo_config),
                'contributors': self._collect_contributors_data(repo),
                'activity': self._collect_activity_data(repo),
                'statistics': self._collect_repository_statistics(repo)
            }
            
            self.cache.set(cache_key, repo_data)
            return repo_data
            
        except Exception as e:
            self.logger.error(f"Error collecting data for {repo_name}: {e}")
            raise
            
    def _collect_branches_data(self, repo, repo_config) -> List[Dict]:
        """Collect data for configured branches"""
        branches_data = []
        
        for branch_config in repo_config.branches:
            try:
                branch = self._retry_on_failure(repo.get_branch, branch_config.name)
                last_commit = branch.commit.commit
                
                branch_data = {
                    'name': branch_config.name,
                    'label': branch_config.label,
                    'is_production': branch_config.is_production,
                    'last_commit': {
                        'sha': branch.commit.sha[:7],
                        'message': last_commit.message,
                        'author': last_commit.author.name if last_commit.author else "Unknown",
                        'date': last_commit.author.date.isoformat() if last_commit.author else None
                    },
                    'protected': branch.protected,
                    'issues': self._collect_branch_issues(repo, branch_config)
                }
                
                branches_data.append(branch_data)
                
            except Exception as e:
                self.logger.error(f"Error collecting data for branch {branch_config.name}: {e}")
                
        return branches_data
        
    def _collect_branch_issues(self, repo, branch_config) -> List[Dict]:
        """Collect issues for a specific branch"""
        issues_data = []
        
        # Determine issue state based on configuration
        state = "all" if self.config.get_option('options', 'include_closed_issues') else "open"
        
        try:
            issues = self._retry_on_failure(repo.get_issues, state=state)
            
            for issue in issues:
                # Skip pull requests if not configured to include them
                if issue.pull_request and not self.config.get_option('options', 'include_pull_requests'):
                    continue
                    
                # Skip issues with ignored labels
                if any(label.name in branch_config.ignore_labels for label in issue.labels):
                    continue
                    
                issue_data = {
                    'number': issue.number,
                    'title': issue.title,
                    'body': issue.body,
                    'state': issue.state,
                    'created_at': issue.created_at.isoformat(),
                    'updated_at': issue.updated_at.isoformat(),
                    'closed_at': issue.closed_at.isoformat() if issue.closed_at else None,
                    'url': issue.html_url,
                    'is_pr': bool(issue.pull_request),
                    'labels': [label.name for label in issue.labels],
                    'priority': self._determine_issue_priority(issue, branch_config),
                    'assignee': issue.assignee.login if issue.assignee else None
                }
                
                issues_data.append(issue_data)
                
        except Exception as e:
            self.logger.error(f"Error collecting issues: {e}")
            
        return issues_data
        
    def _collect_contributors_data(self, repo) -> List[Dict]:
        """Collect contributor statistics"""
        if not self.config.get_option('options', 'show_contributors'):
            return []
            
        try:
            contributors = self._retry_on_failure(repo.get_contributors)
            return [{
                'login': c.login,
                'contributions': c.contributions,
                'url': c.html_url
            } for c in contributors]
        except Exception as e:
            self.logger.error(f"Error collecting contributors data: {e}")
            return []
            
    def _collect_activity_data(self, repo) -> Dict:
        """Collect repository activity data"""
        try:
            commits = self._retry_on_failure(repo.get_commits)
            recent_commits = list(commits.get_page(0))
            
            activity_data = {
                'recent_commits': [{
                    'sha': c.sha[:7],
                    'message': c.commit.message,
                    'author': c.commit.author.name if c.commit.author else "Unknown",
                    'date': c.commit.author.date.isoformat() if c.commit.author else None
                } for c in recent_commits[:10]],
                'commit_activity': self._get_commit_activity(repo)
            }
            
            return activity_data
            
        except Exception as e:
            self.logger.error(f"Error collecting activity data: {e}")
            return {}
            
    def _collect_repository_statistics(self, repo) -> Dict:
        """Collect repository statistics"""
        try:
            stats = {
                'size': repo.size,
                'stars': repo.stargazers_count,
                'forks': repo.forks_count,
                'open_issues': repo.open_issues_count,
                'watchers': repo.watchers_count,
                'default_branch': repo.default_branch
            }
            
            if repo.license:
                stats['license'] = repo.license.name
                
            return stats
            
        except Exception as e:
            self.logger.error(f"Error collecting repository statistics: {e}")
            return {}
            
    def _determine_issue_priority(self, issue, branch_config) -> str:
        """Determine issue priority based on labels"""
        if any(label.name in branch_config.highlight_labels for label in issue.labels):
            return "high"
        return "normal"
        
    def _get_commit_activity(self, repo) -> List[Dict]:
        """Get commit activity for the past year"""
        try:
            stats = self._retry_on_failure(repo.get_stats_commit_activity)
            if not stats:
                return []
                
            return [{
                'week': s.week,
                'total': s.total,
                'days': s.days
            } for s in stats]
            
        except Exception as e:
            self.logger.error(f"Error collecting commit activity: {e}")
            return []
            
    def get_rate_limit_info(self) -> Dict:
        """Get GitHub API rate limit information"""
        try:
            limits = self.github.get_rate_limit()
            return {
                'core': {
                    'limit': limits.core.limit,
                    'remaining': limits.core.remaining,
                    'reset': limits.core.reset.isoformat()
                },
                'search': {
                    'limit': limits.search.limit,
                    'remaining': limits.search.remaining,
                    'reset': limits.search.reset.isoformat()
                }
            }
        except Exception as e:
            self.logger.error(f"Error getting rate limit info: {e}")
            return {}