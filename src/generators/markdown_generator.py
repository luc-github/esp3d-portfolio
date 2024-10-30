import logging
from datetime import datetime, timezone
from typing import Dict, List, Any
from ..utils.constants import STATUS_EMOJIS, CHART_CHARS

class MarkdownGenerator:
    def __init__(self, config_manager):
        self.logger = logging.getLogger("portfolio.markdown")
        self.config = config_manager
        
    def generate_readme(self, data: Dict[str, Any]) -> str:
        """Generate complete README content"""
        content = []
        
        # Header section
        content.extend(self._generate_header(data))
        
        # Navigation section
        content.extend(self._generate_navigation(data))
        
        # Statistics section
        content.extend(self._generate_statistics(data))
        
        # Projects status section
        content.extend(self._generate_projects_status(data))
        
        # Global issues section
        content.extend(self._generate_global_issues(data))
        
        # Activity summary section
        content.extend(self._generate_activity_summary(data))
        
        # Footer
        content.extend(self._generate_footer())
        
        return '\n'.join(content)
    
def _generate_health_suggestions(self, repository: Dict) -> List[Dict]:
        """Generate improvement suggestions based on health metrics"""
        suggestions = []
        scores = repository.get('health_score', {})
        
        # Documentation suggestions
        if scores.get('documentation_score', 0) < 0.6:
            missing_docs = self._check_missing_documentation(repository)
            for doc in missing_docs:
                suggestions.append({
                    'category': 'Documentation',
                    'priority': 'high' if doc['type'] in ['README', 'LICENSE'] else 'medium',
                    'suggestion': f"Add {doc['type']}: {doc['description']}",
                    'impact': doc['impact']
                })

        # Maintenance suggestions
        if scores.get('maintenance_score', 0) < 0.6:
            if self._is_commit_frequency_low(repository):
                suggestions.append({
                    'category': 'Maintenance',
                    'priority': 'medium',
                    'suggestion': 'Increase commit frequency - repository shows low activity',
                    'impact': 'Regular updates indicate active maintenance and development'
                })
            if self._has_stale_issues(repository):
                suggestions.append({
                    'category': 'Maintenance',
                    'priority': 'high',
                    'suggestion': 'Address stale issues - some issues have been open for over 6 months',
                    'impact': 'Long-standing issues may discourage community engagement'
                })

        # Activity suggestions
        if scores.get('activity_score', 0) < 0.6:
            if self._is_single_maintainer(repository):
                suggestions.append({
                    'category': 'Activity',
                    'priority': 'medium',
                    'suggestion': 'Consider recruiting additional maintainers',
                    'impact': 'Multiple maintainers ensure project continuity and faster response times'
                })

        # Community suggestions
        if scores.get('community_score', 0) < 0.6:
            missing_community = self._check_missing_community_files(repository)
            for item in missing_community:
                suggestions.append({
                    'category': 'Community',
                    'priority': 'medium',
                    'suggestion': f"Add {item['file']}: {item['purpose']}",
                    'impact': item['impact']
                })

        return suggestions
