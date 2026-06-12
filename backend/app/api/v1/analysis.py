"""
Medical Image Analysis API Routes
Upload images, run AI predictions, get results.
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.responses import JSONResponse
from typing import Optional
from datetime import datetime
import uuid
import os
import time
from app.core.security import get_current_user, require_patient
from app.core.database import get_database
from app.models.user import User
from app.models.analysis import AnalysisResult, AnalysisDetailResponse, AnalysisListResponse, ImageType, RiskLevel
from app.services.image_service import save_upload_file, validate_image
from app.services.analysis_service import run_analysis_pipeline
import logging

logger = logging.getLogger("medivision.analysis")
router = APIRouter()


@router.post("/upload", status_code=status.HTTP_202_ACCEPTED)
async def upload_image(
    file: UploadFile = File(...),
    image_type: str = Form(...),
    current_user: User = Depends(require_patient),
):
    """Upload a medical image for AI analysis."""
    # Validate image
    is_valid, error_msg = validate_image(file)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)

    # Validate image type
    try:
        img_type = ImageType(image_type.lower())
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid image type. Supported: {[t.value for t in ImageType]}",
        )

    # Save file
    file_id = str(uuid.uuid4())
    file_ext = os.path.splitext(file.filename)[1]
    filename = f"{file_id}{file_ext}"
    upload_dir = f"uploads/analyses/{current_user.id}"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, filename)

    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # Create analysis record
    analysis = AnalysisResult(
        user_id=str(current_user.id),
        image_url=f"/uploads/analyses/{current_user.id}/{filename}",
        image_type=img_type,
        original_filename=file.filename,
        file_size=len(content),
        status="pending",
    )
    await analysis.create()

    # Run AI analysis (async)
    # In production, this would be a Celery task
    try:
        await run_analysis_pipeline(str(analysis.id), file_path, img_type)
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        await AnalysisResult.get(analysis.id).update({"$set": {"status": "failed", "error_message": str(e)}})
        raise HTTPException(status_code=500, detail="Analysis failed. Please try again.")

    return {
        "id": str(analysis.id),
        "status": "processing",
        "message": "Image uploaded successfully. Analysis in progress.",
    }


@router.get("/results", response_model=list[AnalysisListResponse])
async def get_my_analyses(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
):
    """Get analysis results for current user."""
    db = get_database()
    query = {"user_id": str(current_user.id)}

    cursor = db.analysis_results.find(query).sort("created_at", -1).skip(skip).limit(limit)
    results = []
    async for doc in cursor:
        results.append(AnalysisListResponse(
            id=str(doc["_id"]),
            image_type=doc.get("image_type", ""),
            prediction=doc.get("prediction", ""),
            confidence_score=doc.get("confidence_score", 0),
            risk_level=doc.get("risk_level", "low"),
            status=doc.get("status", ""),
            created_at=doc.get("created_at", datetime.utcnow()),
        ))
    return results


@router.get("/results/{analysis_id}", response_model=AnalysisDetailResponse)
async def get_analysis_detail(
    analysis_id: str,
    current_user: User = Depends(get_current_user),
):
    """Get detailed analysis result."""
    db = get_database()
    doc = await db.analysis_results.find_one({"_id": analysis_id})

    if not doc:
        raise HTTPException(status_code=404, detail="Analysis not found")

    # Check ownership
    if doc["user_id"] != str(current_user.id) and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    return AnalysisDetailResponse(
        id=str(doc["_id"]),
        user_id=doc["user_id"],
        image_url=doc.get("image_url", ""),
        image_type=doc.get("image_type", ""),
        original_filename=doc.get("original_filename", ""),
        prediction=doc.get("prediction", ""),
        disease_name=doc.get("disease_name"),
        confidence_score=doc.get("confidence_score", 0),
        risk_level=doc.get("risk_level", "low"),
        risk_score=doc.get("risk_score", 0),
        detected_patterns=doc.get("detected_patterns", []),
        findings=doc.get("findings", []),
        recommendations=doc.get("recommendations", []),
        ai_explanation=doc.get("ai_explanation"),
        status=doc.get("status", ""),
        processing_time_ms=doc.get("processing_time_ms"),
        doctor_reviewed=doc.get("doctor_reviewed", False),
        doctor_notes=doc.get("doctor_notes"),
        report_generated=doc.get("report_generated", False),
        created_at=doc.get("created_at", datetime.utcnow()),
    )


@router.delete("/results/{analysis_id}")
async def delete_analysis(
    analysis_id: str,
    current_user: User = Depends(get_current_user),
):
    """Delete an analysis result."""
    db = get_database()
    doc = await db.analysis_results.find_one({"_id": analysis_id})

    if not doc:
        raise HTTPException(status_code=404, detail="Analysis not found")

    if doc["user_id"] != str(current_user.id) and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    # Delete file
    file_path = doc.get("image_url", "").replace("/uploads/", "uploads/")
    if os.path.exists(file_path):
        os.remove(file_path)

    await db.analysis_results.delete_one({"_id": analysis_id})
    return {"message": "Analysis deleted successfully"}
