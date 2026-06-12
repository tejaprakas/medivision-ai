"""
AI Analysis Service
Orchestrates the medical image analysis pipeline.
"""

import time
import logging
from datetime import datetime
from app.models.analysis import AnalysisResult, RiskLevel
from app.services.image_service import preprocess_image
from app.ai.image_processor import ImageProcessor
from app.ai.prediction_engine import PredictionEngine
from app.core.database import get_database

logger = logging.getLogger("medivision.analysis_service")


async def run_analysis_pipeline(analysis_id: str, image_path: str, image_type):
    """Run the complete AI analysis pipeline."""
    start_time = time.time()
    db = get_database()

    # Update status to processing
    await db.analysis_results.update_one(
        {"_id": analysis_id},
        {"$set": {"status": "processing"}}
    )

    try:
        # Step 1: Preprocess image
        logger.info(f"Preprocessing image: {image_path}")
        processed_image = preprocess_image(image_path)

        # Step 2: Initialize AI models
        image_processor = ImageProcessor()
        prediction_engine = PredictionEngine()

        # Step 3: Extract features
        logger.info("Extracting features...")
        features = image_processor.extract_features(processed_image)

        # Step 4: Run predictions (ensemble)
        logger.info("Running AI predictions...")
        vit_result = prediction_engine.predict_vit(processed_image)
        resnet_result = prediction_engine.predict_resnet(processed_image)
        ensemble_result = prediction_engine.ensemble_predict(vit_result, resnet_result)

        # Step 5: Determine risk level
        confidence = ensemble_result["confidence"]
        risk_level = _determine_risk_level(confidence, ensemble_result["prediction"])
        risk_score = _calculate_risk_score(confidence, risk_level)

        # Step 6: Generate findings and recommendations
        findings = _generate_findings(ensemble_result, image_type)
        recommendations = _generate_recommendations(risk_level, ensemble_result)
        detected_patterns = ensemble_result.get("patterns", [])

        # Step 7: Generate AI explanation
        ai_explanation = _generate_ai_explanation(
            ensemble_result, risk_level, findings, image_type
        )

        processing_time = int((time.time() - start_time) * 1000)

        # Update analysis result
        await db.analysis_results.update_one(
            {"_id": analysis_id},
            {"$set": {
                "status": "completed",
                "prediction": ensemble_result["prediction"],
                "disease_name": ensemble_result.get("disease_name"),
                "confidence_score": confidence,
                "risk_level": risk_level.value,
                "risk_score": risk_score,
                "vit_prediction": vit_result,
                "resnet_prediction": resnet_result,
                "ensemble_prediction": ensemble_result,
                "detected_patterns": detected_patterns,
                "findings": findings,
                "recommendations": recommendations,
                "ai_explanation": ai_explanation,
                "processing_time_ms": processing_time,
                "updated_at": datetime.utcnow(),
            }}
        )

        # Create notification
        await _create_analysis_notification(analysis_id, ensemble_result["prediction"])

        logger.info(f"Analysis {analysis_id} completed in {processing_time}ms")

    except Exception as e:
        logger.error(f"Analysis pipeline failed: {e}", exc_info=True)
        await db.analysis_results.update_one(
            {"_id": analysis_id},
            {"$set": {
                "status": "failed",
                "error_message": str(e),
                "updated_at": datetime.utcnow(),
            }}
        )
        raise


def _determine_risk_level(confidence: float, prediction: str) -> RiskLevel:
    """Determine risk level based on confidence and prediction."""
    if prediction == "No Disease Detected":
        if confidence > 0.85:
            return RiskLevel.LOW
        return RiskLevel.MODERATE

    # Disease detected
    if confidence > 0.9:
        return RiskLevel.CRITICAL
    elif confidence > 0.75:
        return RiskLevel.HIGH
    elif confidence > 0.5:
        return RiskLevel.MODERATE
    return RiskLevel.LOW


def _calculate_risk_score(confidence: float, risk_level: RiskLevel) -> float:
    """Calculate numerical risk score (0-100)."""
    base_scores = {
        RiskLevel.LOW: 20,
        RiskLevel.MODERATE: 50,
        RiskLevel.HIGH: 75,
        RiskLevel.CRITICAL: 95,
    }
    base = base_scores.get(risk_level, 50)
    # Adjust by confidence
    return min(100, base * confidence)


