import streamlit as st
from datetime import datetime
from config.database import get_database_connection


class FeedbackManager:
    def __init__(self):
        self.conn = get_database_connection()
        self._ensure_table()

    def _ensure_table(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
                usability_score INTEGER NOT NULL CHECK(usability_score BETWEEN 1 AND 5),
                feature_satisfaction INTEGER NOT NULL CHECK(feature_satisfaction BETWEEN 1 AND 5),
                missing_features TEXT,
                improvement_suggestions TEXT,
                user_experience TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_rating ON feedback(rating);"
        )
        self.conn.commit()

    def render_feedback_form(self):
        st.header("📣 Your Voice Matters!")
        st.write("Help us improve Smart Resume AI with your valuable feedback.")

        with st.form("feedback_form"):
            st.subheader("Overall Experience")
            rating = st.slider("Overall rating", 1, 5, 5)

            st.subheader("Product Experience")
            usability_score = st.slider("Ease of use", 1, 5, 4)
            feature_satisfaction = st.slider("Feature satisfaction", 1, 5, 4)

            st.subheader("Tell us more")
            missing_features = st.text_area(
                "What features are missing?",
                placeholder="E.g., more templates, export formats, job suggestions...",
            )
            improvement_suggestions = st.text_area(
                "How can we improve?",
                placeholder="Share any ideas or suggestions...",
            )
            user_experience = st.text_area(
                "Describe your experience",
                placeholder="What did you like or dislike?",
            )

            submitted = st.form_submit_button("Share Feedback")
            if submitted:
                self.save_feedback(
                    rating,
                    usability_score,
                    feature_satisfaction,
                    missing_features,
                    improvement_suggestions,
                    user_experience,
                )
                st.success("Thank you for your feedback! ✅")

    def save_feedback(
        self,
        rating,
        usability_score,
        feature_satisfaction,
        missing_features,
        improvement_suggestions,
        user_experience,
    ):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO feedback (
                rating,
                usability_score,
                feature_satisfaction,
                missing_features,
                improvement_suggestions,
                user_experience,
                timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                rating,
                usability_score,
                feature_satisfaction,
                missing_features,
                improvement_suggestions,
                user_experience,
                datetime.now().isoformat(),
            ),
        )
        self.conn.commit()

    def render_feedback_stats(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT 
                COUNT(*) as total,
                AVG(rating) as avg_rating,
                AVG(usability_score) as avg_usability,
                AVG(feature_satisfaction) as avg_features
            FROM feedback
            """
        )
        row = cursor.fetchone()

        total = row[0] or 0
        avg_rating = round(row[1], 1) if row[1] is not None else 0
        avg_usability = round(row[2], 1) if row[2] is not None else 0
        avg_features = round(row[3], 1) if row[3] is not None else 0

        st.subheader("Feedback Overview")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Total Feedback", total)
        with c2:
            st.metric("Overall Rating", avg_rating)
        with c3:
            st.metric("Usability", avg_usability)
        with c4:
            st.metric("Features", avg_features)

        cursor.execute(
            """
            SELECT rating, usability_score, feature_satisfaction,
                   missing_features, improvement_suggestions, user_experience, timestamp
            FROM feedback
            ORDER BY timestamp DESC
            LIMIT 20
            """
        )
        rows = cursor.fetchall()

        if not rows:
            st.info("No feedback submitted yet.")
            return

        st.markdown("### Recent Feedback")
        for (
            rating,
            usability_score,
            feature_satisfaction,
            missing_features,
            improvement_suggestions,
            user_experience,
            ts,
        ) in rows:
            st.markdown("---")
            st.markdown(f"**Rating:** ⭐ {rating}")
            st.markdown(
                f"Usability: {usability_score}/5 · Features: {feature_satisfaction}/5"
            )
            st.markdown(f"_Submitted at: {ts}_")
            if user_experience:
                st.markdown(f"**Experience:** {user_experience}")
            if missing_features:
                st.markdown(f"**Missing features:** {missing_features}")
            if improvement_suggestions:
                st.markdown(f"**Suggestions:** {improvement_suggestions}")
