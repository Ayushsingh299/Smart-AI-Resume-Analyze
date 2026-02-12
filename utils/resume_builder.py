import streamlit as st
from utils.resume_analyzer import ResumeAnalyzer
from utils.resume_builder import ResumeBuilder

analyzer = ResumeAnalyzer()
builder = ResumeBuilder()

st.title("🚀 Smart AI Resume Optimizer")

# Upload Resume
uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])

job_skills = st.text_input(
    "Enter required skills (comma separated)",
    placeholder="Python, SQL, Machine Learning"
)

if uploaded_file:

    # Extract text
    if uploaded_file.name.endswith(".pdf"):
        text = analyzer.extract_text_from_pdf(uploaded_file)
    else:
        text = analyzer.extract_text_from_docx(uploaded_file)

    required_skills = [skill.strip() for skill in job_skills.split(",") if skill]

    resume_data = {"raw_text": text}
    job_req = {"required_skills": required_skills}

    result = analyzer.analyze_resume(resume_data, job_req)

    st.subheader("📊 ATS Score")

    score = result["ats_score"]

    # Color logic
    if score >= 80:
        st.success(f"🔥 Excellent ATS Score: {score}%")
    elif score >= 60:
        st.warning(f"⚠️ Moderate ATS Score: {score}%")
    else:
        st.error(f"❌ Low ATS Score: {score}%")

    # Skill Match
    st.subheader("🎯 Skill Match")

    st.write("✅ Found Skills:")
    st.write(result["keyword_match"]["found_skills"])

    st.write("❌ Missing Skills:")
    st.write(result["keyword_match"]["missing_skills"])

    # Suggestions
    st.subheader("💡 AI Suggestions")

    for tip in result["suggestions"]:
        st.write("👉", tip)

    st.divider()

    # 🚀 IMPROVE BUTTON
    if score < 75:
        st.warning("Your resume can be improved before downloading!")

    if st.button("🚀 Generate Optimized Resume"):

        structured_data = {
            "template": "Professional",
            "personal_info": {
                "full_name": result.get("name", "Your Name"),
                "email": result.get("email", ""),
                "phone": result.get("phone", ""),
                "linkedin": result.get("linkedin", ""),
                "location": "",
                "title": ""
            },
            "summary": result.get("summary", ""),
            "experience": [],
            "education": [],
            "projects": [],
            "skills": {
                "technical": result.get("skills", [])
            }
        }

        resume_file = builder.generate_resume(structured_data)

        st.download_button(
            label="📥 Download Optimized Resume",
            data=resume_file,
            file_name="Optimized_Resume.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )