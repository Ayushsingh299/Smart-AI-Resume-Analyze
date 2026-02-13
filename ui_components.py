import streamlit as st


# ==============================
# GLOBAL STYLE FUNCTIONS
# ==============================
def apply_modern_styles():
    """Styles are loaded from style.css in app.py"""
    pass


# ==============================
# HEADERS
# ==============================
def page_header(title, subtitle=None):
    st.markdown(
        f"""
# {title}

{subtitle if subtitle else ""}
        """,
        unsafe_allow_html=True,
    )


def hero_section(title, subtitle=None, description=None):
    if description and not subtitle:
        subtitle = description
        description = None

    st.markdown(
        f"""
# {title}

{subtitle if subtitle else ""}

{description if description else ""}
        """,
        unsafe_allow_html=True,
    )


# ==============================
# CARDS
# ==============================
def feature_card(icon, title, description):
    st.markdown(
        f"""
### {title}

{description}
        """,
        unsafe_allow_html=True,
    )


def metric_card(label, value, delta=None, icon=None):
    icon_html = icon if icon else ""
    delta_html = f"{delta}" if delta else ""

    st.markdown(
        f"""
{icon_html}

**{label}**

{value}

{delta_html}
        """,
        unsafe_allow_html=True,
    )


def template_card(title, description, image_url=None):
    image_html = f"![{title}]({image_url})" if image_url else ""

    st.markdown(
        f"""
{image_html}

### {title}

{description}
        """,
        unsafe_allow_html=True,
    )


def feedback_card(name, feedback, rating):
    stars = "⭐" * int(rating)

    st.markdown(
        f"""
**{name}**

{stars}

{feedback}
        """,
        unsafe_allow_html=True,
    )


# ==============================
# ABOUT SECTION
# ==============================
def about_section(title, description, image_path=None, social_links=None):
    st.markdown(
        f"""
## {title}

{description}
        """,
        unsafe_allow_html=True,
    )

    if image_path:
        st.image(image_path, width=200)

    uploaded_file = st.file_uploader("Upload profile picture", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, width=200)

    if social_links:
        for platform, url in social_links.items():
            st.markdown(f"[{platform}]({url})", unsafe_allow_html=True)


# ==============================
# LOADING / ALERTS
# ==============================
def loading_spinner(message="Loading..."):
    st.markdown(
        f"""
{message}
        """,
        unsafe_allow_html=True,
    )


def alert(message, type="info"):
    icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌",
    }
    icon = icons.get(type, "ℹ️")

    st.markdown(
        f"""
{icon} {message}
        """,
        unsafe_allow_html=True,
    )


# ==============================
# PROGRESS BAR
# ==============================
def progress_bar(value, max_value, label=None):
    if max_value == 0:
        percentage = 0
    else:
        percentage = (value / max_value) * 100

    if label:
        st.markdown(f"**{label}**", unsafe_allow_html=True)

    st.progress(min(max(int(percentage), 0), 100))
    st.markdown(f"{percentage:.1f}%", unsafe_allow_html=True)


# ==============================
# TABLE
# ==============================
def data_table(data, headers):
    st.table([dict(zip(headers, row)) for row in data])
