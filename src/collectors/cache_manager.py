import json
import time
import logging
from pathlib import Path
from typing import Any, Optional
from datetime import datetime

class CacheManager:
    def __init__(self, cache_config: dict):
        self.logger = logging.getLogger("portfolio.cache")
        self.enabled = cache_config['enabled']
        self.max_age = cache_config['max_age']
        self.cache_dir = Path(cache_config.get('directory', '.cache'))
        
        if self.enabled:
            self.cache_dir.mkdir(exist_ok=True)
            self.logger.info(f"Cache initialized in {self.cache_dir}")
    
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
        
    def _json_serial(obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError (f"Type {type(obj)} not serializable")


    
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
                json.dump(cache_data, f, indent=2, default=_json_serial)
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
                for cache_file in self.cache_dir.glob("*.json"):
                    cache_file.unlink()
                self.logger.info("Cleared all cache entries")
                
        except Exception as e:
            self.logger.warning(f"Error clearing cache: {e}")
    
    def cleanup(self):
        """Remove expired cache entries"""
        if not self.enabled:
            return
            
        try:
            current_time = time.time()
            for cache_file in self.cache_dir.glob("*.json"):
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
            cache_files = list(self.cache_dir.glob("*.json"))
            total_size = sum(f.stat().st_size for f in cache_files)
            current_time = time.time()
            
            expired = sum(1 for f in cache_files if current_time - json.loads(f.read_text())['timestamp'] > self.max_age)
            
            return {
                'enabled': True,
                'total_entries': len(cache_files),
                'expired_entries': expired,
                'total_size_bytes': total_size,
                'cache_dir': str(self.cache_dir)
            }
            
        except Exception as e:
            self.logger.warning(f"Error getting cache stats: {e}")
            return {'enabled': True, 'error': str(e)}