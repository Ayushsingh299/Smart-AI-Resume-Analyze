import streamlit as st
import sqlite3
import os
import logging
import pandas as pd

# ==============================
# CONFIGURATION
# ==============================

st.set_page_config(
    page_title="Smart Resume AI - Feedback System",
    page_icon="⭐",
    layout="wide"
)

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ==============================
# FEEDBACK MANAGER
# ==============================

class FeedbackManager:
    def __init__(self):
        self.db_path = "feedback/feedback.db"
        os.makedirs("feedback", exist_ok=True)
        self.setup_database()

    def get_connection(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    # ✅ NOW LOADING schema.sql
    def setup_database(self):
        try:
            with self.get_connection() as conn:
                with open("schema.sql", "r") as f:
                    conn.executescript(f.read())

            logging.info("Database initialized using schema.sql")

        except Exception as e:
            logging.error(f"Schema load error: {e}")

    def save_feedback(self, data):
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT INTO feedback (
                        rating, usability_score, feature_satisfaction,
                        missing_features, improvement_suggestions,
                        user_experience
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    data['rating'],
                    data['usability_score'],
                    data['feature_satisfaction'],
                    data['missing_features'],
                    data['improvement_suggestions'],
                    data['user_experience']
                ))

            logging.info("Feedback saved successfully")

        except Exception as e:
            logging.error(f"Save error: {e}")
            raise e

    @st.cache_data
    def get_feedback_dataframe(self):
        with self.get_connection() as conn:
            return pd.read_sql_query("SELECT * FROM feedback", conn)


# ==============================
# UI
# ==============================

def render_feedback_form(manager):
    st.title("📝 Share Your Feedback")

    col1, col2, col3 = st.columns(3)

    rating = col1.slider("Overall Rating", 1, 5, 5)
    usability = col2.slider("Usability Score", 1, 5, 5)
    satisfaction = col3.slider("Feature Satisfaction", 1, 5, 5)

    missing_features = st.text_area("Missing Features")
    improvement = st.text_area("Improvement Suggestions")
    experience = st.text_area("User Experience")

    if st.button("Submit Feedback"):

        feedback_data = {
            "rating": rating,
            "usability_score": usability,
            "feature_satisfaction": satisfaction,
            "missing_features": missing_features,
            "improvement_suggestions": improvement,
            "user_experience": experience
        }

        try:
            with st.spinner("Saving feedback securely..."):
                manager.save_feedback(feedback_data)

            st.success("Feedback submitted successfully!")
            st.balloons()

        except Exception:
            st.error("Error saving feedback.")


def render_dashboard(manager):
    st.header("📊 Feedback Analytics Dashboard")

    df = manager.get_feedback_dataframe()

    if df.empty:
        st.info("No feedback data available yet.")
        return

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Responses", len(df))
    col2.metric("Average Rating", round(df['rating'].mean(), 2))
    col3.metric("Usability Score", round(df['usability_score'].mean(), 2))
    col4.metric("Feature Satisfaction", round(df['feature_satisfaction'].mean(), 2))

    st.divider()

    st.subheader("Rating Distribution")
    st.bar_chart(df['rating'].value_counts().sort_index())

    st.subheader("Usability Distribution")
    st.bar_chart(df['usability_score'].value_counts().sort_index())

    st.subheader("Satisfaction Distribution")
    st.bar_chart(df['feature_satisfaction'].value_counts().sort_index())

    # ✅ ADMIN MODE (Your edited version improved)
    if st.sidebar.checkbox("Admin Mode"):
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "feedback_data.csv", "text/csv")


# ==============================
# MAIN
# ==============================

def main():
    manager = FeedbackManager()

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Feedback Form", "Dashboard"])

    if page == "Feedback Form":
        render_feedback_form(manager)
    else:
        render_dashboard(manager)


if __name__ == "__main__":
    main()