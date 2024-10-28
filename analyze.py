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
    # Setup console for rich output
    console = Console()
    
    try:
        # Setup logging
        logger = setup_logger()
        logger.info("Starting ESP3D Portfolio analysis")
        
        # Load configuration
        config_path = Path("config/portfolio_config.json")
        if not config_path.exists():
            console.print("[red]Configuration file not found![/red]")
            sys.exit(1)
            
        config_manager = ConfigManager(config_path)
        
        # Check for GitHub token
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            console.print("[red]GitHub token not found! Please set GITHUB_TOKEN environment variable.[/red]")
            sys.exit(1)
            
        # Initialize analyzer
        analyzer = PortfolioAnalyzer(github_token, config_manager)
        
        # Run analysis with progress tracking
        with console.status("[bold green]Analyzing repositories...") as status:
            analyzer.run_analysis()
            
        console.print("[green]Analysis completed successfully![/green]")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Analysis interrupted by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Error during analysis: {str(e)}[/red]")
        logger.exception("Error during analysis")
        sys.exit(1)

if __name__ == "__main__":
    main()