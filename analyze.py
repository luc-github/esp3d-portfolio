import os
from github import Github
from datetime import datetime
import json

class GitHubPortfolioAnalyzer:
    def __init__(self, token):
        self.g = Github(token)
        self.user = self.g.get_user()
        
    def analyze_repositories(self):
        portfolio = {
            'repositories': [],
            'dependencies': {},
            'todos': []
        }
        
        for repo in self.user.get_repos():
            repo_info = {
                'name': repo.name,
                'description': repo.description,
                'url': repo.html_url,
                'language': repo.language,
                'created_at': repo.created_at.isoformat(),
                'last_updated': repo.updated_at.isoformat(),
                'dependencies': [],
                'todos': []
            }
            
            try:
                # Rechercher les dépendances dans le README
                readme = repo.get_readme()
                content = readme.decoded_content.decode()
                
                # Chercher les TODOs dans les issues
                for issue in repo.get_issues(state='open'):
                    todo = {
                        'title': issue.title,
                        'body': issue.body,
                        'created_at': issue.created_at.isoformat(),
                        'repository': repo.name,
                        'url': issue.html_url
                    }
                    repo_info['todos'].append(todo)
                    portfolio['todos'].append(todo)
                
                # Chercher les références à d'autres repos
                for other_repo in self.user.get_repos():
                    if other_repo.name in content and other_repo.name != repo.name:
                        repo_info['dependencies'].append(other_repo.name)
                
            except Exception as e:
                print(f"Erreur lors de l'analyse de {repo.name}: {str(e)}")
            
            portfolio['repositories'].append(repo_info)
            
        return portfolio
    
    def save_analysis(self, portfolio, filename='github_portfolio.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(portfolio, f, indent=2, ensure_ascii=False)
            
    def generate_markdown_report(self, portfolio, filename='PORTFOLIO.md'):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('# Portfolio des Projets GitHub\n\n')
            
            f.write('## Vue d'ensemble\n\n')
            f.write(f"Nombre total de repositories: {len(portfolio['repositories'])}\n")
            f.write(f"Nombre total de TODOs: {len(portfolio['todos'])}\n\n")
            
            f.write('## Repositories\n\n')
            for repo in portfolio['repositories']:
                f.write(f"### {repo['name']}\n\n")
                f.write(f"- Description: {repo['description'] or 'Pas de description'}\n")
                f.write(f"- Langage principal: {repo['language'] or 'Non spécifié'}\n")
                if repo['dependencies']:
                    f.write("- Dépendances:\n")
                    for dep in repo['dependencies']:
                        f.write(f"  - {dep}\n")
                f.write(f"- [Voir sur GitHub]({repo['url']})\n\n")
                
                if repo['todos']:
                    f.write("#### TODOs:\n")
                    for todo in repo['todos']:
                        f.write(f"- {todo['title']}\n")
                    f.write("\n")
            
            f.write('## TODOs Globaux\n\n')
            for todo in portfolio['todos']:
                f.write(f"- [{todo['repository']}] {todo['title']}\n")

def main():
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        raise ValueError("GITHUB_TOKEN n'est pas défini")
    
    analyzer = GitHubPortfolioAnalyzer(token)
    portfolio = analyzer.analyze_repositories()
    
    analyzer.save_analysis(portfolio)
    analyzer.generate_markdown_report(portfolio)

if __name__ == '__main__':
    main()