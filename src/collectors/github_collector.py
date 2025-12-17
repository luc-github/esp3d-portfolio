import logging
import os
from typing import Dict, List, Optional
from github import Github, GithubException
from datetime import datetime, timezone
from dateutil.parser import parse
from ..utils.constants import MAX_RETRIES, RETRY_DELAY, ProjectType
import time

# Default number of recent commits to collect
DEFAULT_RECENT_COMMITS = 50

class GitHubCollector:
    def __init__(self, token: str, config_manager, cache_manager):
        self.logger = logging.getLogger("portfolio.github")
        self.github = Github(token)
        self.config = config_manager
        self.cache = cache_manager
        self.username = self.github.get_user().login
        
        # Load private repos from environment variable
        self.private_repos = self._load_private_repos()
    
    def _load_private_repos(self) -> List[str]:
        """Load private repository names from environment variable"""
        private_repos_env = os.getenv('PRIVATE_REPOS', '')
        if not private_repos_env:
            return []
        
        repos = [r.strip() for r in private_repos_env.split(',') if r.strip()]
        self.logger.info(f"Loaded {len(repos)} private repositories from environment")
        return repos
    
    def collect_private_repositories_data(self) -> List[Dict]:
        """Collect data for private repositories (commits only, anonymized)"""
        private_repos_data = []
        
        private_config = self.config.get_option('private_repositories', None)
        if not private_config or not private_config.get('enabled', False):
            return []
        
        display_prefix = private_config.get('display_prefix', 'Private Project')
        
        for idx, repo_name in enumerate(self.private_repos, 1):
            try:
                cache_key = f"private_repo_{idx}"  # Anonymized cache key
                cached_data = self.cache.get(cache_key)
                if cached_data:
                    private_repos_data.append(cached_data)
                    continue
                
                self.logger.info(f"Collecting data for private repository #{idx}")
                repo = self._retry_on_failure(
                    self.github.get_repo, 
                    f"{self.username}/{repo_name}"
                )
                
                # Collect only commits (no issues, no stats, no details)
                activity_data = self._collect_private_activity_data(repo)
                
                repo_data = {
                    'name': f"{display_prefix} #{idx}",
                    'real_name': repo_name,  # Keep for internal use, never displayed
                    'type': 'private',
                    'is_private': True,
                    'description': None,  # Hidden
                    'url': None,  # Hidden
                    'language': None,  # Hidden
                    'created_at': repo.created_at.isoformat(),
                    'updated_at': repo.updated_at.isoformat(),
                    'branches': [{
                        'name': repo.default_branch,
                        'label': 'Default',
                        'is_production': True,
                        'last_commit': activity_data.get('last_commit', {}),
                        'protected': False,
                        'issues': []  # No issues for private repos
                    }],
                    'contributors': [],  # Hidden
                    'activity': activity_data,
                    'statistics': {}  # Hidden - no stars/forks/watchers
                }
                
                self.cache.set(cache_key, repo_data)
                private_repos_data.append(repo_data)
                
            except Exception as e:
                self.logger.error(f"Error collecting data for private repository #{idx}: {e}")
        
        return private_repos_data
    
    def _collect_private_activity_data(self, repo) -> Dict:
        """Collect activity data for private repo (commits only)"""
        try:
            max_commits = self.config.get_option('options', 'max_recent_commits', DEFAULT_RECENT_COMMITS)
            
            commits = self._retry_on_failure(repo.get_commits)
            
            recent_commits = []
            commits_collected = 0
            page = 0
            
            while commits_collected < max_commits:
                try:
                    page_commits = list(commits.get_page(page))
                    if not page_commits:
                        break
                    
                    remaining = max_commits - commits_collected
                    recent_commits.extend(page_commits[:remaining])
                    commits_collected += len(page_commits[:remaining])
                    
                    if len(page_commits) < 30:
                        break
                    page += 1
                except Exception as e:
                    self.logger.warning(f"Error fetching commit page {page}: {e}")
                    break
            
            # Anonymize commit data - only keep date, not author or message
            activity_data = {
                'recent_commits': [{
                    'sha': c.sha[:7],
                    'message': 'Private commit',  # Anonymized
                    'author': 'Private',  # Anonymized
                    'date': c.commit.author.date.isoformat() if c.commit.author else None
                } for c in recent_commits],
                'commit_activity': []  # Don't include detailed activity
            }
            
            # Add last commit info
            if recent_commits:
                last = recent_commits[0]
                activity_data['last_commit'] = {
                    'sha': last.sha[:7],
                    'message': 'Private commit',
                    'author': 'Private',
                    'date': last.commit.author.date.isoformat() if last.commit.author else None
                }
            
            return activity_data
            
        except Exception as e:
            self.logger.error(f"Error collecting private activity data: {e}")
            return {}
        
    def _retry_on_failure(self, func, *args, **kwargs):
        """Retry function on failure with exponential backoff"""
        for attempt in range(MAX_RETRIES):
            try:
                return func(*args, **kwargs)
            except GithubException as e:
                if e.status == 404:
                    # Add more details to the log
                    self.logger.warning(
                        f"GitHub 404 Error - Resource not found: Repository: {kwargs.get('repo', 'unknown')}, "
                        f"Branch: {kwargs.get('branch', 'unknown')}, "
                        f"Function: {func.__name__}, "
                        f"Args: {args}, "
                        f"Error: {str(e)}"
                    )
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
            
            # Get all branch configurations for this repo
            repo_config = self.config.get_repository_config(repo.name)
            all_branch_configs = repo_config.branches if repo_config else []
            
            for issue in issues:
                # Skip pull requests if not configured to include them
                if issue.pull_request and not self.config.get_option('options', 'include_pull_requests'):
                    continue
                    
                # Skip issues with ignored labels
                if any(label.name in branch_config.ignore_labels for label in issue.labels):
                    continue

                # Get issue labels
                issue_labels = [label.name for label in issue.labels]
                
                # If the current branch has an issue_label configured
                if branch_config.issue_label:
                    # Check if the issue has a version label (from any branch)
                    all_version_labels = {b.issue_label for b in all_branch_configs 
                                    if b.issue_label is not None}
                    has_version_label = any(label in all_version_labels for label in issue_labels)
                    
                    # Ignore issue if it has a different version label
                    if has_version_label and branch_config.issue_label not in issue_labels:
                        continue
                # If the branch has no issue_label configured
                else:
                    # If the issue has a version label, ignore it for this branch
                    other_branch_labels = {b.issue_label for b in all_branch_configs 
                                        if b.issue_label is not None}
                    if any(label in other_branch_labels for label in issue_labels):
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
                    'labels': issue_labels,
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
            # Get the number of commits to collect from config, default to 50
            max_commits = self.config.get_option('options', 'max_recent_commits', DEFAULT_RECENT_COMMITS)
            
            commits = self._retry_on_failure(repo.get_commits)
            
            # Collect commits across multiple pages if needed
            recent_commits = []
            commits_collected = 0
            page = 0
            
            while commits_collected < max_commits:
                try:
                    page_commits = list(commits.get_page(page))
                    if not page_commits:
                        break
                    
                    remaining = max_commits - commits_collected
                    recent_commits.extend(page_commits[:remaining])
                    commits_collected += len(page_commits[:remaining])
                    
                    if len(page_commits) < 30:  # Less than a full page means no more commits
                        break
                    page += 1
                except Exception as e:
                    self.logger.warning(f"Error fetching commit page {page}: {e}")
                    break
            
            self.logger.debug(f"Collected {len(recent_commits)} commits for {repo.name}")
            
            activity_data = {
                'recent_commits': [{
                    'sha': c.sha[:7],
                    'message': c.commit.message,
                    'author': c.commit.author.name if c.commit.author else "Unknown",
                    'date': c.commit.author.date.isoformat() if c.commit.author else None
                } for c in recent_commits],
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