from enum import Enum

class ProjectType(Enum):
    MAIN = "main"
    DEPENDENCY = "dependency"

class IssueState(Enum):
    OPEN = "open"
    CLOSED = "closed"

class IssuePriority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

# Status emojis
STATUS_EMOJIS = {
    "open": "⭕",
    "closed": "✅",
    "pull_request": "🔄",
    "production": "🚀",
    "development": "🔧",
    "main_project": "⭐",
    "dependency": "🔗",
    "critical": "🔥",
    "high": "⚡",
    "recent": "🆕"
}

# Chart characters for ASCII graphs
CHART_CHARS = {
    "vertical": "│",
    "horizontal": "─",
    "corner_tl": "┌",
    "corner_tr": "┐",
    "corner_bl": "└",
    "corner_br": "┘",
    "junction_l": "├",
    "junction_r": "┤",
    "junction_t": "┬",
    "junction_b": "┴",
    "cross": "┼",
    "block_empty": "░",
    "block_quarter": "▒",
    "block_half": "▓",
    "block_full": "█"
}

# Time constants
SECONDS_IN_DAY = 86400
DAYS_IN_WEEK = 7
DAYS_IN_MONTH = 30

# Cache constants
DEFAULT_CACHE_TIMEOUT = 3600
MAX_CACHE_AGE = 86400  # 1 day

# API constants
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds
API_TIMEOUT = 10  # seconds

# Display constants
DEFAULT_CHART_WIDTH = 80
DEFAULT_CHART_HEIGHT = 10
MAX_DESCRIPTION_LENGTH = 100