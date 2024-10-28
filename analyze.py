import os
from github import Github
from datetime import datetime
import json

class GitHubPortfolioAnalyzer:
    def __init__(self, token, config_file='portfolio_config.json'):
        self.g = Github(token)
        self.user = self.g.get_user()
        
        # Load configuration
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.repo_configs = {repo['name']: repo for repo in config['repositories']}
                self.options = config.get('options', {
                    'include_closed_issues': False,
                    'include_pull_requests': False
                })
            print(f"Loaded configuration: {len(self.repo_configs)} repositories to analyze")
        except FileNotFoundError:
            print(f"Configuration file {config_file} not found. Please create it.")
            raise
        except json.JSONDecodeError:
            print(f"Error parsing {config_file}. Please check the format.")
            raise
        except KeyError as e:
            print(f"Missing required key in configuration: {e}")
            raise
    
    def analyze_repositories(self):
        portfolio = {
            'repositories': [],
            'dependencies': {},
            'todos': []
        }
        
        # Get all repositories first
        print("Fetching repository list...")
        all_repos = list(self.user.get_repos())
        
        # Filter repositories
        for repo in all_repos:
            # Skip if not in target list
            if repo.name not in self.repo_configs:
                continue
                
            print(f"Analyzing repository: {repo.name}")
            repo_config = self.repo_configs[repo.name]
            
            for branch_config in repo_config.get('branches', []):
                branch_name = branch_config['name']
                branch_label = branch_config['label']
                
                try:
                    branch = repo.get_branch(branch_name)
                    
                    repo_info = {
                        'name': repo.name,
                        'description': repo.description,
                        'url': repo.html_url,
                        'language': repo.language,
                        'branch': branch_name,
                        'branch_label': branch_label,
                        'last_commit': branch.commit.commit.author.date.isoformat(),
                        'commit_sha': branch.commit.sha[:7],
                        'created_at': repo.created_at.isoformat(),
                        'last_updated': repo.updated_at.isoformat(),
                        'todos': []
                    }
                    
                    try:
                        # Get TODOs from issues
                        issues = repo.get_issues(state='open' if not self.options['include_closed_issues'] else 'all')
                        for issue in issues:
                            # Skip pull requests if not included in options
                            if issue.pull_request and not self.options['include_pull_requests']:
                                continue
                                
                            todo = {
                                'title': issue.title,
                                'body': issue.body,
                                'created_at': issue.created_at.isoformat(),
                                'repository': repo.name,
                                'branch': branch_name,
                                'branch_label': branch_label,
                                'url': issue.html_url,
                                'number': issue.number,
                                'state': issue.state,
                                'is_pr': bool(issue.pull_request)
                            }
                            repo_info['todos'].append(todo)
                            portfolio['todos'].append(todo)
                        
                    except Exception as e:
                        print(f"Error analyzing {repo.name}/{branch_name}: {str(e)}")
                    
                    portfolio['repositories'].append(repo_info)
                    
                except Exception as e:
                    print(f"Error accessing branch {branch_name} in {repo.name}: {str(e)}")
            
        return portfolio
    
    def save_analysis(self, portfolio, filename='github_portfolio.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(portfolio, f, indent=2, ensure_ascii=False)
            
    def generate_readme(self, portfolio):
        """Generate README content for the portfolio"""
        content = []
        
        content.append('# ESP3D Portfolio\n')
        content.append('This repository tracks the status of ESP3D-related projects and their open issues.\n')
        
        # Overview section with statistics
        content.append('## Overview\n')
        repo_count = len(set(repo['name'] for repo in portfolio['repositories']))
        content.append(f"Total repositories: {repo_count}\n")
        content.append(f"Total TODOs: {len(portfolio['todos'])}\n\n")
        
        # Group repositories by name
        repos_by_name = {}
        for repo in portfolio['repositories']:
            if repo['name'] not in repos_by_name:
                repos_by_name[repo['name']] = []
            repos_by_name[repo['name']].append(repo)
        
        # Repositories section
        content.append('## Repositories\n')
        for repo_name, branches in repos_by_name.items():
            content.append(f"### [{repo_name}]({branches[0]['url']})\n")
            content.append(f"- Description: {branches[0]['description'] or 'No description'}\n")
            content.append(f"- Main language: {branches[0]['language'] or 'Not specified'}\n\n")
            
            for branch in branches:
                label_emoji = "🚀" if branch['branch_label'] == "Production" else "🔧"
                content.append(f"#### {label_emoji} {branch['branch_label']} Branch (`{branch['branch']}`)\n")
                content.append(f"- Last commit: {branch['last_commit'].split('T')[0]} (#{branch['commit_sha']})\n\n")
                
                if branch['todos']:
                    content.append("##### Open Issues:\n")
                    for todo in branch['todos']:
                        state_marker = "🔄" if todo['is_pr'] else "⭕" if todo['state'] == 'open' else "✅"
                        content.append(f"- {state_marker} #{todo['number']}: [{todo['title']}]({todo['url']})\n")
                    content.append("\n")
            content.append("---\n\n")
        
        # Global TODOs section
        content.append('## Global TODOs\n')
        for todo in portfolio['todos']:
            state_marker = "🔄" if todo['is_pr'] else "⭕" if todo['state'] == 'open' else "✅"
            branch_emoji = "🚀" if todo['branch_label'] == "Production" else "🔧"
            content.append(f"- {state_marker} [{todo['repository']}/{todo['branch']}] {branch_emoji} #{todo['number']}: [{todo['title']}]({todo['url']})\n")
        
        # Add footer with generation timestamp
        content.append(f"\n---\n*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC*\n")
        
        return ''.join(content)

def main():
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        raise ValueError("GITHUB_TOKEN is not defined")
    
    analyzer = GitHubPortfolioAnalyzer(token)
    portfolio = analyzer.analyze_repositories()
    
    # Save the raw data
    analyzer.save_analysis(portfolio)
    
    # Generate and save README
    readme_content = analyzer.generate_readme(portfolio)
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)

if __name__ == '__main__':
    main()