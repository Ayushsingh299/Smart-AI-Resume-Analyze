# 🚀 Smart AI Resume Analyzer

<p align="center">
<img src="https://img.shields.io/github/stars/Ayushsingh299/Smart-AI-Resume-Analyze?style=for-the-badge"/>
<img src="https://img.shields.io/github/forks/Ayushsingh299/Smart-AI-Resume-Analyze?style=for-the-badge"/>
<img src="https://img.shields.io/github/license/Ayushsingh299/Smart-AI-Resume-Analyze?style=for-the-badge"/>
<img src="https://img.shields.io/github/last-commit/Ayushsingh299/Smart-AI-Resume-Analyze?style=for-the-badge"/>
</p>

> 💡 **Smart AI Resume Analyzer** is an advanced AI-powered platform designed to analyze, optimize, and enhance resumes using Natural Language Processing and Machine Learning — helping candidates significantly improve their chances of getting shortlisted.

🌐 **Live Demo:** https://smart-ai-resume-analyzer.streamlit.app/
📄 **AI Documentation:** AI_MODELS.md
🤝 **Contributions:** Pull Requests Welcome

---

# 🌍 Problem Statement

Modern hiring heavily relies on **Applicant Tracking Systems (ATS)** to filter candidates before a human recruiter even views the resume.

Unfortunately, many qualified candidates get rejected due to:

* Missing role-specific keywords
* Poor formatting
* Weak resume structure
* Lack of measurable achievements

### ✅ Solution

Smart AI Resume Analyzer bridges this gap by delivering **AI-driven insights, ATS scoring, and structured optimization recommendations** — transforming resumes into recruiter-ready professional profiles.

---

# ✨ Key Features

## 🔍 AI Resume Analysis

* ATS Compatibility Score
* Keyword Gap Detection
* Skills Analysis
* Role-Based Recommendations
* AI-Powered Resume Scoring

## 🎨 Intelligent Resume Builder

* Modern, Minimal, Professional, and Creative templates
* Smart content suggestions
* ATS-friendly formatting
* Fully customizable sections

## 🤖 AI Optimization Engine

* Google Gemini integration
* Content enhancement suggestions
* Industry-specific insights
* AI-generated PDF reports

## 🔎 Advanced Job Search

* LinkedIn job scraper
* Customizable job search
* Market insights

---

# 🏗️ System Architecture

```
User → Streamlit UI → Resume Parser → NLP Engine (spaCy + ML)
→ AI Processing (Google Gemini) → SQLite Database
→ Analytics Dashboard → Recommendations
```

Designed with a **modular and scalable architecture** to support future AI integrations.

---

# ⚡ Performance Highlights

* 🚀 Resume analysis in seconds
* 📄 Supports PDF & DOCX parsing
* 🧠 Optimized NLP pipeline
* ☁️ Cloud deployment ready
* 🔌 Expandable AI model support

---

# 🏷️ Version Overview

## 🔹 Version 1.0 – Rule-Based Analyzer

* Keyword Matching
* ATS Compatibility Score
* Role-Based Feedback
* Resume Insights

## 🔹 Version 2.0 – AI-Powered Analyzer (Testing Phase)

* Google Gemini Integration
* AI Resume Score
* PDF Report Generation
* AI Keyword Optimization
* LinkedIn Job Scraper

🔥 Continuous improvements are being made to enhance analysis accuracy and user experience.

---

# 🛠️ Tech Stack

## 🌐 Frontend

* Streamlit
* HTML
* CSS
* JavaScript

## ⚙️ Backend

* Python
* Streamlit

## 🧠 AI / NLP

* Google Gemini
* spaCy
* NLTK
* Scikit-learn

## 🗄️ Database

* SQLite3

## 📊 Visualization & Utilities

* Plotly
* OpenPyXL
* Python-docx
* PyPDF2

---

# ⚙️ Installation Guide

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Ayushsingh299/Smart-AI-Resume-Analyze.git
cd Smart-AI-Resume-Analyze
```

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

**Windows**

```
venv\Scripts\activate
```

**Mac/Linux**

```
source venv/bin/activate
```

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 4️⃣ Download spaCy Model

```bash
python -m spacy download en_core_web_sm
```

## 5️⃣ Run Application

```bash
streamlit run app.py
```

🎉 Your application should now be running locally!

---

# 🔐 Security & Best Practices

* Environment variables used for API keys
* Sensitive files excluded via `.gitignore`
* Secure authentication flow
* SQL-safe database operations
* Modular architecture

⚠️ **Admin credentials are securely configured and not publicly exposed.**

---

# 🐞 Known Issue

### Autofill Bug in Resume Builder

Browsers sometimes autofill the email field without triggering validation.

✅ **Quick Fix:**
Simply edit one character and retype it — the issue resolves instantly.

A permanent fix is in progress.

---

# 🎯 Why Choose Smart AI Resume Analyzer?

✔ Tailored role-based recommendations
✔ Professional resume templates
✔ AI-powered insights
✔ Saves hours of manual editing
✔ Improves interview chances

Built to function like a **career intelligence platform**, not just a resume tool.

---

# 👨‍💻 Maintainer

**Ayush Singh**
🔗 https://github.com/Ayushsingh299

Passionate about building intelligent systems that solve real-world problems using AI and scalable software architecture.

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to your branch
5. Open a Pull Request

---

# 📄 License

This project is licensed under the **MIT License**.

---

# ⭐ Support the Project

If you found this project helpful:

✅ Star the repository
✅ Share it with others
✅ Contribute improvements

Your support helps grow this project 🚀

---

> 💡 *“Great software is built to solve problems. Exceptional software creates opportunities.”*
