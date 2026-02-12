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
        <div class="page-header">
            <h1 class="header-title">{title}</h1>
            {f'<p class="header-subtitle">{subtitle}</p>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True
    )


def hero_section(title, subtitle=None, description=None):
    if description and not subtitle:
        subtitle = description
        description = None

    st.markdown(
        f"""
        <div class="page-header hero-header">
            <h1 class="header-title">{title}</h1>
            {f'<div class="header-subtitle">{subtitle}</div>' if subtitle else ''}
            {f'<p class="header-description">{description}</p>' if description else ''}
        </div>
        """,
        unsafe_allow_html=True
    )


# ==============================
# CARDS
# ==============================

def feature_card(icon, title, description):
    st.markdown(f"""
        <div class="card feature-card">
            <div class="feature-icon">
                <i class="{icon}"></i>
            </div>
            <h3>{title}</h3>
            <p>{description}</p>
        </div>
    """, unsafe_allow_html=True)


def metric_card(label, value, delta=None, icon=None):
    icon_html = f'<i class="{icon}"></i>' if icon else ''
    delta_html = f'<div class="metric-delta">{delta}</div>' if delta else ''

    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">
                {icon_html}
                <div class="metric-label">{label}</div>
            </div>
            <div class="metric-value">{value}</div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)


def template_card(title, description, image_url=None):
    image_html = f'<img src="{image_url}" class="template-image" />' if image_url else ''

    st.markdown(f"""
        <div class="glass-card template-card">
            {image_html}
            <h3>{title}</h3>
            <p>{description}</p>
        </div>
    """, unsafe_allow_html=True)


def feedback_card(name, feedback, rating):
    stars = "⭐" * int(rating)

    st.markdown(f"""
        <div class="card feedback-card">
            <div class="feedback-header">
                <div class="feedback-name">{name}</div>
                <div class="feedback-rating">{stars}</div>
            </div>
            <p>{feedback}</p>
        </div>
    """, unsafe_allow_html=True)


# ==============================
# ABOUT SECTION (FIXED)
# ==============================

def about_section(title, description, image_path=None, social_links=None):
    st.markdown(f"""
        <div class="about-section">
            <h2>{title}</h2>
            <p class="about-description">{description}</p>
        </div>
    """, unsafe_allow_html=True)

    if image_path:
        st.image(image_path, width=200)

    uploaded_file = st.file_uploader("Upload profile picture", type=['png', 'jpg', 'jpeg'])
    if uploaded_file:
        st.image(uploaded_file, width=200)

    if social_links:
        st.markdown('<div class="social-links">', unsafe_allow_html=True)
        for platform, url in social_links.items():
            st.markdown(
                f'<a href="{url}" target="_blank"><i class="fab fa-{platform.lower()}"></i></a>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)


# ==============================
# LOADING / ALERTS
# ==============================

def loading_spinner(message="Loading..."):
    st.markdown(f"""
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <p>{message}</p>
        </div>
    """, unsafe_allow_html=True)


def alert(message, type="info"):
    icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌"
    }

    icon = icons.get(type, "ℹ️")

    st.markdown(f"""
        <div class="alert alert-{type}">
            {icon} {message}
        </div>
    """, unsafe_allow_html=True)


# ==============================
# PROGRESS BAR
# ==============================

def progress_bar(value, max_value, label=None):
    percentage = (value / max_value) * 100
    label_html = f'<div>{label}</div>' if label else ''

    st.markdown(f"""
        <div class="progress-container">
            {label_html}
            <div class="progress-bar">
                <div class="progress-fill" style="width:{percentage}%"></div>
            </div>
            <div>{percentage:.1f}%</div>
        </div>
    """, unsafe_allow_html=True)


# ==============================
# TABLE
# ==============================

def data_table(data, headers):
    header_row = "".join([f"<th>{h}</th>" for h in headers])

    rows = ""
    for row in data:
        cells = "".join([f"<td>{cell}</td>" for cell in row])
        rows += f"<tr>{cells}</tr>"

    st.markdown(f"""
        <table class="modern-table">
            <thead>
                <tr>{header_row}</tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
    """, unsafe_allow_html=True)

