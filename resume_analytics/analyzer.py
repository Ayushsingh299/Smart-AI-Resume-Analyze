import spacy
from spacy.matcher import PhraseMatcher
from datetime import datetime
from typing import Dict, List
import logging


logging.basicConfig(level=logging.INFO)


class ResumeAnalyzer:
    """
    Production-grade Resume Analyzer.
    Optimized for speed, NLP accuracy, and scalability.
    """

    # Load model ONCE (VERY IMPORTANT)
    _nlp = None
    _matcher = None

    def __init__(self):

        if ResumeAnalyzer._nlp is None:
            logging.info("Loading spaCy model...")
            ResumeAnalyzer._nlp = spacy.load("en_core_web_sm")

        if ResumeAnalyzer._matcher is None:
            ResumeAnalyzer._matcher = self._build_matcher()

        self.nlp = ResumeAnalyzer._nlp
        self.matcher = ResumeAnalyzer._matcher

    # =====================================================
    # SKILL MATCHER (VERY POWERFUL UPGRADE)
    # =====================================================

    def _build_matcher(self):

        matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")

        tech_skills = [
            "python", "java", "javascript", "react", "node",
            "sql", "html", "css", "aws", "docker", "kubernetes",
            "git", "machine learning", "deep learning",
            "ai", "data science", "pandas", "numpy",
            "tensorflow", "pytorch", "fastapi", "django"
        ]

        patterns = [self.nlp.make_doc(skill) for skill in tech_skills]
        matcher.add("TECH_SKILLS", patterns)

        return matcher

    # =====================================================
    # MAIN ANALYSIS
    # =====================================================

    def analyze_resume(self, resume_text: str) -> Dict:

        if not resume_text.strip():
            raise ValueError("Resume text cannot be empty.")

        doc = self.nlp(resume_text)

        word_count = len(doc)
        sentence_count = len(list(doc.sents))

        skills = self._extract_skills(doc)
        experience_years = self._extract_experience(doc)

        profile_score = self._calculate_score(
            word_count,
            skills,
            experience_years
        )

        return {
            "timestamp": datetime.utcnow().isoformat(),

            "metrics": {
                "word_count": word_count,
                "sentence_count": sentence_count,
                "skills_count": len(skills),
                "experience_years": experience_years,
                "profile_score": profile_score
            },

            "skills": skills,

            "suggestions": self._generate_suggestions(
                word_count,
                sentence_count,
                skills,
                experience_years
            )
        }

    # =====================================================
    # SKILL EXTRACTION (MUCH STRONGER)
    # =====================================================

    def _extract_skills(self, doc) -> List[str]:

        matches = self.matcher(doc)

        skills = {
            doc[start:end].text.lower()
            for _, start, end in matches
        }

        return sorted(skills)

    # =====================================================
    # EXPERIENCE DETECTION (SMARTER)
    # =====================================================

    def _extract_experience(self, doc) -> int:

        years = []

        for i, token in enumerate(doc):

            if token.like_num and i < len(doc) - 1:

                next_token = doc[i + 1].text.lower()

                if "year" in next_token:
                    try:
                        years.append(int(token.text))
                    except:
                        continue

        return max(years) if years else 0

    # =====================================================
    # SCORING ENGINE (LOOKS LIKE REAL ATS)
    # =====================================================

    def _calculate_score(
        self,
        word_count: int,
        skills: List[str],
        experience: int
    ) -> int:

        score = 0

        # Word Count (20)
        score += min(word_count / 400 * 20, 20)

        # Skills (40)
        score += min(len(skills) / 10 * 40, 40)

        # Experience (40)
        score += min(experience / 6 * 40, 40)

        return round(score)

    # =====================================================
    # AI-LIKE SUGGESTIONS
    # =====================================================

    def _generate_suggestions(
        self,
        word_count,
        sentence_count,
        skills,
        experience
    ) -> List[Dict]:

        suggestions = []

        if word_count < 350:
            suggestions.append({
                "icon": "fa-file-text",
                "text": "Increase resume depth. Strong resumes are typically 400–700 words."
            })

        if len(skills) < 6:
            suggestions.append({
                "icon": "fa-code",
                "text": "Add more industry-relevant technical skills to improve ATS ranking."
            })

        if experience < 2:
            suggestions.append({
                "icon": "fa-briefcase",
                "text": "Highlight internships, projects, or freelance work to demonstrate experience."
            })

        if sentence_count < 8:
            suggestions.append({
                "icon": "fa-list",
                "text": "Use bullet points to describe achievements clearly."
            })

        if not suggestions:
            suggestions.append({
                "icon": "fa-star",
                "text": "Excellent resume! Consider adding measurable achievements (e.g., improved performance by 30%)."
            })

        return suggestions
        