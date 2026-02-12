import pandas as pd
import logging
from datetime import datetime


class ExcelManager:
    """
    Handles exporting resume data to Excel.
    Excel should be used for reporting/export,
    NOT as primary database storage.
    """

    def __init__(self, file_name="resume_export.xlsx"):
        self.file_name = file_name

    def save_resume_data(self, user_id, job_role, content, analysis_data=None):
        """
        Append resume data to Excel file.
        Creates file if it does not exist.
        """
        try:
            # Load existing file if present
            try:
                df = pd.read_excel(self.file_name)
            except FileNotFoundError:
                df = pd.DataFrame()

            # New row
            new_row = {
                "user_id": user_id,
                "job_role": job_role,
                "content": content,
                "analysis_data": str(analysis_data) if analysis_data else None,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            # Append row
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

            # Save file
            df.to_excel(self.file_name, index=False)

            return True

        except Exception as e:
            logging.error("Excel save failed: %s", e)
            return False

    def get_all_resumes(self):
        """
        Return all resume records from Excel.
        """
        try:
            return pd.read_excel(self.file_name)
        except FileNotFoundError:
            return pd.DataFrame()

    def get_user_resumes(self, user_id):
        """
        Filter resumes by user_id.
        """
        df = self.get_all_resumes()
        if df.empty:
            return df
        return df[df["user_id"] == user_id]