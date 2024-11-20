#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from rich.console import Console
from rich.progress import track
from src.analyzer import PortfolioAnalyzer
from src.utils.logger import setup_logger
from src.utils.config_manager import ConfigManager

def main():
    # Load configuration
    config_path = Path("config/portfolio_config.json")
    if not config_path.exists():
        print(f"ERROR: Configuration file not found at {config_path}")
        return
        
    try:
        config_manager = ConfigManager(config_path)
        
        # Setup logging with config
        logger = setup_logger(config_manager)
        logger.info("Starting ESP3D Portfolio analysis")
        
        # Vérifier que le token GitHub est configuré
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            logger.error("GITHUB_TOKEN environment variable is not set")
            return
        
        # Initialize analyzer
        analyzer = PortfolioAnalyzer(github_token, config_manager)
        
        # Run analysis
        analyzer.run_analysis()
        
        logger.info("Analysis completed successfully")
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        if logger:
            logger.exception("Error during analysis")

if __name__ == "__main__":
    main()