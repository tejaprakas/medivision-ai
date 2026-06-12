"""
Medical Report API Routes
Generate, download, and manage PDF medical reports.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from datetime import datetime
from app.core.security import get_current_user
from app.core.database import get_database
from app.models.user import User
from app.models.report import MedicalReport, ReportResponse
from app.services.report_service import generate_pdf_report
import logging

logger = logging.getLogger("medivision.reports")
router = APIRouter()


@router.post("/generate/{analysis_id}", response_model=ReportResponse)
async def generate_report(
    analysis_id: str,
    current_user: User = Depends(get_current_user),
):
    """Generate PDF report for an analysis."""
    db = get_database()

    # Get analysis
    analysis = await db.analysis_results.find_one({"_id": analysis_id})
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    if analysis["user_id"] != str(current_user.id) and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    if analysis.get("status") != "completed":
        raise HTTPException(status_code=400, detail="Analysis not yet completed")

    # Generate report number
    count = await db.medical_reports.count_documents({})
    report_number = f"MR-{datetime.utcnow().year}-{count + 1:04d}"

    # Create report record
    report = MedicalReport(
        user_id=str(current_user.id),
        patient_id=str(current_user.id),
        analysis_id=analysis_id,
        report_number=report_number,
        patient_name=current_user.full_name,
        image_type=analysis.get("image_type", ""),
        prediction=analysis.get("prediction", ""),
        disease_name=analysis.get("disease_name"),
        confidence_score=analysis.get("confidence_score", 0),
        risk_level=analysis.get("risk_level", "low"),
        findings=analysis.get("findings", []),
        recommendations=analysis.get("recommendations", []),
        ai_explanation=analysis.get("ai_explanation"),
    )
    await report.create()

    # Generate PDF
    try:
        pdf_path = await generate_pdf_report(report, analysis)
        await db.medical_reports.update_one(
            {"_id": report.id},
            {"$set": {"pdf_url": f"/uploads/reports/{report_number}.pdf", "pdf_generated": True}}
        )
    except Exception as e:
        logger.error(f"PDF generation failed: {e}")

    # Update analysis
    await db.analysis_results.update_one(
        {"_id": analysis_id},
        {"$set": {"report_generated": True, "report_id": str(report.id)}}
    )

    return ReportResponse(
        id=str(report.id),
        report_number=report.report_number,
        title=report.title,
        image_type=report.image_type,
        prediction=report.prediction,
        confidence_score=report.confidence_score,
        risk_level=report.risk_level,
        pdf_url=report.pdf_url,
        pdf_generated=report.pdf_generated,
        created_at=report.created_at,
    )


@router.get("/my-reports", response_model=list[ReportResponse])
async def get_my_reports(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
):
    """Get user's medical reports."""
    db = get_database()
    cursor = db.medical_reports.find(
        {"user_id": str(current_user.id)}
    ).sort("created_at", -1).skip(skip).limit(limit)

    reports = []
    async for doc in cursor:
        reports.append(ReportResponse(
            id=str(doc["_id"]),
            report_number=doc["report_number"],
            title=doc.get("title", ""),
            image_type=doc.get("image_type", ""),
            prediction=doc.get("prediction", ""),
            confidence_score=doc.get("confidence_score", 0),
            risk_level=doc.get("risk_level", "low"),
            pdf_url=doc.get("pdf_url"),
            pdf_generated=doc.get("pdf_generated", False),
            created_at=doc.get("created_at", datetime.utcnow()),
        ))
    return reports


@router.get("/download/{report_id}")
async def download_report(
    report_id: str,
    current_user: User = Depends(get_current_user),
):
    """Download PDF report."""
    db = get_database()
    report = await db.medical_reports.find_one({"_id": report_id})

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if report["user_id"] != str(current_user.id) and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    pdf_path = f"uploads/reports/{report['report_number']}.pdf"
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF file not found")

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"MediVision_Report_{report['report_number']}.pdf",
    )
