import random
from vector_db import MOCK_CANDIDATES

AVATAR_COLORS = [
    ("rgba(124,58,237,0.15)", "#6d28d9"),
    ("rgba(8,145,178,0.15)",  "#0e7490"),
    ("rgba(5,150,105,0.15)",  "#047857"),
    ("rgba(217,119,6,0.15)",  "#b45309"),
    ("rgba(219,39,119,0.15)", "#9d174d"),
    ("rgba(220,38,38,0.15)",  "#b91c1c"),
]

STATUSES = [
    "Sourced", "Screened", "Interview Scheduled",
    "Offered", "Screened", "Sourced", "Sourced"
]

STATUS_CLASSES = {
    "Sourced":              "status-sourced",
    "Screened":             "status-screened",
    "Interview Scheduled":  "status-interview",
    "Offered":              "status-offered",
    "Rejected":             "status-rejected",
}


def get_avatar(name, idx):
    """Return background color, foreground color, and initials for a candidate."""
    bg, fg = AVATAR_COLORS[idx % len(AVATAR_COLORS)]
    initials = "".join(p[0] for p in name.split()[:2])
    return bg, fg, initials


def get_score(seed_name):
    """Return a deterministic score (62-97) for a candidate based on their name."""
    random.seed(seed_name)
    return random.randint(62, 97)


def score_color_class(score):
    """Return the CSS class for a score badge."""
    if score >= 85: return "score-high"
    if score >= 72: return "score-mid"
    return "score-low"


def card_tier(rank):
    """Return the CSS tier class for a candidate card based on rank."""
    if rank == 1: return "gold"
    if rank == 2: return "silver"
    if rank == 3: return "bronze"
    return "default"


def get_status(name):
    """Return a deterministic status for a candidate."""
    random.seed(name + "status")
    return random.choice(STATUSES)


def filter_candidates(search="", filter_exp="All", filter_loc="All"):
    """Filter the candidate list based on search, experience, and location."""
    filtered = MOCK_CANDIDATES.copy()

    if search:
        q = search.lower()
        filtered = [
            c for c in filtered
            if q in c["name"].lower()
            or q in c["education"].lower()
            or any(q in s.lower() for s in c["skills"])
        ]

    if filter_exp != "All":
        ranges = {
            "0-2 yrs": (0, 2),
            "3-4 yrs": (3, 4),
            "5-6 yrs": (5, 6),
            "7+ yrs":  (7, 99),
        }
        lo, hi = ranges[filter_exp]
        filtered = [c for c in filtered if lo <= c["experience"] <= hi]

    if filter_loc != "All":
        filtered = [c for c in filtered if c["location"] == filter_loc]

    return filtered


def get_sorted_scored_candidates(candidates):
    """Return candidates sorted by score (highest first)."""
    return sorted(
        [(c, get_score(c["name"])) for c in candidates],
        key=lambda x: x[1],
        reverse=True
    )