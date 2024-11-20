import logging
from pathlib import Path
from rich.logging import RichHandler
from datetime import datetime

def setup_logger(config_manager, log_dir="logs"):
    """Configure logging based on configuration settings"""
    log_config = config_manager.config.get('logging', {})
    
    # Si les logs sont complètement désactivés
    if not log_config.get('enabled', True):
        logging.getLogger().setLevel(logging.ERROR)
        return logging.getLogger("portfolio")
    
    # Déterminer le niveau de log
    log_level = getattr(logging, log_config.get('level', 'INFO').upper())
    
    # Configurer les handlers
    handlers = []
    
    # Handler pour la console
    if log_config.get('console_logging', True):
        console_handler = RichHandler(rich_tracebacks=True)
        console_handler.setLevel(log_level)
        handlers.append(console_handler)
    
    # Handler pour les fichiers
    if log_config.get('file_logging', False):
        # Créer le répertoire des logs si nécessaire
        Path(log_dir).mkdir(exist_ok=True)
        
        # Nettoyer les anciens fichiers de log
        max_files = log_config.get('max_files', 7)
        cleanup_old_logs(log_dir, max_files)
        
        # Créer le nouveau fichier de log
        log_filename = f"{log_dir}/portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        handlers.append(file_handler)
    
    # Configuration de base
    logging.basicConfig(
        level=log_level,
        handlers=handlers
    )
    
    logger = logging.getLogger("portfolio")
    logger.setLevel(log_level)
    
    if not log_config.get('file_logging', False):
        logger.info("File logging is disabled")
    
    return logger

def cleanup_old_logs(log_dir: str, max_files: int):
    """Nettoyer les anciens fichiers de log"""
    log_path = Path(log_dir)
    if not log_path.exists():
        return
        
    # Liste tous les fichiers de log triés par date de modification
    log_files = sorted(
        log_path.glob("portfolio_*.log"),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )
    
    # Supprimer les fichiers excédentaires
    for old_log in log_files[max_files:]:
        try:
            old_log.unlink()
        except Exception:
            pass