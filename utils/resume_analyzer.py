import re
from typing import Dict, List


class ResumeAnalyzer:
    """
    Smart Resume Analyzer
    Detects document type, extracts sections,
    calculates ATS score, and generates suggestions.
    """

    def __init__(self):

        self.document_types = {
            "resume": ["experience", "education", "skills", "project"],
            "marksheet": ["cgpa", "semester", "grade"],
            "certificate": ["certificate", "completed", "training"],
            "id_card": ["id", "identity", "valid until"]
        }

        self.section_keywords = {
            "education": ["education", "university", "college", "degree"],
            "experience": ["experience", "employment", "internship"],
            "skills": ["skills", "technologies", "tools"],
            "projects": ["projects", "academic projects"]
        }

    # ===================================
    # DOCUMENT TYPE DETECTION
    # ===================================

    def detect_document_type(self, text: str) -> str:
        text = text.lower()

        scores = {
            doc: sum(keyword in text for keyword in keywords)
            for doc, keywords in self.document_types.items()
        }

        best = max(scores, key=scores.get)

        return best if scores[best] >= 2 else "unknown"

    # ===================================
    # PERSONAL INFO
    # ===================================

    def extract_personal_info(self, text: str) -> Dict:

        patterns = {
            "email": r'[\w\.-]+@[\w\.-]+\.\w+',
            "phone": r'(\+\d{1,3}[-.]?)?\d{10}',
            "linkedin": r'linkedin\.com/in/[\w-]+',
            "github": r'github\.com/[\w-]+'
        }

        info = {
            key: (re.search(pattern, text).group(0)
                  if re.search(pattern, text) else "")
            for key, pattern in patterns.items()
        }

        info["name"] = text.split("\n")[0].strip() if text else "Unknown"

        return info

    # ===================================
    # SECTION CHECKER
    # ===================================

    def section_score(self, text: str) -> int:

        text = text.lower()

        score = 0

        for keywords in self.section_keywords.values():
            if any(k in text for k in keywords):
                score += 25

        return score

    # ===================================
    # SKILL MATCH
    # ===================================

    def keyword_match(self, text: str, required_skills: List[str]) -> Dict:

        text = text.lower()

        found = [skill for skill in required_skills if skill.lower() in text]
        missing = [skill for skill in required_skills if skill not in found]

        score = int((len(found) / len(required_skills)) * 100) if required_skills else 0

        return {
            "score": score,
            "found_skills": found,
            "missing_skills": missing
        }

    # ===================================
    # FORMATTING CHECK
    # ===================================

    def formatting_score(self, text: str):

        score = 100
        issues = []

        if len(text) < 300:
            score -= 25
            issues.append("Resume is too short")

        if not re.search(r'[•\-\*]', text):
            score -= 15
            issues.append("Use bullet points")

        if not re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text):
            score -= 20
            issues.append("Add contact information")

        return max(score, 0), issues

    # ===================================
    # MAIN ANALYSIS
    # ===================================

    def analyze_resume(self, resume_data: Dict, job_req: Dict):

        text = resume_data.get("raw_text", "")

        doc_type = self.detect_document_type(text)

        if doc_type != "resume":
            return {
                "ats_score": 0,
                "document_type": doc_type,
                "suggestions": ["Please upload a proper resume."]
            }

        personal = self.extract_personal_info(text)

        section_score = self.section_score(text)

        keyword = self.keyword_match(
            text,
            job_req.get("required_skills", [])
        )

        format_score, format_issues = self.formatting_score(text)

        ats_score = int(
            section_score * 0.3 +
            keyword["score"] * 0.4 +
            format_score * 0.3
        )

        suggestions = format_issues.copy()

        if keyword["score"] < 70:
            suggestions.append("Add more job-relevant skills")

        if section_score < 75:
            suggestions.append("Include all major sections")

        if not suggestions:
            suggestions.append("Excellent ATS-ready resume!")

        return {
            **personal,
            "document_type": "resume",
            "ats_score": ats_score,
            "keyword_match": keyword,
            "section_score": section_score,
            "format_score": format_score,
            "suggestions": suggestions
        }