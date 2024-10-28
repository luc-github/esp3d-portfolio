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
        """Generate enhanced README content for the portfolio"""
        content = []
        
        # Header with badges
        content.append('# 🛠️ ESP3D Portfolio\n')
        
        # Add stats badges
        repo_count = len(set(repo['name'] for repo in portfolio['repositories']))
        todo_count = len(portfolio['todos'])
        content.append('<div align="center">\n\n')
        content.append(f'![Repositories](https://img.shields.io/badge/Repositories-{repo_count}-blue)')
        content.append(f' ![Issues](https://img.shields.io/badge/Open%20Issues-{todo_count}-yellow)')
        content.append('\n</div>\n\n')
        
        # Introduction
        content.append('> 📑 This repository tracks the status of ESP3D-related projects and their open issues.\n')
        
        # Quick Navigation
        content.append('## 🔍 Quick Navigation\n\n')
        content.append('<div align="center">\n\n')
        content.append('| Section | Description |\n')
        content.append('|---------|-------------|\n')
        for repo_name in set(repo['name'] for repo in portfolio['repositories']):
            content.append(f'| [🔗 {repo_name}](#-{repo_name.lower()}) | Project status and issues |\n')
        content.append('| [📋 Global TODOs](#-global-todos) | All open issues across projects |\n')
        content.append('\n</div>\n\n')
        
        # Statistics Section
        content.append('<details>\n<summary><h2>📊 Statistics</h2></summary>\n\n')
        
        # Add a statistics table
        content.append('| Metric | Value |\n')
        content.append('|--------|-------|\n')
        content.append(f'| Total Repositories | {repo_count} |\n')
        content.append(f'| Total Open Issues | {todo_count} |\n')
        
        # Count issues per repository
        repos_stats = {}
        for todo in portfolio['todos']:
            repos_stats[todo['repository']] = repos_stats.get(todo['repository'], 0) + 1
        
        for repo, count in repos_stats.items():
            content.append(f'| Issues in {repo} | {count} |\n')
            
        content.append('\n</details>\n\n')
        
        # Repositories section
        content.append('## 📦 Projects Status\n')
        
        # Group repositories by name
        repos_by_name = {}
        for repo in portfolio['repositories']:
            if repo['name'] not in repos_by_name:
                repos_by_name[repo['name']] = []
            repos_by_name[repo['name']].append(repo)
        
        for repo_name, branches in repos_by_name.items():
            content.append(f'<details open>\n<summary><h3>🔗 {repo_name}</h3></summary>\n\n')
            
            # Repository info box
            content.append('<table><tr><td>\n\n')
            content.append(f"**Project**: [{repo_name}]({branches[0]['url']})<br>\n")
            content.append(f"**Description**: {branches[0]['description'] or 'No description'}<br>\n")
            content.append(f"**Language**: {branches[0]['language'] or 'Not specified'}<br>\n")
            content.append('\n</td></tr></table>\n\n')
            
            for branch in branches:
                # Branch header with appropriate emoji
                label_emoji = "🚀" if branch['branch_label'] == "Production" else "🔧"
                content.append(f"<details>\n<summary><h4>{label_emoji} {branch['branch_label']} Branch (`{branch['branch']}`)</h4></summary>\n\n")
                
                # Branch info
                content.append('```\n')
                content.append(f"Last commit: {branch['last_commit'].split('T')[0]} (#{branch['commit_sha']})\n")
                content.append('```\n\n')
                
                # Issues for this branch
                if branch['todos']:
                    content.append('<table>\n')
                    content.append('<tr><th>Status</th><th>Issue</th><th>Created</th></tr>\n')
                    for todo in branch['todos']:
                        state_marker = "🔄" if todo['is_pr'] else "⭕" if todo['state'] == 'open' else "✅"
                        created_date = todo['created_at'].split('T')[0]
                        content.append(f"<tr><td>{state_marker}</td><td>#{todo['number']}: <a href='{todo['url']}'>{todo['title']}</a></td><td><code>{created_date}</code></td></tr>\n")
                    content.append('</table>\n')
                else:
                    content.append('> 🎉 No open issues\n')
                
                content.append('\n</details>\n\n')
            
            content.append('</details>\n\n')
            content.append('<hr>\n\n')
        
        # Global TODOs section
        content.append('## 📋 Global TODOs\n\n')
        content.append('<details open>\n<summary><h3>🔍 All Open Issues</h3></summary>\n\n')
        
        # Group todos by repository
        todos_by_repo = {}
        for todo in portfolio['todos']:
            repo_name = todo['repository']
            if repo_name not in todos_by_repo:
                todos_by_repo[repo_name] = []
            todos_by_repo[repo_name].append(todo)
        
        for repo_name, todos in todos_by_repo.items():
            content.append(f"<details>\n<summary><b>📁 {repo_name}</b></summary>\n\n")
            content.append('<table>\n')
            content.append('<tr><th>Status</th><th>Branch</th><th>Issue</th><th>Created</th></tr>\n')
            
            for todo in todos:
                state_marker = "🔄" if todo['is_pr'] else "⭕" if todo['state'] == 'open' else "✅"
                branch_emoji = "🚀" if todo['branch_label'] == "Production" else "🔧"
                created_date = todo['created_at'].split('T')[0]
                content.append(f"<tr><td>{state_marker}</td><td>{branch_emoji} {todo['branch']}</td><td>#{todo['number']}: <a href='{todo['url']}'>{todo['title']}</a></td><td><code>{created_date}</code></td></tr>\n")
            
            content.append('</table>\n\n</details>\n\n')
        
        content.append('</details>\n\n')
        
        # Footer with timestamp and info
        content.append('<hr>\n\n')
        content.append('<div align="center">\n\n')
        content.append('*🔄 Last updated: ')
        content.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        content.append(' UTC*\n\n')
        content.append('*Generated by [esp3d-portfolio](https://github.com/luc-github/esp3d-portfolio)*\n')
        content.append('\n</div>\n')
        
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