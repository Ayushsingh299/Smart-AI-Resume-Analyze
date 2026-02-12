from typing import List, Dict, Optional

# =====================================================
# COMPANY DATA
# =====================================================

FEATURED_COMPANIES: Dict[str, List[Dict]] = {
    "tech": [
        {
            "name": "Google",
            "color": "#4285F4",
            "careers_url": "https://careers.google.com",
            "description": "Leading technology company known for search, cloud, and AI innovation.",
            "categories": ["Software", "AI/ML", "Cloud", "Data Science"],
            "industry": "Technology"
        },
        {
            "name": "Microsoft",
            "color": "#00A4EF",
            "careers_url": "https://careers.microsoft.com",
            "description": "Global leader in software and enterprise cloud solutions.",
            "categories": ["Software", "Cloud", "Enterprise"],
            "industry": "Technology"
        },
        {
            "name": "Amazon",
            "color": "#FF9900",
            "careers_url": "https://www.amazon.jobs",
            "description": "E-commerce and cloud computing giant.",
            "categories": ["Software", "Cloud", "Operations"],
            "industry": "Technology"
        },
        {
            "name": "Apple",
            "color": "#555555",
            "careers_url": "https://www.apple.com/careers",
            "description": "Innovation leader in consumer hardware and software.",
            "categories": ["Software", "Hardware", "Design"],
            "industry": "Technology"
        },
        {
            "name": "Meta",
            "color": "#1877F2",
            "careers_url": "https://www.metacareers.com/",
            "description": "Social media and metaverse technology company.",
            "categories": ["Software", "AI/ML", "Networking"],
            "industry": "Technology"
        },
    ],

    "indian_tech": [
        {
            "name": "TCS",
            "careers_url": "https://www.tcs.com/careers",
            "description": "India's largest IT services company.",
            "categories": ["IT Services", "Consulting"],
            "industry": "IT Services"
        },
        {
            "name": "Infosys",
            "careers_url": "https://www.infosys.com/careers",
            "description": "Global leader in digital transformation.",
            "categories": ["IT Services", "Consulting"],
            "industry": "IT Services"
        },
        {
            "name": "Wipro",
            "careers_url": "https://careers.wipro.com",
            "description": "Leading global IT and consulting company.",
            "categories": ["IT Services", "Engineering"],
            "industry": "IT Services"
        },
        {
            "name": "HCLTech",
            "careers_url": "https://www.hcltech.com/careers",
            "description": "Global technology and engineering company.",
            "categories": ["Engineering", "Digital"],
            "industry": "IT Services"
        },
    ],

    "global_corps": [
        {
            "name": "IBM",
            "careers_url": "https://www.ibm.com/careers",
            "description": "Technology and consulting leader.",
            "categories": ["AI", "Cloud", "Consulting"],
            "industry": "Technology"
        },
        {
            "name": "Accenture",
            "careers_url": "https://www.accenture.com/careers",
            "description": "Global professional services powerhouse.",
            "categories": ["Consulting", "Technology"],
            "industry": "Consulting"
        },
        {
            "name": "Cognizant",
            "careers_url": "https://careers.cognizant.com",
            "description": "Professional services and IT solutions company.",
            "categories": ["IT Services", "Digital"],
            "industry": "IT Services"
        }
    ]
}

# Flattened cache for fast lookup
ALL_COMPANIES: List[Dict] = [
    company
    for category in FEATURED_COMPANIES.values()
    for company in category
]

COMPANY_LOOKUP = {
    company["name"].lower(): company
    for company in ALL_COMPANIES
}

# =====================================================
# JOB MARKET INSIGHTS
# =====================================================

JOB_MARKET_INSIGHTS = {
    "trending_skills": [
        {"name": "Artificial Intelligence", "growth": "+45%"},
        {"name": "Cloud Computing", "growth": "+38%"},
        {"name": "Data Science", "growth": "+35%"},
        {"name": "Cybersecurity", "growth": "+32%"},
        {"name": "DevOps", "growth": "+30%"},
    ],
    "top_locations": [
        {"name": "Bangalore", "jobs": "50,000+"},
        {"name": "Hyderabad", "jobs": "25,000+"},
        {"name": "Pune", "jobs": "20,000+"},
        {"name": "Remote", "jobs": "Growing Fast"},
    ],
    "salary_insights": [
        {"role": "Machine Learning Engineer", "range": "10-35 LPA"},
        {"role": "Software Engineer", "range": "5-25 LPA"},
        {"role": "Data Scientist", "range": "8-30 LPA"},
        {"role": "Cloud Engineer", "range": "6-26 LPA"},
    ]
}

# =====================================================
# HELPER FUNCTIONS (FAST + SAFE)
# =====================================================

def get_featured_companies(category: Optional[str] = None) -> List[Dict]:
    """Return companies filtered by category."""
    if category:
        return FEATURED_COMPANIES.get(category, [])
    return ALL_COMPANIES


def get_company_info(company_name: str) -> Optional[Dict]:
    """O(1) lookup — extremely fast."""
    return COMPANY_LOOKUP.get(company_name.lower())


def get_companies_by_industry(industry: str) -> List[Dict]:
    """Filter companies by industry."""
    return [
        company for company in ALL_COMPANIES
        if company.get("industry") == industry
    ]


def get_market_insights() -> Dict:
    """Return job market insights."""
    return JOB_MARKET_INSIGHTS