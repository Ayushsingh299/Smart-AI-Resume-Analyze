import PyPDF2
import docx
import re
from io import BytesIO


class ResumeParser:
    def __init__(self):
        # Expanded technical skills list
        self.skill_keywords = [
            "python", "java", "javascript", "html", "css", "sql",
            "react", "angular", "vue", "node", "express",
            "django", "flask", "spring", "docker", "kubernetes",
            "aws", "azure", "gcp", "git", "jenkins", "jira",
            "machine learning", "data science", "tensorflow",
            "pandas", "numpy", "power bi", "tableau"
        ]

    # ==============================
    # TEXT EXTRACTION
    # ==============================

    def extract_text_from_pdf(self, pdf_file):
        try:
            reader = PyPDF2.PdfReader(BytesIO(pdf_file.read()))
            text = ""
            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"PDF Extraction Error: {str(e)}")

    def extract_text_from_docx(self, docx_file):
        try:
            document = docx.Document(BytesIO(docx_file.read()))
            text = "\n".join([para.text for para in document.paragraphs])
            return text.strip()
        except Exception as e:
            raise Exception(f"DOCX Extraction Error: {str(e)}")

    def extract_text(self, file):
        filename = file.name.lower()
        file.seek(0)

        if filename.endswith(".pdf"):
            return self.extract_text_from_pdf(file)
        elif filename.endswith(".docx"):
            return self.extract_text_from_docx(file)
        else:
            raise Exception("Unsupported file format. Only PDF and DOCX allowed.")

    # ==============================
    # SECTION EXTRACTION
    # ==============================

    def extract_section(self, text, section_name):
        pattern = rf"{section_name}.*?(?=\n[A-Z ]{{3,}}|\Z)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        return match.group(0).strip() if match else ""

    # ==============================
    # SKILL EXTRACTION
    # ==============================

    def extract_skills(self, text):
        text_lower = text.lower()
        found_skills = []

        for skill in self.skill_keywords:
            pattern = rf"\b{re.escape(skill)}\b"
            if re.search(pattern, text_lower):
                found_skills.append(skill)

        return list(set(found_skills))

    # ==============================
    # BASIC INFO EXTRACTION
    # ==============================

    def extract_email(self, text):
        match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        return match.group(0) if match else ""

    def extract_phone(self, text):
        match = re.search(r'(\+\d{1,3}[-.\s]?)?\d{10}', text)
        return match.group(0) if match else ""

    # ==============================
    # MAIN PARSER
    # ==============================

    def parse(self, file):
        text = self.extract_text(file)

        skills = self.extract_skills(text)
        experience = self.extract_section(text, "experience")
        education = self.extract_section(text, "education")

        email = self.extract_email(text)
        phone = self.extract_phone(text)

        return {
            "email": email,
            "phone": phone,
            "skills": skills,
            "experience": experience,
            "education": education,
            "raw_text": text
        }
        