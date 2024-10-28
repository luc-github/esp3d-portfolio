import logging
from pathlib import Path
from rich.logging import RichHandler
from datetime import datetime

def setup_logger(log_dir="logs"):
    # Create logs directory if it doesn't exist
    Path(log_dir).mkdir(exist_ok=True)
    
    # Configure logging
    log_filename = f"{log_dir}/portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            RichHandler(rich_tracebacks=True),
            logging.FileHandler(log_filename)
        ]
    )
    
    return logging.getLogger("portfolio")