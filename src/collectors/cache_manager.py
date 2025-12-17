import json
import time
import logging
import hashlib
from pathlib import Path
from typing import Any, Optional, Dict
from datetime import datetime

# Keys in config that affect cached data (changes require cache invalidation)
CONFIG_KEYS_AFFECTING_CACHE = [
    'repositories',           # Repo list, branches, labels
    'options.max_recent_commits',
    'options.include_closed_issues',
    'options.include_pull_requests',
    'private_repositories.enabled',
]

class CacheManager:
    def __init__(self, cache_config: dict, full_config: dict = None):
        """Initialize cache manager.
        
        Args:
            cache_config: Cache-specific configuration (enabled, max_age, directory)
            full_config: Full application config for change detection (optional)
        """
        self.logger = logging.getLogger("portfolio.cache")
        self.enabled = cache_config['enabled']
        self.max_age = cache_config['max_age']
        self.cache_dir = Path(cache_config.get('directory', '.cache'))
        self.config_hash_file = self.cache_dir / '_config_hash.json'
        
        if self.enabled:
            self.cache_dir.mkdir(exist_ok=True)
            self.logger.info(f"Cache initialized in {self.cache_dir}")
            
            # Check for config changes if full_config provided
            if full_config:
                self._check_config_changes(full_config)
    
    def _compute_config_hash(self, config: dict) -> str:
        """Compute a hash of config sections that affect cached data."""
        # Extract only the relevant parts of config
        relevant_config = {}
        
        # Always include repositories (most important)
        relevant_config['repositories'] = config.get('repositories', [])
        
        # Include specific options that affect data collection
        options = config.get('options', {})
        relevant_config['options'] = {
            'max_recent_commits': options.get('max_recent_commits'),
            'include_closed_issues': options.get('include_closed_issues'),
            'include_pull_requests': options.get('include_pull_requests'),
        }
        
        # Include private repositories config
        private_config = config.get('private_repositories', {})
        relevant_config['private_repositories'] = {
            'enabled': private_config.get('enabled'),
        }
        
        # Create a stable JSON string and hash it
        config_str = json.dumps(relevant_config, sort_keys=True, default=str)
        return hashlib.sha256(config_str.encode()).hexdigest()[:16]
    
    def _check_config_changes(self, config: dict):
        """Check if config has changed and invalidate cache if needed."""
        current_hash = self._compute_config_hash(config)
        
        try:
            if self.config_hash_file.exists():
                with self.config_hash_file.open('r', encoding='utf-8') as f:
                    saved_data = json.load(f)
                    saved_hash = saved_data.get('hash', '')
                    saved_time = saved_data.get('timestamp', 0)
                    
                if saved_hash != current_hash:
                    self.logger.warning("=" * 60)
                    self.logger.warning("CONFIG CHANGE DETECTED - Invalidating cache automatically")
                    self.logger.warning(f"  Previous hash: {saved_hash}")
                    self.logger.warning(f"  Current hash:  {current_hash}")
                    self.logger.warning("=" * 60)
                    
                    # Clear all cache entries
                    self.clear()
                    
                    # Save new hash
                    self._save_config_hash(current_hash)
                else:
                    self.logger.debug(f"Config unchanged (hash: {current_hash})")
            else:
                # First run or hash file deleted - save current hash
                self.logger.info(f"Initializing config hash: {current_hash}")
                self._save_config_hash(current_hash)
                
        except Exception as e:
            self.logger.warning(f"Error checking config changes: {e}")
            # Save current hash to avoid repeated errors
            self._save_config_hash(current_hash)
    
    def _save_config_hash(self, config_hash: str):
        """Save config hash to file."""
        try:
            with self.config_hash_file.open('w', encoding='utf-8') as f:
                json.dump({
                    'hash': config_hash,
                    'timestamp': time.time(),
                    'readable_time': datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            self.logger.warning(f"Error saving config hash: {e}")
    
    def _get_cache_path(self, key: str) -> Path:
        """Get the file path for a cache key"""
        return self.cache_dir / f"{key}.json"
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if not self.enabled:
            return None
            
        cache_path = self._get_cache_path(key)
        if not cache_path.exists():
            return None
            
        try:
            with cache_path.open('r', encoding='utf-8') as f:
                cached_data = json.load(f)
                
            # Check if cache is expired
            if time.time() - cached_data['timestamp'] > self.max_age:
                self.logger.debug(f"Cache expired for {key}")
                return None
                
            self.logger.debug(f"Cache hit for {key}")
            return cached_data['data']
            
        except Exception as e:
            self.logger.warning(f"Error reading cache for {key}: {e}")
            return None
        
    def _json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")

    def set(self, key: str, data: Any):
        """Store value in cache with timestamp"""
        if not self.enabled:
            return
            
        try:
            cache_data = {
                'timestamp': time.time(),
                'data': data
            }
            
            cache_path = self._get_cache_path(key)
            with cache_path.open('w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, default=self._json_serial)
            self.logger.debug(f"Cached data for {key}")
            
        except Exception as e:
            self.logger.warning(f"Error writing cache for {key}: {e}")

    def clear(self, key: Optional[str] = None):
        """Clear specific or all cache entries"""
        if not self.enabled:
            return
            
        try:
            if key:
                cache_path = self._get_cache_path(key)
                if cache_path.exists():
                    cache_path.unlink()
                    self.logger.debug(f"Cleared cache for {key}")
            else:
                # Clear all cache files except config hash
                cleared_count = 0
                for cache_file in self.cache_dir.glob("*.json"):
                    if cache_file.name != '_config_hash.json':
                        cache_file.unlink()
                        cleared_count += 1
                self.logger.info(f"Cleared {cleared_count} cache entries")
                
        except Exception as e:
            self.logger.warning(f"Error clearing cache: {e}")
    
    def cleanup(self):
        """Remove expired cache entries"""
        if not self.enabled:
            return
            
        try:
            current_time = time.time()
            for cache_file in self.cache_dir.glob("*.json"):
                # Skip config hash file
                if cache_file.name == '_config_hash.json':
                    continue
                    
                try:
                    with cache_file.open('r', encoding='utf-8') as f:
                        cached_data = json.load(f)
                    
                    if current_time - cached_data['timestamp'] > self.max_age:
                        cache_file.unlink()
                        self.logger.debug(f"Removed expired cache file: {cache_file}")
                        
                except Exception as e:
                    self.logger.warning(f"Error processing cache file {cache_file}: {e}")
                    
            self.logger.info("Cache cleanup completed")
            
        except Exception as e:
            self.logger.warning(f"Error during cache cleanup: {e}")
    
    def get_cache_stats(self) -> dict:
        """Get cache statistics"""
        if not self.enabled:
            return {'enabled': False}
            
        try:
            cache_files = [f for f in self.cache_dir.glob("*.json") if f.name != '_config_hash.json']
            total_size = sum(f.stat().st_size for f in cache_files)
            current_time = time.time()
            
            expired = 0
            for f in cache_files:
                try:
                    data = json.loads(f.read_text())
                    if current_time - data['timestamp'] > self.max_age:
                        expired += 1
                except:
                    pass
            
            # Get config hash info
            config_hash_info = None
            if self.config_hash_file.exists():
                try:
                    with self.config_hash_file.open('r') as f:
                        config_hash_info = json.load(f)
                except:
                    pass
            
            return {
                'enabled': True,
                'total_entries': len(cache_files),
                'expired_entries': expired,
                'total_size_bytes': total_size,
                'cache_dir': str(self.cache_dir),
                'config_hash': config_hash_info.get('hash') if config_hash_info else None,
                'config_hash_time': config_hash_info.get('readable_time') if config_hash_info else None
            }
            
        except Exception as e:
            self.logger.warning(f"Error getting cache stats: {e}")
            return {'enabled': True, 'error': str(e)}