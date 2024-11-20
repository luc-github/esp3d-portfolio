import logging
from typing import Dict, Any
from datetime import datetime
from .collectors import GitHubCollector, CacheManager
from .processors import StatsCalculator, IssueProcessor
from .generators import MarkdownGenerator
from .utils import ConfigManager

class PortfolioAnalyzer:
    def __init__(self, github_token: str, config_manager: ConfigManager):
        """Initialize the portfolio analyzer.
        
        Args:
            github_token: GitHub API token
            config_manager: Configuration manager instance
        """
        self.logger = logging.getLogger("portfolio.analyzer")
        self.config = config_manager
        
        # Initialize components
        self.cache_manager = CacheManager(self.config.get_cache_config())
        self.github_collector = GitHubCollector(github_token, self.config, self.cache_manager)
        self.stats_calculator = StatsCalculator(self.config)
        self.issue_processor = IssueProcessor(self.config)
        self.markdown_generator = MarkdownGenerator(self.config)
        
        self.logger.info("Portfolio analyzer initialized")
    
    def run_analysis(self) -> None:
        """Run the complete portfolio analysis."""
        try:
            # Collect and process data
            portfolio_data = self._collect_data()
            processed_data = self._process_data(portfolio_data)
            
            # Generate and save reports
            self._generate_reports(processed_data)
            
            self.logger.info("Analysis completed successfully")
            
        except Exception as e:
            self.logger.error(f"Error during analysis: {e}")
            raise
    
    def _collect_data(self) -> Dict[str, Any]:
        """Collect data from GitHub."""
        self.logger.info("Starting data collection")
        
        repositories_data = []
        for repo_config in self.config.get_repositories():
            try:
                repo_data = self.github_collector.collect_repository_data(repo_config['name'])
                repositories_data.append(repo_data)
            except Exception as e:
                self.logger.error(f"Error collecting data for {repo_config['name']}: {e}")
        
        return {
            'repositories': repositories_data,
            'rate_limit': self.github_collector.get_rate_limit_info()
        }
    
    def _process_data(self, portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process collected data."""
        self.logger.info("Processing collected data")
        
        # Process issues for each repository
        for repo in portfolio_data['repositories']:
            repo = self.issue_processor.process_repository_issues(repo)
        
        # Calculate overall statistics
        portfolio_data['stats'] = self.stats_calculator.calculate_portfolio_stats(
            portfolio_data['repositories']
        )
        
        # Calculate health scores for each repository
        for repo in portfolio_data['repositories']:
            repo['health_score'] = self.stats_calculator.calculate_repository_health(repo)
        
        # Calculate activity rankings
        portfolio_data['activity_ranking'] = self.stats_calculator.calculate_activity_kpi(
            portfolio_data['repositories']
        )
        
        return portfolio_data
    
    def _generate_reports(self, processed_data: Dict[str, Any]) -> None:
        """Generate all reports."""
        self.logger.info("Generating reports")
        
        # Generate README
        readme_content = self.markdown_generator.generate_readme(processed_data)
        self._save_report(readme_content, 'README.md')
        
        # Save raw data
        self._save_report(processed_data, 'github_portfolio.json', is_json=True)

    def _save_report(self, content: Any, filename: str, is_json: bool = False) -> None:
        """Save report to file."""
        def json_serial(obj):
            """JSON serializer for objects not serializable by default json code"""
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Type {type(obj)} not serializable")

        try:
            mode = 'w' if not is_json else 'w'
            with open(filename, mode, encoding='utf-8') as f:
                if is_json:
                    import json
                    json.dump(content, f, indent=2, default=json_serial)
                else:
                    f.write(content)
                    
            self.logger.info(f"Saved report: {filename}")
            
        except Exception as e:
            self.logger.error(f"Error saving report {filename}: {e}")
            raise

    def cleanup(self) -> None:
        """Cleanup resources and temporary files."""
        try:
            self.cache_manager.cleanup()
            self.logger.info("Cleanup completed")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")