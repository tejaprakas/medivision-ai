"""
Analysis Result Model
Stores AI analysis results for medical images.
"""

from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class ImageType(str, Enum):
    ECG = "ecg"
    MRI = "mri"
    CT_SCAN = "ct_scan"
    X_RAY = "x_ray"


class RiskLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class AnalysisResult(Document):
    """Medical image analysis result document model."""

    user_id: str
    image_url: str
    image_type: ImageType
    original_filename: str
    file_size: int

    # AI Prediction Results
    prediction: str  # "Disease Detected" or "No Disease Detected"
    disease_name: Optional[str] = None
    confidence_score: float = 0.0  # 0-1
    risk_level: RiskLevel = RiskLevel.LOW
    risk_score: float = 0.0  # 0-100

    # Model-specific results
    vit_prediction: Optional[Dict[str, Any]] = None
    resnet_prediction: Optional[Dict[str, Any]] = None
    ensemble_prediction: Optional[Dict[str, Any]] = None

    # Detailed findings
    detected_patterns: List[str] = []
    findings: List[str] = []
    recommendations: List[str] = []

    # AI Explanation
    ai_explanation: Optional[str] = None

    # Status
    status: str = "completed"  # pending, processing, completed, failed
    processing_time_ms: Optional[int] = None
    error_message: Optional[str] = None

    # Doctor review
    doctor_reviewed: bool = False
    doctor_id: Optional[str] = None
    doctor_notes: Optional[str] = None

    # Report
    report_generated: bool = False
    report_id: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "analysis_results"
        indexes = [
            "user_id",
            "image_type",
            "risk_level",
            "status",
            "created_at",
        ]


class AnalysisCreateResponse(BaseModel):
    id: str
    status: str
    message: str = "Analysis started successfully"


class AnalysisDetailResponse(BaseModel):
    id: str
    user_id: str
    image_url: str
    image_type: str
    original_filename: str
    prediction: str
    disease_name: Optional[str]
    confidence_score: float
    risk_level: str
    risk_score: float
    detected_patterns: List[str]
    findings: List[str]
    recommendations: List[str]
    ai_explanation: Optional[str]
    status: str
    processing_time_ms: Optional[int]
    doctor_reviewed: bool
    doctor_notes: Optional[str]
    report_generated: bool
    created_at: datetime


class AnalysisListResponse(BaseModel):
    id: str
    image_type: str
    prediction: str
    confidence_score: float
    risk_level: str
    status: str
    created_at: datetime
