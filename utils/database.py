import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from config.database import get_database_connection
from plotly.subplots import make_subplots


class DashboardManager:
    def __init__(self):
        self.conn = get_database_connection()
        self.colors = {
            "primary": "#4CAF50",
            "secondary": "#2196F3",
            "warning": "#FFA726",
            "danger": "#F44336",
            "info": "#00BCD4",
            "success": "#66BB6A",
            "purple": "#9C27B0",
            "background": "#1E1E1E",
            "card": "#2D2D2D",
            "text": "#FFFFFF",
            "subtext": "#B0B0B0",
        }

    def apply_dashboard_style(self):
        """Apply custom styling for dashboard"""
        st.markdown(
            """
            <style>
                .dashboard-title {
                    font-size: 2.5rem;
                    font-weight: bold;
                    margin-bottom: 2rem;
                    color: white;
                    text-align: center;
                }

                .metric-card {
                    background-color: #2D2D2D;
                    border-radius: 15px;
                    padding: 1.5rem;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    transition: transform 0.3s ease;
                    height: 100%;
                }

                .metric-card:hover {
                    transform: translateY(-5px);
                }

                .metric-value {
                    font-size: 2.5rem;
                    font-weight: bold;
                    color: #4CAF50;
                    margin: 0.5rem 0;
                }

                .metric-label {
                    font-size: 1rem;
                    color: #B0B0B0;
                }

                .trend-up {
                    color: #4CAF50;
                    font-size: 1.2rem;
                }

                .trend-down {
                    color: #F44336;
                    font-size: 1.2rem;
                }

                .chart-container {
                    background-color: #2D2D2D;
                    border-radius: 15px;
                    padding: 1.5rem;
                    margin: 1rem 0;
                }

                .section-title {
                    font-size: 1.5rem;
                    color: white;
                    margin: 2rem 0 1rem 0;
                }

                .stPlotlyChart {
                    background-color: #2D2D2D;
                    border-radius: 15px;
                    padding: 1rem;
                }

                div[data-testid="stHorizontalBlock"] > div {
                    background-color: #2D2D2D;
                    border-radius: 15px;
                    padding: 1rem;
                    margin: 0.5rem;
                }

                [data-testid="stMetricValue"] {
                    font-size: 2rem !important;
                }

                [data-testid="stMetricLabel"] {
                    font-size: 1rem !important;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

    def get_resume_metrics(self):
        """Get resume-related metrics from database"""
        cursor = self.conn.cursor()

        now = datetime.now()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start_of_week = now - timedelta(days=now.weekday())
        start_of_month = now.replace(day=1)

        metrics = {}
        for period, start_date in [
            ("Today", start_of_day),
            ("This Week", start_of_week),
            ("This Month", start_of_month),
            ("All Time", datetime(2000, 1, 1)),
        ]:
            try:
                cursor.execute(
                    """
                    SELECT 
                        COUNT(DISTINCT rd.id) as total_resumes,
                        ROUND(AVG(ra.ats_score), 1) as avg_ats_score,
                        ROUND(AVG(ra.keyword_match_score), 1) as avg_keyword_score,
                        COUNT(DISTINCT CASE WHEN ra.ats_score >= 70 THEN rd.id END) as high_scoring
                    FROM resume_data rd
                    LEFT JOIN resume_analysis ra ON rd.id = ra.resume_id
                    WHERE rd.created_at >= ?
                    """,
                    (start_date.strftime("%Y-%m-%d %H:%M:%S"),),
                )
                row = cursor.fetchone()
            except Exception:
                row = None

            if row:
                metrics[period] = {
                    "total": row[0] or 0,
                    "ats_score": row[1] or 0,
                    "keyword_score": row[2] or 0,
                    "high_scoring": row[3] or 0,
                }
            else:
                metrics[period] = {
                    "total": 0,
                    "ats_score": 0,
                    "keyword_score": 0,
                    "high_scoring": 0,
                }

        return metrics

    def get_keyword_stats(self):
        """Get keyword-level statistics (safe if table missing)"""
        query = """
        SELECT 
            rk.keyword,
            COUNT(DISTINCT rk.resume_id) as resume_count,
            ROUND(AVG(ra.keyword_match_score), 1) as avg_match_score
        FROM resume_keywords rk
        LEFT JOIN resume_analysis ra ON rk.resume_id = ra.resume_id
        GROUP BY rk.keyword
        HAVING resume_count >= 2
        ORDER BY resume_count DESC, avg_match_score DESC
        LIMIT 20
        """
        try:
            df = pd.read_sql_query(query, self.conn)
        except Exception:
            return pd.DataFrame(
                columns=["keyword", "resume_count", "avg_match_score"]
            )

        if df.empty:
            return pd.DataFrame(
                columns=["keyword", "resume_count", "avg_match_score"]
            )

        return df

    def get_job_role_stats(self):
        """Get job role statistics (safe if schema mismatch)"""
        query = """
        SELECT 
            job_role,
            COUNT(DISTINCT resume_id) as resume_count,
            ROUND(AVG(ats_score), 1) as avg_ats_score,
            ROUND(AVG(keyword_match_score), 1) as avg_keyword_score
        FROM resume_analysis
        GROUP BY job_role
        ORDER BY resume_count DESC
        """
        try:
            df = pd.read_sql_query(query, self.conn)
        except Exception:
            return pd.DataFrame(
                columns=[
                    "job_role",
                    "resume_count",
                    "avg_ats_score",
                    "avg_keyword_score",
                ]
            )

        if df.empty:
            return pd.DataFrame(
                columns=[
                    "job_role",
                    "resume_count",
                    "avg_ats_score",
                    "avg_keyword_score",
                ]
            )

        return df

    def get_recent_resumes(self, limit=10):
        """Get list of recent resumes"""
        query = """
        SELECT 
            rd.id,
            rd.candidate_name,
            rd.email,
            rd.phone,
            rd.job_role,
            rd.created_at,
            ra.ats_score,
            ra.keyword_match_score,
            ra.overall_score,
            ra.match_percentage
        FROM resume_data rd
        LEFT JOIN resume_analysis ra ON rd.id = ra.resume_id
        ORDER BY rd.created_at DESC
        LIMIT ?
        """
        try:
            df = pd.read_sql_query(query, self.conn, params=(limit,))
        except Exception:
            return pd.DataFrame(
                columns=[
                    "id",
                    "candidate_name",
                    "email",
                    "phone",
                    "job_role",
                    "created_at",
                    "ats_score",
                    "keyword_match_score",
                    "overall_score",
                    "match_percentage",
                ]
            )
        return df

    def get_trend_data(self, days=30):
        """Get time-series data for trends (safe)"""
        start_date = datetime.now() - timedelta(days=days)
        query = """
        SELECT 
            DATE(rd.created_at) as date,
            COUNT(DISTINCT rd.id) as resumes_count,
            ROUND(AVG(ra.ats_score), 1) as avg_ats_score,
            ROUND(AVG(ra.keyword_match_score), 1) as avg_keyword_score
        FROM resume_data rd
        LEFT JOIN resume_analysis ra ON rd.id = ra.resume_id
        WHERE rd.created_at >= ?
        GROUP BY DATE(rd.created_at)
        ORDER BY date
        """
        try:
            df = pd.read_sql_query(
                query,
                self.conn,
                params=(start_date.strftime("%Y-%m-%d %H:%M:%S"),),
            )
        except Exception:
            return pd.DataFrame(
                columns=[
                    "date",
                    "resumes_count",
                    "avg_ats_score",
                    "avg_keyword_score",
                ]
            )

        return df

    def render_summary_cards(self, metrics):
        """Render top summary cards"""
        st.markdown('<div class="section-title">Overview</div>', unsafe_allow_html=True)

        cols = st.columns(4)
        periods = ["Today", "This Week", "This Month", "All Time"]
        icons = ["📄", "📅", "📆", "📊"]

        for col, period, icon in zip(cols, periods, icons):
            with col:
                data = metrics.get(period, {})
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 1.1rem; color: #B0B0B0;">{period}</span>
                            <span style="font-size: 1.5rem;">{icon}</span>
                        </div>
                        <div class="metric-value">{data.get('total', 0)}</div>
                        <div class="metric-label">Resumes Analyzed</div>
                        <div style="margin-top: 1rem; display: flex; justify-content: space-between;">
                            <span style="color: #4CAF50;">
                                ATS: {data.get('ats_score', 0)}%
                            </span>
                            <span style="color: #2196F3;">
                                Keywords: {data.get('keyword_score', 0)}%
                            </span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    def render_trend_charts(self, trend_df):
        """Render trend visualizations"""
        st.markdown(
            '<div class="section-title">Resume Analysis Trends</div>',
            unsafe_allow_html=True,
        )

        if trend_df.empty:
            st.info("No trend data available yet.")
            return

        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            row_heights=[0.6, 0.4],
            vertical_spacing=0.12,
        )

        fig.add_trace(
            go.Bar(
                x=trend_df["date"],
                y=trend_df["resumes_count"],
                name="Resumes Analyzed",
                marker_color=self.colors["primary"],
            ),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=trend_df["date"],
                y=trend_df["avg_ats_score"],
                name="Avg ATS Score",
                mode="lines+markers",
                marker_color=self.colors["secondary"],
            ),
            row=2,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=trend_df["date"],
                y=trend_df["avg_keyword_score"],
                name="Avg Keyword Score",
                mode="lines+markers",
                marker_color=self.colors["warning"],
            ),
            row=2,
            col=1,
        )

        fig.update_layout(
            template="plotly_dark",
            height=600,
            margin=dict(l=40, r=40, t=40, b=40),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )

        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_yaxes(title_text="Resumes Count", row=1, col=1)
        fig.update_yaxes(title_text="Score", row=2, col=1)

        st.plotly_chart(fig, use_container_width=True)

    def render_keyword_insights(self, keyword_df):
        """Render keyword-level insights"""
        st.markdown(
            '<div class="section-title">Keyword Performance Insights</div>',
            unsafe_allow_html=True,
        )

        if keyword_df.empty:
            st.info("No keyword data available yet.")
            return

        col1, col2 = st.columns([2, 1])

        with col1:
            fig = px.bar(
                keyword_df.sort_values("resume_count", ascending=False),
                x="keyword",
                y="resume_count",
                color="avg_match_score",
                color_continuous_scale="Viridis",
                title="Top Keywords by Resume Coverage",
            )
            fig.update_layout(
                template="plotly_dark",
                xaxis_title="Keyword",
                yaxis_title="Number of Resumes",
                height=400,
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            top_keyword = keyword_df.iloc[0]
            st.markdown(
                f"""
                <div class="chart-container">
                    <h4 style="color: white;">Top Performing Keyword</h4>
                    <h2 style="color: #4CAF50;">{top_keyword['keyword']}</h2>
                    <p style="color: #B0B0B0;">
                        Appears in <b>{top_keyword['resume_count']}</b> resumes
                        with average match score of <b>{top_keyword['avg_match_score']}%</b>
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    def render_job_role_insights(self, job_role_df):
        """Render job role insights"""
        st.markdown(
            '<div class="section-title">Job Role Analysis</div>',
            unsafe_allow_html=True,
        )

        if job_role_df.empty:
            st.info("No job role data available yet.")
            return

        col1, col2 = st.columns(2)

        with col1:
            fig1 = px.bar(
                job_role_df.sort_values("resume_count", ascending=False),
                x="job_role",
                y="resume_count",
                title="Resumes by Job Role",
                color="resume_count",
                color_continuous_scale="Blues",
            )
            fig1.update_layout(
                template="plotly_dark",
                xaxis_title="Job Role",
                yaxis_title="Number of Resumes",
                height=400,
            )
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            fig2 = go.Figure()
            fig2.add_trace(
                go.Bar(
                    x=job_role_df["job_role"],
                    y=job_role_df["avg_ats_score"],
                    name="Avg ATS Score",
                    marker_color=self.colors["secondary"],
                )
            )
            fig2.add_trace(
                go.Bar(
                    x=job_role_df["job_role"],
                    y=job_role_df["avg_keyword_score"],
                    name="Avg Keyword Score",
                    marker_color=self.colors["warning"],
                )
            )
            fig2.update_layout(
                template="plotly_dark",
                barmode="group",
                title="Average Scores by Job Role",
                xaxis_title="Job Role",
                yaxis_title="Score",
                height=400,
            )
            st.plotly_chart(fig2, use_container_width=True)

    def render_recent_resumes_table(self, recent_df):
        """Render recent resumes table"""
        st.markdown(
            '<div class="section-title">Recent Resume Analyses</div>',
            unsafe_allow_html=True,
        )

        if recent_df.empty:
            st.info("No resumes analyzed yet.")
            return

        display_df = recent_df.copy()
        display_df["created_at"] = pd.to_datetime(display_df["created_at"]).dt.strftime(
            "%Y-%m-%d %H:%M"
        )
        display_df.rename(
            columns={
                "candidate_name": "Candidate",
                "job_role": "Job Role",
                "created_at": "Analyzed At",
                "ats_score": "ATS Score",
                "keyword_match_score": "Keyword Score",
                "overall_score": "Overall Score",
                "match_percentage": "Match %",
            },
            inplace=True,
        )

        st.dataframe(
            display_df[
                [
                    "Candidate",
                    "Job Role",
                    "Analyzed At",
                    "ATS Score",
                    "Keyword Score",
                    "Overall Score",
                    "Match %",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

    def render_dashboard(self):
        """Main dashboard rendering function"""
        st.markdown(
            """
            <style>
                .dashboard-container {
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                    padding: 2rem;
                    border-radius: 20px;
                    margin: -1rem -1rem 2rem -1rem;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                }
                .dashboard-title {
                    color: #4FD1C5;
                    font-size: 2.5rem;
                    margin-bottom: 0.5rem;
                    display: flex;
                    align-items: center;
                    gap: 1rem;
                }
                .dashboard-icon {
                    background: rgba(79, 209, 197, 0.2);
                    padding: 0.5rem;
                    border-radius: 12px;
                }
                .stats-grid {
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 1.5rem;
                    margin-top: 2rem;
                }
                .stat-card {
                    background: rgba(255, 255, 255, 0.05);
                    backdrop-filter: blur(10px);
                    padding: 1.5rem;
                    border-radius: 16px;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    transition: all 0.3s ease;
                }
                .stat-card:hover {
                    transform: translateY(-5px);
                    background: rgba(255, 255, 255, 0.1);
                }
                .stat-value {
                    font-size: 2.5rem;
                    font-weight: bold;
                    margin: 0;
                    color: #4FD1C5;
                }
                .stat-label {
                    font-size: 1rem;
                    color: rgba(255, 255, 255, 0.7);
                    margin: 0.5rem 0 0 0;
                }
                .chart-container {
                    background: rgba(255, 255, 255, 0.05);
                    border-radius: 16px;
                    padding: 1rem;
                    margin-bottom: 1rem;
                }
                .insights-grid {
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 1.5rem;
                    margin-top: 1rem;
                }
                .insight-card {
                    background: rgba(255, 255, 255, 0.05);
                    padding: 1.5rem;
                    border-radius: 16px;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }
                .trend-indicator {
                    display: inline-flex;
                    align-items: center;
                    padding: 0.25rem 0.5rem;
                    border-radius: 12px;
                    font-size: 0.875rem;
                    margin-left: 0.5rem;
                }
                .trend-up {
                    background: rgba(46, 204, 113, 0.2);
                    color: #2ecc71;
                }
                .trend-down {
                    background: rgba(231, 76, 60, 0.2);
                    color: #e74c3c;
                }
                @keyframes fadeInUp {
                    from {
                        opacity: 0;
                        transform: translateY(20px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
                .animate-fade-in {
                    animation: fadeInUp 0.5s ease-out forwards;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

        self.apply_dashboard_style()

        st.markdown(
            """
            <div class="dashboard-container animate-fade-in">
                <div class="dashboard-title">
                    <div class="dashboard-icon">
                        📊
                    </div>
                    <div>
                        Smart Resume Analytics Dashboard
                        <div style="font-size: 0.9rem; color: rgba(255, 255, 255, 0.7);">
                            Track resume analysis performance and insights
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        metrics = self.get_resume_metrics()
        trend_df = self.get_trend_data()
        keyword_df = self.get_keyword_stats()
        job_role_df = self.get_job_role_stats()
        recent_df = self.get_recent_resumes()

        self.render_summary_cards(metrics)
        st.markdown("<br>", unsafe_allow_html=True)

        self.render_trend_charts(trend_df)
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            self.render_keyword_insights(keyword_df)
        with col2:
            self.render_job_role_insights(job_role_df)

        st.markdown("<br>", unsafe_allow_html=True)
        self.render_recent_resumes_table(recent_df)