def _generate_findings(ensemble_result: dict, image_type) -> list[str]:
    """Generate medical findings from prediction results."""
    findings = []
    prediction = ensemble_result.get("prediction", "")

    if prediction == "Disease Detected":
        disease = ensemble_result.get("disease_name", "abnormal patterns")
        findings.append(f"AI model detected signs of {disease} in the {image_type.value if hasattr(image_type, 'value') else image_type} image.")
        findings.append(f"Confidence level: {ensemble_result['confidence']:.1%}")

        patterns = ensemble_result.get("patterns", [])
        for pattern in patterns[:3]:
            findings.append(f"Detected pattern: {pattern}")
    else:
        findings.append(f"No significant abnormalities detected in the {image_type.value if hasattr(image_type, 'value') else image_type} image.")
        findings.append(f"Normal confidence: {ensemble_result['confidence']:.1%}")

    return findings


def _generate_recommendations(risk_level: RiskLevel, ensemble_result: dict) -> list[str]:
    """Generate recommendations based on risk level."""
    recommendations = []

    if risk_level == RiskLevel.CRITICAL:
        recommendations.append("⚠️ URGENT: Please consult a cardiologist immediately.")
        recommendations.append("Seek emergency medical attention if experiencing symptoms.")
        recommendations.append("Avoid strenuous physical activity until evaluated.")
    elif risk_level == RiskLevel.HIGH:
        recommendations.append("Schedule an appointment with a cardiologist as soon as possible.")
        recommendations.append("Monitor for symptoms: chest pain, shortness of breath, dizziness.")
        recommendations.append("Maintain a heart-healthy diet and avoid smoking.")
    elif risk_level == RiskLevel.MODERATE:
        recommendations.append("Consider scheduling a routine check-up with your doctor.")
        recommendations.append("Maintain regular exercise and a balanced diet.")
        recommendations.append("Monitor blood pressure and cholesterol levels.")
    else:
        recommendations.append("Continue maintaining a healthy lifestyle.")
        recommendations.append("Regular annual check-ups are recommended.")
        recommendations.append("Stay active and maintain a balanced diet.")

    recommendations.append("⚠️ This is an AI-generated preliminary screening. Always consult a qualified healthcare professional.")

    return recommendations


def _generate_ai_explanation(ensemble_result: dict, risk_level: RiskLevel, findings: list, image_type) -> str:
    """Generate a human-readable AI explanation."""
    prediction = ensemble_result.get("prediction", "")
    confidence = ensemble_result.get("confidence", 0)
    disease = ensemble_result.get("disease_name", "abnormal patterns")
    img_type = image_type.value if hasattr(image_type, "value") else str(image_type)

    if prediction == "Disease Detected":
        explanation = (
            f"Based on the analysis of your {img_type.upper()} image, our AI model has detected "
            f"signs of {disease} with {confidence:.1%} confidence. "
            f"The risk level is assessed as **{risk_level.value.upper()}**. "
            f"\n\nKey findings:\n"
        )
        for i, finding in enumerate(findings, 1):
            explanation += f"{i}. {finding}\n"
        explanation += (
            f"\n⚠️ Important: This is an AI-generated preliminary screening result. "
            f"It is NOT a medical diagnosis. Please consult a licensed healthcare professional "
            f"for proper clinical evaluation and diagnosis."
        )
    else:
        explanation = (
            f"Based on the analysis of your {img_type.upper()} image, our AI model found "
            f"no significant abnormalities with {confidence:.1%} confidence. "
            f"The risk level is assessed as **{risk_level.value.upper()}**. "
            f"\n\nHowever, this does not guarantee the absence of heart disease. "
            f"Regular check-ups and a healthy lifestyle are always recommended. "
            f"\n⚠️ This is an AI-generated preliminary screening result. "
            f"Always consult a qualified healthcare professional for medical advice."
        )

    return explanation


async def _create_analysis_notification(analysis_id: str, prediction: str):
    """Create notification for completed analysis."""
    from app.models.notification import Notification, NotificationType, NotificationPriority
    from app.core.database import get_database

    db = get_database()
    analysis = await db.analysis_results.find_one({"_id": analysis_id})
    if not analysis:
        return

    priority = NotificationPriority.NORMAL
    if "Disease" in prediction:
        priority = NotificationPriority.HIGH

    notification = Notification(
        user_id=analysis["user_id"],
        type=NotificationType.ANALYSIS_COMPLETE,
        priority=priority,
        title="Analysis Complete",
        message=f"Your medical image analysis is ready. Result: {prediction}",
        data={"analysis_id": analysis_id},
        action_url=f"/dashboard/analysis/{analysis_id}",
    )
    await notification.create()
