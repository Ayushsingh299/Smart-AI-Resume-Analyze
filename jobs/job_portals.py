import urllib.parse
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)

# =====================================================
# DATA MODEL (VERY PROFESSIONAL)
# =====================================================

@dataclass(frozen=True)
class Portal:
    name: str
    icon: str
    color: str
    url: str


# =====================================================
# JOB PORTAL ENGINE
# =====================================================

class JobPortal:
    """Production-ready job portal integration engine."""

    def __init__(self):

        # Immutable portals -> prevents accidental modification
        self.portals: Tuple[Portal, ...] = (

            Portal(
                "LinkedIn",
                "fab fa-linkedin",
                "#0077b5",
                "https://www.linkedin.com/jobs/search/?keywords={}&location={}&f_E={}"
            ),

            Portal(
                "Indeed",
                "fas fa-search-dollar",
                "#2164f3",
                "https://www.indeed.com/jobs?q={}&l={}&explvl={}"
            ),

            Portal(
                "Naukri",
                "fas fa-briefcase",
                "#4a90e2",
                "https://www.naukri.com/{}-jobs-in-{}?experience={}"
            ),

            Portal(
                "Foundit",
                "fas fa-globe",
                "#ff6b6b",
                'https://www.foundit.in/srp/results?query="{}"&locations={}&experienceRanges={}~{}&experience={}'
            ),

            Portal(
                "Instahyre",
                "fas fa-user-tie",
                "#00bfa5",
                "https://www.instahyre.com/{}-jobs-in-{}"
            ),

            Portal(
                "Freshersworld",
                "fas fa-graduation-cap",
                "#28a745",
                "https://www.freshersworld.com/jobs/jobsearch/{}-jobs-in-{}"
            ),
        )

    # =====================================================
    # FORMATTERS
    # =====================================================

    @staticmethod
    def encode(text: str) -> str:
        """Safe URL encoding."""
        return urllib.parse.quote_plus(text.strip())

    @staticmethod
    def slug(text: str) -> str:
        """Convert to URL slug."""
        return text.strip().lower().replace(" ", "-")

    def parse_experience(self, experience: Optional[Dict]) -> Tuple[str, str, str]:
        """
        Returns:
        (exp_level, exp_min, exp_max)
        """

        if not experience:
            return "", "0", "0"

        exp_id = experience.get("id", "all")

        mapping = {
            "0-1": ("0", "0", "1"),
            "1-3": ("1", "1", "3"),
            "3-5": ("2", "3", "5"),
            "5-7": ("3", "5", "7"),
            "7-10": ("4", "7", "10"),
            "10+": ("5", "10", "15"),
        }

        return mapping.get(exp_id, ("", "0", "0"))

    # =====================================================
    # CORE SEARCH ENGINE
    # =====================================================

    def search_jobs(
        self,
        query: str,
        location: str = "",
        experience: Optional[Dict] = None
    ) -> List[Dict]:
        """Generate job search URLs across portals."""

        encoded_query = self.encode(query)
        encoded_location = self.encode(location) if location else ""
        slug_title = self.slug(query)
        slug_location = self.slug(location) if location else ""

        exp_level, exp_min, exp_max = self.parse_experience(experience)

        results = []

        for portal in self.portals:
            try:

                if portal.name == "Foundit":
                    url = portal.url.format(
                        encoded_query,
                        encoded_location,
                        exp_min,
                        exp_max,
                        exp_min
                    )

                elif portal.name in ["Instahyre", "Freshersworld"]:
                    url = portal.url.format(
                        slug_title,
                        slug_location
                    )

                elif portal.name in ["LinkedIn", "Indeed", "Naukri"]:
                    url = portal.url.format(
                        encoded_query,
                        encoded_location,
                        exp_level
                    )

                else:
                    url = portal.url.format(
                        encoded_query,
                        encoded_location
                    )

                results.append({
                    "portal": portal.name,
                    "icon": portal.icon,
                    "color": portal.color,
                    "title": f"{portal.name} • {query} jobs"
                             + (f" in {location}" if location else ""),
                    "url": url
                })

            except Exception as e:
                logging.error(f"{portal.name} URL generation failed: {e}")

        return results

    # =====================================================
    # HELPER
    # =====================================================

    def get_portals(self) -> Tuple[Portal, ...]:
        """Return immutable portal list."""
        return self.portals