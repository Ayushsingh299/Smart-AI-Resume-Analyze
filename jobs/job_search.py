import streamlit as st
from typing import List, Dict
from .job_portals import JobPortal
from .suggestions import (
    JOB_SUGGESTIONS,
    LOCATION_SUGGESTIONS,
)
from .companies import get_featured_companies, get_market_insights


# =====================================================
# GLOBAL STYLES (LOAD ONCE)
# =====================================================

@st.cache_resource
def load_global_styles():
    st.markdown("""
        <style>

        .company-card {
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 1rem;
            transition: 0.2s;
        }

        .company-card:hover {
            transform: translateY(-6px);
            background: rgba(255,255,255,0.08);
        }

        .insight-card {
            background: rgba(255,255,255,0.05);
            padding: 1rem;
            border-radius: 10px;
            text-align:center;
        }

        .job-result {
            padding: 12px;
            margin: 8px 0;
            border-radius: 8px;
            background: rgba(255,255,255,0.05);
        }

        </style>
    """, unsafe_allow_html=True)


# =====================================================
# CACHE HEAVY OBJECTS
# =====================================================

@st.cache_resource
def get_job_portal():
    return JobPortal()


@st.cache_data
def filter_suggestions(query: str, suggestions: List[Dict]) -> List[str]:
    """Fast cached suggestion filtering."""

    if not query:
        return []

    q = query.lower().strip()

    return [
        s["text"] for s in suggestions
        if q in s["text"].lower()
    ][:5]


# =====================================================
# CONSTANT FILTER OPTIONS
# =====================================================

FILTER_OPTIONS = {
    "experience_levels": [
        {"id": "all", "text": "All Levels"},
        {"id": "0-1", "text": "0-1 years"},
        {"id": "1-3", "text": "1-3 years"},
        {"id": "3-5", "text": "3-5 years"},
        {"id": "5-7", "text": "5-7 years"},
        {"id": "7-10", "text": "7-10 years"},
        {"id": "10+", "text": "10+ years"}
    ]
}


# =====================================================
# MARKET INSIGHTS
# =====================================================

def render_market_insights():
    insights = get_market_insights()

    st.subheader("📊 Job Market Insights")

    tabs = st.tabs(["Trending Skills", "Top Locations"])

    with tabs[0]:
        cols = st.columns(3)
        for i, skill in enumerate(insights["trending_skills"][:6]):
            cols[i % 3].markdown(f"""
                <div class="insight-card">
                    <h4>{skill['name']}</h4>
                    <p style="color:#00c853;">Growth: {skill['growth']}</p>
                </div>
            """, unsafe_allow_html=True)

    with tabs[1]:
        cols = st.columns(3)
        for i, loc in enumerate(insights["top_locations"][:6]):
            cols[i % 3].markdown(f"""
                <div class="insight-card">
                    <h4>{loc['name']}</h4>
                    <p>{loc['jobs']} jobs</p>
                </div>
            """, unsafe_allow_html=True)


# =====================================================
# FEATURED COMPANIES
# =====================================================

def render_company_section():

    st.subheader("🏢 Featured Companies")

    tabs = st.tabs(["All", "Tech", "Indian", "Global"])

    categories = [None, "tech", "indian_tech", "global_corps"]

    for tab, category in zip(tabs, categories):
        with tab:

            companies = get_featured_companies(category)

            cols = st.columns(3)

            for i, company in enumerate(companies):
                cols[i % 3].markdown(f"""
                    <a href="{company['careers_url']}" target="_blank"
                       style="text-decoration:none;color:inherit;">
                        <div class="company-card">
                            <h4>{company['name']}</h4>
                            <p style="font-size:0.9rem;color:#aaa;">
                                {company['description']}
                            </p>
                        </div>
                    </a>
                """, unsafe_allow_html=True)


# =====================================================
# MAIN JOB SEARCH PAGE
# =====================================================

def render_job_search():

    load_global_styles()

    st.title("🔍 Smart Job Search")
    st.caption("Search jobs across multiple platforms instantly.")

    # Market insights first (product thinking)
    render_market_insights()

    st.divider()

    # FORM (prevents rerun chaos)
    with st.form("job_search_form"):

        col1, col2 = st.columns(2)

        with col1:
            job_query = st.text_input(
                "Job Title / Skills",
                placeholder="Software Engineer, Data Scientist..."
            )

            suggestions = filter_suggestions(job_query, JOB_SUGGESTIONS)

            if suggestions:
                job_query = st.selectbox("Suggestions", suggestions)

        with col2:
            location = st.text_input(
                "Location",
                placeholder="Bangalore, Remote..."
            )

            loc_suggestions = filter_suggestions(location, LOCATION_SUGGESTIONS)

            if loc_suggestions:
                location = st.selectbox("Locations", loc_suggestions)

        experience = st.selectbox(
            "Experience Level",
            options=FILTER_OPTIONS["experience_levels"],
            format_func=lambda x: x["text"]
        )

        submitted = st.form_submit_button("🚀 SEARCH JOBS")

    # SEARCH EXECUTION
    if submitted:

        if not job_query:
            st.warning("Please enter a job title.")
            return

        portal = get_job_portal()

        with st.spinner("Searching across job portals..."):

            results = portal.search_jobs(
                job_query,
                location,
                experience
            )

        st.success(f"Found {len(results)} job portals.")

        for result in results:
            st.markdown(f"""
                <div class="job-result">
                    <h4>
                        <i class="{result['icon']}"
                           style="color:{result['color']}"></i>
                        {result['portal']}
                    </h4>

                    <p>{result['title']}</p>

                    <a href="{result['url']}"
                       target="_blank"
                       style="color:#00bfa5;">
                        View Jobs →
                    </a>
                </div>
            """, unsafe_allow_html=True)

    st.divider()

    render_company_section()