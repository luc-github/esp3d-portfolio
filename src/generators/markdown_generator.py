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
                    f'| [{type_emoji} {repo["name"]}](#user-content-{repo["name"].lower()}) | Main Project | '
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
            f'<details open id="{repo["name"].lower()}">\n<summary><h3>{type_emoji} {repo["name"]}</h3></summary>'
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
    
    def _generate_health_score_section(self, repo: Dict) -> List[str]:
        """Generate health score section with suggestions"""
        health_score = repo.get('health_score', {})
        overall_score = health_score.get('overall_score', 0) * 100
        content = [
            f'**Health Score**: {self._generate_health_score_badge(repo)}',
            '',
            '<details>',
            '<summary>📊 Health Score Details</summary>',
            '',
            '| Metric | Score | Status |',
            '|--------|--------|--------|'
        ]
        
        metrics = {
            'documentation_score': {
                'name': 'Documentation',
                'suggestions': {
                    'low': '- Add more detailed README\n- Create documentation directory\n- Add usage examples',
                    'medium': '- Enhance API documentation\n- Add more code comments\n- Create wiki pages',
                    'high': '- Keep documentation up to date\n- Consider adding video tutorials'
                }
            },
            'maintenance_score': {
                'name': 'Maintenance',
                'suggestions': {
                    'low': '- Increase commit frequency\n- Address stale issues\n- Set up automated testing',
                    'medium': '- Improve test coverage\n- Regular dependency updates\n- Set up branch protection',
                    'high': '- Monitor performance metrics\n- Regular security audits'
                }
            },
            'activity_score': {
                'name': 'Activity',
                'suggestions': {
                    'low': '- Engage with community\n- Regular status updates\n- Promote the project',
                    'medium': '- Host community calls\n- Write blog posts\n- Create roadmap',
                    'high': '- Consider feature requests\n- Regular releases'
                }
            },
            'community_score': {
                'name': 'Community',
                'suggestions': {
                    'low': '- Add contributing guidelines\n- Add code of conduct\n- Welcome new contributors',
                    'medium': '- Create issue templates\n- Regular acknowledgments\n- Set up discussions',
                    'high': '- Mentor new contributors\n- Recognize key contributors'
                }
            }
        }
        
        for metric, info in metrics.items():
            score = health_score.get(metric, 0) * 100
            if score < 40:
                status = '🔴 Needs Attention'
                level = 'low'
            elif score < 70:
                status = '🟡 Good'
                level = 'medium'
            else:
                status = '🟢 Excellent'
                level = 'high'
                
            content.append(f'| {info["name"]} | {score:.1f}% | {status} |')
            
            # Add suggestions for metrics below 70%
            if score < 70:
                if len(content) > 0 and not content[-1].endswith('|'):
                    content.append('')
                content.append(f'**{info["name"]} Suggestions:**\n{info["suggestions"][level]}')
        
        content.extend(['', '</details>', ''])
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
            content.extend(self._generate_health_score_section(repo))
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
        """Generate colored activity heatmap"""
        if not heatmap_data:
            return "No heatmap data available"
            
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        hours = [f'{h:02d}' for h in range(0, 24, 3)]
        
        # Plus explicite et plus coloré
        activity_levels = {
            0: ("⬜", "No activity"),
            1: ("🟦", "Low (1-2 commits)"),
            2: ("🟩", "Moderate (3-5 commits)"),
            3: ("🟨", "High (6-10 commits)"),
            4: ("🟥", "Very High (>10 commits)")
        }
        
        heatmap = []
        
        # Add hours header
        header = '    ' + ' '.join(hours)
        heatmap.append(header)
        heatmap.append('    ' + '-' * (len(header) - 4))
        
        # Add data rows
        for day_idx, day_data in enumerate(heatmap_data):
            row = [days[day_idx]]
            for hour_idx in range(0, 24, 3):
                block_activity = sum(day_data[hour_idx:hour_idx + 3]) / 3
                
                # Convert activity level to emoji
                if block_activity == 0:
                    level = 0
                elif block_activity <= 2:
                    level = 1
                elif block_activity <= 5:
                    level = 2
                elif block_activity <= 10:
                    level = 3
                else:
                    level = 4
                    
                row.append(activity_levels[level][0])
                
            heatmap.append(' '.join([f"{row[0]:<3}"] + row[1:]))
        
        # Add legend with descriptions
        heatmap.extend([
            '',
            'Legend:',
            ' '.join(f"{emoji} {desc}" for emoji, desc in activity_levels.values())
        ])
            
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