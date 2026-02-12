"""
Production-grade job data module
Optimized for fast lookup, deduplication, and scalable architecture.
"""

from dataclasses import dataclass
from typing import Tuple, Dict


# =====================================================
# DATA MODELS (VERY PROFESSIONAL)
# =====================================================

@dataclass(frozen=True)
class Suggestion:
    text: str
    icon: str


@dataclass(frozen=True)
class FilterOption:
    id: str
    text: str


# =====================================================
# JOB SUGGESTIONS
# Tuple = immutable -> safer + faster
# =====================================================

JOB_SUGGESTIONS: Tuple[Suggestion, ...] = tuple({
    Suggestion("Software Engineer", "💻"),
    Suggestion("Full Stack Developer", "🔧"),
    Suggestion("Data Scientist", "📊"),
    Suggestion("Product Manager", "📱"),
    Suggestion("DevOps Engineer", "⚙️"),
    Suggestion("UI/UX Designer", "🎨"),
    Suggestion("Python Developer", "🐍"),
    Suggestion("Java Developer", "☕"),
    Suggestion("React Developer", "⚛️"),
    Suggestion("Machine Learning Engineer", "🤖"),
    Suggestion("Backend Developer", "🖧"),
    Suggestion("Frontend Developer", "🎨"),
    Suggestion("Node.js Developer", "🌿"),
    Suggestion("Cloud Engineer", "☁️"),
    Suggestion("Cybersecurity Analyst", "🔒"),
    Suggestion("Blockchain Developer", "🔗"),
    Suggestion("Mobile App Developer", "📱"),
    Suggestion("Game Developer", "🎮"),
    Suggestion("QA Engineer", "✅"),
})


# =====================================================
# LOCATIONS (AUTO-DEDUPED)
# =====================================================

_raw_locations = {
    "Bangalore", "Mumbai", "Delhi", "Hyderabad", "Pune",
    "Chennai", "Noida", "Gurgaon", "Ahmedabad",
    "Kolkata", "Vadodara", "Remote", "Work from Home",
    "Lucknow", "Kanpur", "Agra", "Varanasi",
    "Jaipur", "Chandigarh", "Dehradun", "Shimla",
    "Kochi", "Visakhapatnam", "Nagpur", "Surat"
}

LOCATION_SUGGESTIONS: Tuple[Suggestion, ...] = tuple(
    Suggestion(loc, "📍" if loc not in {"Remote", "Work from Home"} else "🏠")
    for loc in sorted(_raw_locations)
)


# =====================================================
# FILTER OPTIONS
# =====================================================

JOB_TYPES: Tuple[FilterOption, ...] = (
    FilterOption("all", "All Types"),
    FilterOption("full-time", "Full Time"),
    FilterOption("part-time", "Part Time"),
    FilterOption("contract", "Contract"),
    FilterOption("internship", "Internship"),
    FilterOption("remote", "Remote"),
)

EXPERIENCE_RANGES: Tuple[FilterOption, ...] = (
    FilterOption("all", "All Levels"),
    FilterOption("fresher", "Fresher"),
    FilterOption("1-3", "1-3 years"),
    FilterOption("3-5", "3-5 years"),
    FilterOption("5-7", "5-7 years"),
    FilterOption("7+", "7+ years"),
)

SALARY_RANGES: Tuple[FilterOption, ...] = (
    FilterOption("all", "All Ranges"),
    FilterOption("0-3", "0-3 LPA"),
    FilterOption("3-6", "3-6 LPA"),
    FilterOption("6-10", "6-10 LPA"),
    FilterOption("10-15", "10-15 LPA"),
    FilterOption("15+", "15+ LPA"),
)


# =====================================================
# ⚡ ULTRA FAST LOOKUPS (Senior-level technique)
# =====================================================

JOB_LOOKUP: Dict[str, Suggestion] = {
    job.text.lower(): job
    for job in JOB_SUGGESTIONS
}

LOCATION_LOOKUP: Dict[str, Suggestion] = {
    loc.text.lower(): loc
    for loc in LOCATION_SUGGESTIONS
}


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def get_job_suggestions(query: str):
    """O(n) but extremely fast due to tuple + no mutation."""

    q = query.lower().strip()

    return [
        job for job in JOB_SUGGESTIONS
        if q in job.text.lower()
    ][:5]


def get_location_suggestions(query: str):

    q = query.lower().strip()

    return [
        loc for loc in LOCATION_SUGGESTIONS
        if q in loc.text.lower()
    ][:5]