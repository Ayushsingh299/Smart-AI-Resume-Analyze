import streamlit as st


def apply_modern_styles():
    """Optional global styles (already mostly handled in app.py)."""
    pass


def page_header(title, subtitle=None):
    st.markdown(f"# {title}", unsafe_allow_html=True)
    if subtitle:
        st.markdown(subtitle, unsafe_allow_html=True)


def hero_section(title, subtitle=None, description=None):
    page_header(title, subtitle or description)


def feature_card(icon, title, description):
    st.markdown(f"### {title}", unsafe_allow_html=True)
    st.markdown(description, unsafe_allow_html=True)


def about_section(title, description, image_path=None, social_links=None):
    page_header(title)
    st.markdown(description, unsafe_allow_html=True)


def render_analytics_section(analytics_data=None):
    """Placeholder to satisfy import; app already renders analytics directly."""
    if analytics_data:
        st.write("Analytics:", analytics_data)


def render_activity_section(activity_data=None):
    """Placeholder to satisfy import."""
    if activity_data:
        st.write("Recent activity:", activity_data)


def render_suggestions_section(suggestions=None):
    """Placeholder to satisfy import."""
    if suggestions:
        st.write("Suggestions:")
        for s in suggestions:
            st.write("-", s)