def _check_missing_documentation(self, repository: Dict) -> List[Dict]:
        """Check for missing documentation"""
        missing = []
        
        if not repository.get('readme_content'):
            missing.append({
                'type': 'README',
                'description': 'Add a README.md with project description, setup instructions, and usage examples',
                'impact': 'Helps users understand and use your project'
            })
            
        if not repository.get('license'):
            missing.append({
                'type': 'LICENSE',
                'description': 'Add a license file to clarify terms of use',
                'impact': 'Defines how others can use and contribute to your project'
            })
            
        if not any('docs/' in f for f in repository.get('files', [])):
            missing.append({
                'type': 'Documentation',
                'description': 'Create a docs/ directory with detailed documentation',
                'impact': 'Provides in-depth information for users and contributors'
            })
            
        return missing

    def _is_commit_frequency_low(self, repository: Dict) -> bool:
        """Check if commit frequency is below threshold"""
        activity = repository.get('activity', {}).get('commit_frequency', {})
        monthly_commits = activity.get('monthly', 0)
        return monthly_commits < 4  # Less than 4 commits per month

    def _has_stale_issues(self, repository: Dict) -> bool:
        """Check for stale issues"""
        six_months_ago = datetime.now(timezone.utc) - timedelta(days=180)
        for issue in repository.get('issues', []):
            if issue['state'] == 'open':
                updated_at = datetime.fromisoformat(issue['updated_at'].replace('Z', '+00:00'))
                if updated_at < six_months_ago:
                    return True
        return False

    def _is_single_maintainer(self, repository: Dict) -> bool:
        """Check if repository has single maintainer"""
        active_contributors = len(repository.get('contributors', []))
        return active_contributors < 2

    def _check_missing_community_files(self, repository: Dict) -> List[Dict]:
        """Check for missing community files"""
        community_files = [
            {
                'file': 'CONTRIBUTING.md',
                'purpose': 'Guidelines for contributing to the project',
                'impact': 'Helps new contributors understand how to participate'
            },
            {
                'file': 'CODE_OF_CONDUCT.md',
                'purpose': 'Project code of conduct',
                'impact': 'Ensures a welcoming and inclusive community'
            },
            {
                'file': 'SECURITY.md',
                'purpose': 'Security policy and reporting guidelines',
                'impact': 'Helps manage security vulnerabilities responsibly'
            }
        ]
        
        missing = []
        existing_files = [f.lower() for f in repository.get('files', [])]
        
        for cf in community_files:
            if not any(cf['file'].lower() in f for f in existing_files):
                missing.append(cf)
                
        return missing

    def _generate_header(self, data: Dict) -> List[str]:
        """Generate header section with badges"""
        stats = data['stats']
        
        return [
            '# 🛠️ ESP3D Portfolio',
            '',
            '<div align="center">',
            '',
            f'![Repositories](https://img.shields.io/badge/Repositories-{stats["repositories"]["total_count"]}-blue)',
            f'![Main Projects](https://img.shields.io/badge/Main%20Projects-{stats["repositories"]["main_projects"]}-orange)',
            f'![Dependencies](https://img.shields.io/badge/Dependencies-{stats["repositories"]["dependencies"]}-green)',
            f'![Open Issues](https://img.shields.io/badge/Open%20Issues-{stats["issues"]["open_count"]}-yellow)',
            '',
            '> 📑 Real-time status and analysis of ESP3D-related projects',
            '',
            '</div>',
            ''
        ]
    
    def _generate_navigation(self, data: Dict) -> List[str]:
        """Generate quick navigation section"""
        content = [
            '## 🔍 Quick Navigation',
            '',
            '<div align="center">',
            '',
            '| Section | Type | Description |',
            '|---------|------|-------------|'
        ]
        
        # Add main projects first
        for repo in data['repositories']:
            if repo['type'] == 'main':
                type_emoji = STATUS_EMOJIS['main_project']
                content.append(
                    f'| [{type_emoji} {repo["name"]}](#{repo["name"].lower()}) | Main Project | '
                    f'{repo["description"] or "Project status and issues"} |'
                )
        
        # Then add dependencies
        for repo in data['repositories']:
            if repo['type'] == 'dependency':
                type_emoji = STATUS_EMOJIS['dependency']
                content.append(
                    f'| [{type_emoji} {repo["name"]}](#{repo["name"].lower()}) | Dependency | '
                    f'{repo["description"] or "Project status and issues"} |'
                )
        
        content.extend([
            '| [📋 Global Issues](#-global-issues) | Overview | All open issues across projects |',
            '| [📊 Statistics](#-statistics) | Metrics | Project health and activity metrics |',
            '',
            '</div>',
            ''
        ])
        
        return content
    
    def _generate_statistics(self, data: Dict) -> List[str]:
        """Generate statistics section with charts"""
        stats = data['stats']
        content = [
            '## 📊 Statistics',
            '',
            '<details>',
            '<summary>Click to view detailed statistics</summary>',
            '',
            '### Repository Statistics',
            '',
            '| Metric | Value |',
            '|--------|-------|',
            f'| Total Repositories | {stats["repositories"]["total_count"]} |',
            f'| Main Projects | {stats["repositories"]["main_projects"]} |',
            f'| Dependencies | {stats["repositories"]["dependencies"]} |',
            f'| Total Stars | {stats["repositories"].get("total_stars", 0)} |',
            f'| Total Forks | {stats["repositories"].get("total_forks", 0)} |',
            '',
            '### Issue Statistics',
            '',
            '| Metric | Value |',
            '|--------|-------|',
            f'| Open Issues | {stats["issues"]["open_count"]} |',
            f'| Closed Issues | {stats["issues"]["closed_count"]} |',
            f'| Average Age | {stats["issues"]["avg_age_days"]:.1f} days |',
            f'| Close Rate | {stats["issues"]["close_rate"]*100:.1f}% |',
            '',
            '### Recent Activity',
            '',
            '```',
            self._generate_activity_chart(data['stats']['activity']['commit_frequency']),
            '```',
            '',
            '</details>',
            ''
        ]
        
        return content
    
    def _generate_projects_status(self, data: Dict) -> List[str]:
        """Generate projects status section"""
        content = ['## 📦 Projects Status', '']
        
        # Sort repositories: main projects first, then dependencies
        sorted_repos = sorted(
            data['repositories'],
            key=lambda x: (x['type'] != 'main', x['name'].lower())
        )
        
        for repo in sorted_repos:
            content.extend(self._generate_repository_section(repo))
            content.extend(['', '<hr>', ''])
            
        return content
    
    def _generate_repository_section(self, repo: Dict) -> List[str]:
        """Generate section for a single repository"""
        type_emoji = STATUS_EMOJIS['main_project'] if repo['type'] == 'main' else STATUS_EMOJIS['dependency']
        
        content = [
            f'<details open>',
            f'<summary><h3>{type_emoji} {repo["name"]}</h3></summary>',
            '',
            '<table><tr><td>',
            '',
            f'**Project**: [{repo["name"]}]({repo["url"]})<br>',
            f'**Type**: {repo["type"].title()}<br>',
            f'**Description**: {repo["description"] or "No description"}<br>',
            f'**Language**: {repo["language"] or "Not specified"}<br>',
            f'**Health Score**: {self._generate_health_score_badge(repo)}',
            '',
            '</td></tr></table>',
            ''
        ]
        
        # Add branches sections
        for branch in repo.get('branches', []):
            content.extend(self._generate_branch_section(branch))
            
        content.append('</details>')
        return content
    
    def _generate_branch_section(self, branch: Dict) -> List[str]:
        """Generate section for a single branch"""
        label_emoji = STATUS_EMOJIS['production'] if branch['is_production'] else STATUS_EMOJIS['development']
        
        content = [
            f'<details>',
            f'<summary><h4>{label_emoji} {branch["label"]} Branch (`{branch["name"]}`)</h4></summary>',
            '',
            '```',
            f'Last commit: {branch["last_commit"]["date"].split("T")[0]} (#{branch["last_commit"]["sha"]})',
            f'Author: {branch["last_commit"]["author"]}',
            '```',
            ''
        ]
        
        if branch.get('issues'):
            content.extend(self._generate_issues_table(branch['issues']))
        else:
            content.append('> 🎉 No open issues')
        suggestions = self._generate_health_suggestions(repo)
        if suggestions:
            content.append('\n#### 📈 Improvement Suggestions\n')
            for suggestion in suggestions:
                priority_marker = {
                    'high': '🔴',
                    'medium': '🟡',
                    'low': '🟢'
                }.get(suggestion['priority'], '⚪')
                
                content.append(f"- {priority_marker} **{suggestion['category']}**: {suggestion['suggestion']}")
                content.append(f"  - Impact: {suggestion['impact']}")
            content.append('')    
        content.extend(['', '</details>', ''])
        return content
    
    def _generate_issues_table(self, issues: List[Dict]) -> List[str]:
        """Generate table of issues"""
        content = [
            '<table>',
            '<tr><th>Status</th><th>Issue</th><th>Created</th><th>Updated</th><th>Priority</th></tr>'
        ]
        
        for issue in issues:
            state_marker = self._get_issue_state_marker(issue)
            created_date = issue['created_at'].split('T')[0]
            updated_date = issue['updated_at'].split('T')[0]
            
            priority_style = self._get_priority_style(issue['priority'])
            
            content.append(
                f'<tr><td>{state_marker}</td>'
                f'<td>#{issue["number"]}: <a href="{issue["url"]}">{issue["title"]}</a></td>'
                f'<td><code>{created_date}</code></td>'
                f'<td><code>{updated_date}</code></td>'
                f'<td{priority_style}>{issue["priority"]}</td></tr>'
            )
            
        content.append('</table>')
        return content
    
    def _generate_global_issues(self, data: Dict) -> List[str]:
        """Generate global issues section"""
        content = [
            '## 📋 Global Issues',
            '',
            '<details open>',
            '<summary><h3>🔍 All Open Issues</h3></summary>',
            ''
        ]
        
        # Group issues by repository
        issues_by_repo = {}
        for repo in data['repositories']:
            repo_issues = []
            for branch in repo.get('branches', []):
                for issue in branch.get('issues', []):
                    if issue['state'] == 'open':  # Only include open issues
                        repo_issues.append({**issue, 'branch': branch['name'], 'branch_label': branch['label']})
            if repo_issues:
                issues_by_repo[repo['name']] = repo_issues
        
        # Generate sections for each repository
        for repo_name, issues in issues_by_repo.items():
            content.extend([
                f'<details>',
                f'<summary><b>📁 {repo_name}</b></summary>',
                '',
                '<table>',
                '<tr><th>Status</th><th>Branch</th><th>Issue</th><th>Created</th><th>Updated</th><th>Priority</th></tr>'
            ])
            
            # Sort issues by priority and update date
            sorted_issues = sorted(
                issues,
                key=lambda x: (self._priority_sort_key(x['priority']), x['updated_at']),
                reverse=True
            )
            
            for issue in sorted_issues:
                state_marker = self._get_issue_state_marker(issue)
                branch_emoji = STATUS_EMOJIS['production'] if issue['branch_label'] == 'Production' else STATUS_EMOJIS['development']
                
                content.append(
                    f'<tr><td>{state_marker}</td>'
                    f'<td>{branch_emoji} {issue["branch"]}</td>'
                    f'<td>#{issue["number"]}: <a href="{issue["url"]}">{issue["title"]}</a></td>'
                    f'<td><code>{issue["created_at"].split("T")[0]}</code></td>'
                    f'<td><code>{issue["updated_at"].split("T")[0]}</code></td>'
                    f'<td{self._get_priority_style(issue["priority"])}>{issue["priority"]}</td></tr>'
                )
            
            content.extend(['</table>', '', '</details>', ''])
        
        content.extend(['</details>', ''])
        return content
    
    def _generate_activity_summary(self, data: Dict) -> List[str]:
        """Generate activity summary section"""
        content = [
            '## 📈 Recent Activity',
            '',
            '<details>',
            '<summary>Click to view recent activity</summary>',
            '',
            '### Last 7 Days',
            ''
        ]
        
        # Add activity statistics
        stats = data['stats']['activity']
        content.extend([
            '| Activity | Count |',
            '|----------|--------|',
            f'| Commits | {stats["total_commits"]} |',
            f'| New Issues | {data["stats"]["issues"]["recent_activity"]["last_week"]} |',
            f'| Closed Issues | {data["stats"]["issues"]["recent_activity"].get("closed_last_week", 0)} |',
            f'| Active Contributors | {stats["active_contributors"]["last_week"]} |',
            ''
        ])
        
        # Add activity heatmap
        content.extend([
            '### Activity Heatmap',
            '',
            '```',
            self._generate_heatmap(data['stats']['activity']['activity_heatmap']),
            '```',
            '',
            '</details>',
            ''
        ])
        
        return content
    
    def _generate_footer(self) -> List[str]:
        """Generate footer section"""
        return [
            '<hr>',
            '',
            '<div align="center">',
            '',
            f'*🔄 Last updated: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")} UTC*',
            '',
            '*Generated by [esp3d-portfolio](https://github.com/luc-github/esp3d-portfolio)*',
            '',
            '</div>'
        ]
    
    def _generate_health_score_badge(self, repo: Dict) -> str:
        """Generate health score badge with color"""
        health_score = repo.get('health_score', {}).get('overall_score', 0) * 100
        color = self._get_health_score_color(health_score)
        return f'<span style="color: {color}">{"%.1f" % health_score}%</span>'
    
    def _generate_activity_chart(self, commit_frequency: Dict) -> str:
        """Generate ASCII chart for commit activity"""
        if not commit_frequency:
            return "No activity data available"
            
        # S'assurer que nous avons une liste de dictionnaires avec 'date' et 'count'
        if isinstance(commit_frequency, list):
            data_points = commit_frequency
        else:
            # Convertir les données en format attendu
            data_points = []
            for date, count in commit_frequency.items():
                if isinstance(count, dict) and 'total' in count:
                    data_points.append({'date': date, 'total': count['total']})
                elif isinstance(count, (int, float)):
                    data_points.append({'date': date, 'total': count})
            
        if not data_points:
            return "No commits in this period"
            
        try:
            max_value = max(point['total'] for point in data_points)
            if max_value == 0:
                return "No commits in this period"
                
            chart_height = 7
            chart = []
            
            for i in range(chart_height):
                row = []
                threshold = max_value * (chart_height - i) / chart_height
                
                for point in data_points:
                    if point['total'] >= threshold:
                        row.append(CHART_CHARS['block_full'])
                    else:
                        row.append(CHART_CHARS['block_empty'])
                        
                chart.append(''.join(row))
                
            # Ajouter une légende
            dates = [point['date'][:10] for point in data_points]  # Format YYYY-MM-DD
            chart.append('-' * len(data_points))
            chart.append(' '.join(dates))
                
            return '\n'.join(chart)
            
        except Exception as e:
            self.logger.error(f"Error generating activity chart: {e}")
            return "Error generating activity chart"
          
    def _generate_heatmap(self, heatmap_data: List[List[int]]) -> str:
        """Generate ASCII heatmap for activity"""
        if not heatmap_data:
            return "No heatmap data available"
            
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        hours = [f'{h:02d}' for h in range(0, 24, 3)]
        
        heatmap = []
        
        # Add hours header
        header = '    ' + ' '.join(hours)
        heatmap.append(header)
        heatmap.append('    ' + '-' * (len(header) - 4))
        
        # Add data rows
        for day_idx, day_data in enumerate(heatmap_data):
            row = [days[day_idx]]
            for hour_idx in range(0, 24, 3):
                # Calculate average activity for this 3-hour block
                block_activity = sum(day_data[hour_idx:hour_idx + 3]) / 3
                
                # Convert activity level to character
                if block_activity == 0:
                    char = CHART_CHARS['block_empty']
                elif block_activity < 2:
                    char = CHART_CHARS['block_quarter']
                elif block_activity < 5:
                    char = CHART_CHARS['block_half']
                else:
                    char = CHART_CHARS['block_full']
                    
                row.append(char)
                
            heatmap.append(' '.join([f"{row[0]:<3}"] + row[1:]))
            
        return '\n'.join(heatmap)
    
    def _get_issue_state_marker(self, issue: Dict) -> str:
        """Get appropriate emoji marker for issue state"""
        if issue.get('is_pr'):
            return STATUS_EMOJIS['pull_request']
        return STATUS_EMOJIS[issue['state']]
    
    def _get_priority_style(self, priority: str) -> str:
        """Get HTML style for priority cell"""
        colors = {
            'critical': '#ff0000',
            'high': '#ff9900',
            'medium': '#ffcc00',
            'low': '#009900'
        }
        return f' style="color: {colors.get(priority.lower(), "#000000")}"'
    
    def _priority_sort_key(self, priority: str) -> int:
        """Get sort key for priority"""
        priority_order = {
            'critical': 0,
            'high': 1,
            'medium': 2,
            'low': 3
        }
        return priority_order.get(priority.lower(), 999)
    
    def _get_health_score_color(self, score: float) -> str:
        """Get color for health score"""
        if score >= 90:
            return '#00cc00'  # Green
        elif score >= 75:
            return '#99cc00'  # Light green
        elif score >= 60:
            return '#ffcc00'  # Yellow
        elif score >= 40:
            return '#ff9900'  # Orange
        else:
            return '#ff0000'  # Red