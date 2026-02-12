from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

Base = declarative_base()


# ---------------- MODELS ---------------- #

class Resume(Base):
    __tablename__ = 'resumes'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(100))
    job_role = Column(String(100))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime,
                        default=datetime.datetime.utcnow,
                        onupdate=datetime.datetime.utcnow)


class Analysis(Base):
    __tablename__ = 'analyses'

    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer)
    analysis_data = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


# ---------------- DATABASE MANAGER ---------------- #

class DatabaseManager:

    def __init__(self, db_path="resume_data.db"):
        self.engine = create_engine(
            f"sqlite:///{db_path}",
            connect_args={"check_same_thread": False}  # important for Streamlit
        )

        self.SessionLocal = sessionmaker(bind=self.engine)

        Base.metadata.create_all(self.engine)

    # ✅ Session per request
    def get_session(self):
        return self.SessionLocal()

    # ---------- Resume ---------- #

    def save_resume(self, user_id, job_role, content):
        session = self.get_session()

        try:
            resume = Resume(
                user_id=user_id,
                job_role=job_role,
                content=content
            )

            session.add(resume)
            session.commit()
            session.refresh(resume)

            return resume.id

        finally:
            session.close()

    def get_resume(self, resume_id):
        session = self.get_session()
        try:
            return session.query(Resume).filter_by(id=resume_id).first()
        finally:
            session.close()

    def get_user_resumes(self, user_id):
        session = self.get_session()
        try:
            return session.query(Resume).filter_by(user_id=user_id).all()
        finally:
            session.close()

    # ---------- Analysis ---------- #

    def save_analysis(self, resume_id, analysis_data):
        session = self.get_session()

        try:
            analysis = Analysis(
                resume_id=resume_id,
                analysis_data=analysis_data
            )

            session.add(analysis)
            session.commit()
            session.refresh(analysis)

            return analysis.id

        finally:
            session.close()

    def get_analysis(self, analysis_id):
        session = self.get_session()
        try:
            return session.query(Analysis).filter_by(id=analysis_id).first()
        finally:
            session.close()

    def get_resume_analyses(self, resume_id):
        session = self.get_session()
        try:
            return session.query(Analysis).filter_by(resume_id=resume_id).all()
        finally:
            session.close()