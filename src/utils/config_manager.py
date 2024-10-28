import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
from .constants import DEFAULT_CACHE_TIMEOUT, MAX_CACHE_AGE

@dataclass
class BranchConfig:
    name: str
    label: str
    is_production: bool

@dataclass
class RepositoryConfig:
    name: str
    type: str
    priority: int
    tracked_labels: list
    ignore_labels: list
    highlight_labels: list
    branches: list[BranchConfig]

class ConfigManager:
    def __init__(self, config_path: Path):
        self.logger = logging.getLogger("portfolio.config")
        self.config_path = config_path
        self.config = self._load_config()
        self._validate_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            self.logger.info(f"Loaded configuration from {self.config_path}")
            return config
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            raise
            
    def _validate_config(self):
        """Validate configuration structure and values"""
        required_keys = ['repositories', 'options', 'display', 'cache']
        for key in required_keys:
            if key not in self.config:
                raise ValueError(f"Missing required configuration section: {key}")
                
        # Validate repositories
        for repo in self.config['repositories']:
            required_repo_keys = ['name', 'type', 'branches']
            for key in required_repo_keys:
                if key not in repo:
                    raise ValueError(f"Missing required repository key: {key} in {repo['name']}")
                    
        # Set default values if not present
        self._set_defaults()
        
    def _set_defaults(self):
        """Set default values for optional configuration parameters"""
        defaults = {
            'options': {
                'include_closed_issues': False,
                'include_pull_requests': True,
                'days_for_recent': 7,
                'cache_timeout': DEFAULT_CACHE_TIMEOUT,
                'show_contributors': True,
                'show_activity_graph': True
            },
            'display': {
                'sort_issues_by': 'updated_at',
                'group_by': ['repository', 'branch'],
                'expanded_sections': ['main_projects']
            },
            'cache': {
                'enabled': True,
                'max_age': MAX_CACHE_AGE
            }
        }
        
        for section, values in defaults.items():
            if section not in self.config:
                self.config[section] = {}
            for key, value in values.items():
                if key not in self.config[section]:
                    self.config[section][key] = value
                    
    def get_repository_config(self, repo_name: str) -> Optional[RepositoryConfig]:
        """Get configuration for a specific repository"""
        repo_data = next((r for r in self.config['repositories'] if r['name'] == repo_name), None)
        if repo_data:
            branches = [BranchConfig(**b) for b in repo_data['branches']]
            return RepositoryConfig(
                name=repo_data['name'],
                type=repo_data['type'],
                priority=repo_data.get('priority', 999),
                tracked_labels=repo_data.get('tracked_labels', []),
                ignore_labels=repo_data.get('ignore_labels', []),
                highlight_labels=repo_data.get('highlight_labels', []),
                branches=branches
            )
        return None
        
    def get_option(self, section: str, key: str, default: Any = None) -> Any:
        """Get a configuration option with default fallback"""
        return self.config.get(section, {}).get(key, default)
        
    def get_repositories(self) -> list:
        """Get list of all configured repositories"""
        return self.config['repositories']
        
    def is_cache_enabled(self) -> bool:
        """Check if caching is enabled"""
        return self.config['cache']['enabled']
        
    def get_cache_config(self) -> dict:
        """Get cache configuration"""
        return self.config['cache']