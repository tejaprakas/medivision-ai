"""
Analytics API Routes
Platform-wide analytics and statistics.
"""

from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
from app.core.security import get_current_user, require_admin, require_doctor_or_admin
from app.core.database import get_database
from app.models.user import User
import logging

logger = logging.getLogger("medivision.analytics")
router = APIRouter()


@router.get("/dashboard")
async def get_dashboard_analytics(current_user: User = Depends(require_doctor_or_admin)):
    """Get dashboard analytics data."""
    db = get_database()
    now = datetime.utcnow()
    thirty_days_ago = now - timedelta(days=30)

    # User statistics
    total_patients = await db.users.count_documents({"role": "patient"})
    total_doctors = await db.users.count_documents({"role": "doctor"})
    total_users = total_patients + total_doctors

    # Analysis statistics
    total_analyses = await db.analysis_results.count_documents({})
    completed_analyses = await db.analysis_results.count_documents({"status": "completed"})
    pending_analyses = await db.analysis_results.count_documents({"status": "pending"})
    failed_analyses = await db.analysis_results.count_documents({"status": "failed"})

    # Risk distribution
    risk_pipeline = [
        {"$match": {"status": "completed"}},
        {"$group": {"_id": "$risk_level", "count": {"$sum": 1}}},
    ]
    risk_distribution = {}
    async for doc in db.analysis_results.aggregate(risk_pipeline):
        risk_distribution[doc["_id"]] = doc["count"]

    # Image type distribution
    type_pipeline = [
        {"$group": {"_id": "$image_type", "count": {"$sum": 1}}},
    ]
    type_distribution = {}
    async for doc in db.analysis_results.aggregate(type_pipeline):
        type_distribution[doc["_id"]] = doc["count"]

    # Monthly analysis count
    monthly_pipeline = [
        {"$match": {"created_at": {"$gte": thirty_days_ago}}},
        {"$group": {
            "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"}},
            "count": {"$sum": 1},
        }},
        {"$sort": {"_id": 1}},
    ]
    monthly_data = []
    async for doc in db.analysis_results.aggregate(monthly_pipeline):
        monthly_data.append({"date": doc["_id"], "count": doc["count"]})

    # Appointment statistics
    total_appointments = await db.appointments.count_documents({})
    pending_appointments = await db.appointments.count_documents({"status": "pending"})
    completed_appointments = await db.appointments.count_documents({"status": "completed"})

    # Report statistics
    total_reports = await db.medical_reports.count_documents({})

    return {
        "users": {
            "total": total_users,
            "patients": total_patients,
            "doctors": total_doctors,
        },
        "analyses": {
            "total": total_analyses,
            "completed": completed_analyses,
            "pending": pending_analyses,
            "failed": failed_analyses,
        },
        "risk_distribution": risk_distribution,
        "image_type_distribution": type_distribution,
        "monthly_analyses": monthly_data,
        "appointments": {
            "total": total_appointments,
            "pending": pending_appointments,
            "completed": completed_appointments,
        },
        "reports": {
            "total": total_reports,
        },
    }


@router.get("/patient/{patient_id}")
async def get_patient_analytics(
    patient_id: str,
    current_user: User = Depends(get_current_user),
):
    """Get analytics for a specific patient."""
    db = get_database()

    # Check access
    if (current_user.role.value == "patient" and str(current_user.id) != patient_id):
        from fastapi import HTTPException, status
        raise HTTPException(status_code=403, detail="Access denied")

    total_analyses = await db.analysis_results.count_documents({"user_id": patient_id})
    completed = await db.analysis_results.count_documents({"user_id": patient_id, "status": "completed"})

    # Risk history
    risk_pipeline = [
        {"$match": {"user_id": patient_id, "status": "completed"}},
        {"$sort": {"created_at": 1}},
        {"$project": {"risk_score": 1, "risk_level": 1, "created_at": 1}},
    ]
    risk_history = []
    async for doc in db.analysis_results.aggregate(risk_pipeline):
        risk_history.append({
            "risk_score": doc.get("risk_score", 0),
            "risk_level": doc.get("risk_level", "low"),
            "date": doc.get("created_at").isoformat() if doc.get("created_at") else None,
        })

    return {
        "total_analyses": total_analyses,
        "completed_analyses": completed,
        "risk_history": risk_history,
    }
