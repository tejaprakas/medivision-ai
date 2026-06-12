"""
Medical Report Model
Stores generated PDF medical reports.
"""

from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class MedicalReport(Document):
    """Medical report document model."""

    user_id: str
    patient_id: str
    analysis_id: str
    report_number: str  # e.g., "MR-2024-0001"

    # Patient snapshot
    patient_name: str
    patient_age: Optional[int] = None
    patient_gender: Optional[str] = None

    # Report content
    title: str = "Medical Analysis Report"
    image_type: str
    prediction: str
    disease_name: Optional[str] = None
    confidence_score: float = 0.0
    risk_level: str = "low"
    findings: List[str] = []
    recommendations: List[str] = []
    ai_explanation: Optional[str] = None
    doctor_notes: Optional[str] = None

    # PDF
    pdf_url: Optional[str] = None
    pdf_generated: bool = False

    # Doctor review
    reviewed_by: Optional[str] = None
    review_date: Optional[datetime] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "medical_reports"
        indexes = [
            "user_id",
            "patient_id",
            "analysis_id",
            "report_number",
            "created_at",
        ]


class ReportResponse(BaseModel):
    id: str
    report_number: str
    title: str
    image_type: str
    prediction: str
    confidence_score: float
    risk_level: str
    pdf_url: Optional[str]
    pdf_generated: bool
    created_at: datetime
