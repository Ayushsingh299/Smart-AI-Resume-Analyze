    def render_about(self):
        """Render the About page"""
        apply_modern_styles()

        # Use GitHub avatar as profile image
        image_url = "https://avatars.githubusercontent.com/u/145857093?v=4"

        # About page specific styles
        st.markdown(
            """
            <style>
                .hero-section {
                    background: linear-gradient(135deg, #4CAF50 0%, #2a5298 100%);
                    padding: 2.5rem;
                    border-radius: 20px;
                    margin-bottom: 2rem;
                    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3);
                    text-align: center;
                    color: #ffffff;
                }
                .hero-title {
                    font-size: 2.4rem;
                    font-weight: 700;
                    margin-bottom: 0.75rem;
                }
                .hero-subtitle {
                    font-size: 1.05rem;
                    max-width: 700px;
                    margin: 0 auto;
                    opacity: 0.9;
                    line-height: 1.6;
                }

                .profile-section {
                    text-align: center;
                    padding: 2rem 1rem;
                    background: #1e1e1e;
                    border-radius: 20px;
                    margin-bottom: 2rem;
                    box-shadow: 0 10px 25px rgba(0,0,0,0.25);
                }
                .profile-image {
                    width: 140px;
                    height: 140px;
                    border-radius: 50%;
                    object-fit: cover;
                    border: 3px solid #4CAF50;
                    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
                    margin-bottom: 1rem;
                }
                .profile-name {
                    font-size: 1.8rem;
                    font-weight: 600;
                    color: #ffffff;
                    margin-bottom: 0.25rem;
                }
                .profile-title {
                    font-size: 1rem;
                    color: #b0b0b0;
                    margin-bottom: 1rem;
                }
                .social-links {
                    display: flex;
                    justify-content: center;
                    gap: 1rem;
                    margin-bottom: 1.25rem;
                }
                .social-link {
                    width: 40px;
                    height: 40px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: #ffffff;
                    background: rgba(255,255,255,0.06);
                    border: 1px solid rgba(255,255,255,0.12);
                    transition: all 0.25s ease;
                }
                .social-link:hover {
                    background: #4CAF50;
                    border-color: #4CAF50;
                    transform: translateY(-2px);
                }
                .bio-text {
                    max-width: 700px;
                    margin: 0 auto;
                    color: #dddddd;
                    line-height: 1.7;
                    font-size: 0.98rem;
                    text-align: center;
                }

                .vision-section {
                    background: #1e1e1e;
                    border-radius: 20px;
                    padding: 2rem;
                    margin-bottom: 2rem;
                    box-shadow: 0 10px 25px rgba(0,0,0,0.25);
                    text-align: center;
                }
                .vision-icon {
                    font-size: 2.2rem;
                    color: #ffd54f;
                    margin-bottom: 0.75rem;
                }
                .vision-title {
                    font-size: 1.6rem;
                    color: #ffffff;
                    margin-bottom: 0.75rem;
                }
                .vision-text {
                    color: #d0d0d0;
                    max-width: 800px;
                    margin: 0 auto;
                    line-height: 1.7;
                    font-size: 0.98rem;
                }

                .features-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
                    gap: 1.5rem;
                    margin: 2rem 0;
                }
                .feature-card {
                    background: #1e1e1e;
                    border-radius: 18px;
                    padding: 1.75rem;
                    box-shadow: 0 10px 25px rgba(0,0,0,0.25);
                    border: 1px solid rgba(255,255,255,0.06);
                }
                .feature-icon {
                    font-size: 1.8rem;
                    color: #4CAF50;
                    margin-bottom: 0.75rem;
                }
                .feature-title {
                    font-size: 1.2rem;
                    color: #ffffff;
                    margin-bottom: 0.5rem;
                    font-weight: 600;
                }
                .feature-description {
                    color: #cccccc;
                    line-height: 1.6;
                    font-size: 0.95rem;
                }

                .cta-button {
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    padding: 0.85rem 1.8rem;
                    border-radius: 999px;
                    background: linear-gradient(135deg, #4CAF50 0%, #2a9d8f 100%);
                    color: #ffffff !important;
                    text-decoration: none;
                    font-weight: 500;
                    border: none;
                    box-shadow: 0 10px 25px rgba(76,175,80,0.3);
                    transition: all 0.25s ease;
                    font-size: 0.98rem;
                }
                .cta-button:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 14px 30px rgba(76,175,80,0.4);
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Hero section
        st.markdown(
            """
            <div class="hero-section">
                <h1 class="hero-title">About Smart Resume AI</h1>
                <p class="hero-subtitle">
                    Smart Resume AI is a modern, AI‑powered platform that analyzes and enhances resumes 
                    to help candidates present their skills clearly, confidently, and professionally.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Profile section
        st.markdown(
            f"""
            <div class="profile-section">
                <img src="{image_url}" alt="Ayush Singh" class="profile-image">
                <h2 class="profile-name">Ayush Singh</h2>
                <p class="profile-title">
                    B.Tech Computer Science Student · Aspiring Software Engineer · Future Data Scientist
                </p>
                <div class="social-links">
                    <a href="https://github.com/Ayushsingh299" class="social-link" target="_blank">
                        <i class="fab fa-github"></i>
                    </a>
                    <a href="https://www.linkedin.com/in/ayush-singh-190163358" class="social-link" target="_blank">
                        <i class="fab fa-linkedin"></i>
                    </a>
                    <a href="mailto:ayush2043singh@gmail.com" class="social-link" target="_blank">
                        <i class="fas fa-envelope"></i>
                    </a>
                </div>
                <p class="bio-text">
                    I am a dedicated B.Tech Computer Science student with a strong interest in software development,
                    applied AI, and data‑driven solutions. I built <b>Smart Resume AI</b> to help job seekers create
                    stronger, interview‑ready resumes through clear insights instead of guesswork. I focus on writing
                    clean, maintainable code and continuously improving my skills to grow into a well‑rounded software
                    engineer and data professional.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Vision section
        st.markdown(
            """
            <div class="vision-section">
                <i class="fas fa-lightbulb vision-icon"></i>
                <h2 class="vision-title">Vision Behind Smart Resume AI</h2>
                <p class="vision-text">
                    Smart Resume AI is built with a simple goal: to make professional, high‑quality resume feedback 
                    accessible to everyone. By combining modern AI with a clean user experience, the platform helps 
                    students and professionals understand where their resumes are strong, where they can improve, 
                    and how to align better with real‑world job expectations.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Feature highlights
        st.markdown(
            """
            <div class="features-grid">
                <div class="feature-card">
                    <i class="fas fa-robot feature-icon"></i>
                    <h3 class="feature-title">AI‑Driven Evaluation</h3>
                    <p class="feature-description">
                        Analyze resumes using AI‑based checks for ATS compatibility, structure, and keyword relevance 
                        so candidates can quickly understand how their profile appears to recruiters and screening tools.
                    </p>
                </div>
                <div class="feature-card">
                    <i class="fas fa-chart-line feature-icon"></i>
                    <h3 class="feature-title">Actionable Insights</h3>
                    <p class="feature-description">
                        Transform raw feedback into clear, practical recommendations that help users refine their 
                        content, highlight impact, and present skills in a way that matches their target roles.
                    </p>
                </div>
                <div class="feature-card">
                    <i class="fas fa-shield-alt feature-icon"></i>
                    <h3 class="feature-title">User‑Focused Experience</h3>
                    <p class="feature-description">
                        Designed with simplicity and privacy in mind, Smart Resume AI offers a focused, distraction‑free
                        interface where users stay in control of their data and their career story.
                    </p>
                </div>
            </div>
            <div style="text-align: center; margin: 3rem 0;">
                <a href="?page=analyzer" class="cta-button">
                    Start Improving Your Resume
                    <i class="fas fa-arrow-right" style="margin-left: 10px;"></i>
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )
