import logging
from pathlib import Path
from rich.logging import RichHandler
from datetime import datetime

def setup_logger(log_dir="logs"):
    # Create logs directory if it doesn't exist
    Path(log_dir).mkdir(exist_ok=True)
    
    # Configure logging
    log_filename = f"{log_dir}/portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    # Formateur détaillé
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Handler pour le fichier
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Handler pour la console avec Rich
    console_handler = RichHandler(rich_tracebacks=True)
    console_handler.setLevel(logging.INFO)
    
    # Configuration de base
    logging.basicConfig(
        level=logging.DEBUG,  # Niveau global à DEBUG
        handlers=[console_handler, file_handler]
    )
    
    logger = logging.getLogger("portfolio")
    logger.setLevel(logging.DEBUG)
    
    return logger