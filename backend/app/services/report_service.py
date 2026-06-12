"""
PDF Report Generator Service
Generates professional medical PDF reports.
"""

import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image as RLImage, PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import logging

logger = logging.getLogger("medivision.reports")

# Brand colors
PRIMARY = colors.HexColor("#2563EB")
SECONDARY = colors.HexColor("#06B6D4")
SUCCESS = colors.HexColor("#10B981")
WARNING = colors.HexColor("#F59E0B")
DANGER = colors.HexColor("#EF4444")
DARK = colors.HexColor("#1E293B")
LIGHT_GRAY = colors.HexColor("#F1F5F9")
MEDIUM_GRAY = colors.HexColor("#94A3B8")


async def generate_pdf_report(report, analysis: dict) -> str:
    """Generate a professional PDF medical report."""
    os.makedirs("uploads/reports", exist_ok=True)
    pdf_path = f"uploads/reports/{report.report_number}.pdf"

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="ReportTitle",
        fontSize=24,
        leading=30,
        textColor=PRIMARY,
        alignment=TA_CENTER,
        spaceAfter=6,
        fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        name="ReportSubtitle",
        fontSize=11,
        leading=14,
        textColor=MEDIUM_GRAY,
        alignment=TA_CENTER,
        spaceAfter=20,
        fontName="Helvetica",
    ))
    styles.add(ParagraphStyle(
        name="SectionHeader",
        fontSize=14,
        leading=18,
        textColor=DARK,
        spaceBefore=16,
        spaceAfter=8,
        fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        name="BodyText",
        fontSize=10,
        leading=14,
        textColor=DARK,
        alignment=TA_JUSTIFY,
        fontName="Helvetica",
    ))
    styles.add(ParagraphStyle(
        name="Disclaimer",
        fontSize=8,
        leading=11,
        textColor=DANGER,
        alignment=TA_JUSTIFY,
        fontName="Helvetica-Oblique",
    ))

    elements = []

    # Header
    elements.append(Paragraph("MediVision AI", styles["ReportTitle"]))
    elements.append(Paragraph("AI-Powered Medical Analysis Report", styles["ReportSubtitle"]))
    elements.append(HRFlowable(width="100%", thickness=2, color=PRIMARY, spaceAfter=16))

    # Report Info Table
    info_data = [
        ["Report Number:", report.report_number, "Date:", report.created_at.strftime("%B %d, %Y")],
        ["Patient Name:", report.patient_name, "Image Type:", report.image_type.upper()],
    ]
    info_table = Table(info_data, colWidths=[100, 180, 80, 120])
    info_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (0, -1), DARK),
        ("TEXTCOLOR", (2, 0), (2, -1), DARK),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, -1), (-1, -1), 0.5, MEDIUM_GRAY),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 16))

    # Analysis Results Section
    elements.append(Paragraph("Analysis Results", styles["SectionHeader"]))
    elements.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceAfter=10))

    # Prediction result with color coding
    prediction_color = DANGER if report.prediction == "Disease Detected" else SUCCESS
    risk_color = {
        "low": SUCCESS,
        "moderate": WARNING,
        "high": DANGER,
        "critical": DANGER,
    }.get(report.risk_level, MEDIUM_GRAY)

    result_data = [
        ["Prediction:", report.prediction],
        ["Confidence Score:", f"{report.confidence_score:.1%}"],
        ["Risk Level:", report.risk_level.upper()],
    ]
    if report.disease_name:
        result_data.insert(1, ["Detected Condition:", report.disease_name])

    result_table = Table(result_data, colWidths=[140, 340])
    result_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TEXTCOLOR", (0, 0), (0, -1), DARK),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, LIGHT_GRAY]),
        ("GRID", (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
    ]))
    elements.append(result_table)
    elements.append(Spacer(1, 16))

    # Findings
    if report.findings:
        elements.append(Paragraph("Findings", styles["SectionHeader"]))
        for finding in report.findings:
            elements.append(Paragraph(f"• {finding}", styles["BodyText"]))
            elements.append(Spacer(1, 4))
        elements.append(Spacer(1, 8))

    # AI Explanation
    if report.ai_explanation:
        elements.append(Paragraph("AI Explanation", styles["SectionHeader"]))
        elements.append(Paragraph(report.ai_explanation, styles["BodyText"]))
        elements.append(Spacer(1, 12))

    # Recommendations
    if report.recommendations:
        elements.append(Paragraph("Recommendations", styles["SectionHeader"]))
        for rec in report.recommendations:
            elements.append(Paragraph(f"• {rec}", styles["BodyText"]))
            elements.append(Spacer(1, 4))
        elements.append(Spacer(1, 8))

    # Doctor Notes
    if report.doctor_notes:
        elements.append(Paragraph("Doctor's Notes", styles["SectionHeader"]))
        elements.append(Paragraph(report.doctor_notes, styles["BodyText"]))
        elements.append(Spacer(1, 12))

    # Disclaimer
    elements.append(Spacer(1, 20))
    elements.append(HRFlowable(width="100%", thickness=1, color=DANGER, spaceAfter=8))
    elements.append(Paragraph(
        "⚠️ MEDICAL DISCLAIMER: This AI system provides preliminary screening results and should not be "
        "considered a medical diagnosis. The analysis is generated by artificial intelligence models and "
        "is intended for educational and preliminary screening purposes only. Always consult a licensed "
        "healthcare professional for clinical decisions and proper medical diagnosis.",
        styles["Disclaimer"],
    ))

    # Footer
    elements.append(Spacer(1, 30))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=MEDIUM_GRAY, spaceAfter=6))
    elements.append(Paragraph(
        f"Generated by MediVision AI | Report #{report.report_number} | {report.created_at.strftime('%Y-%m-%d %H:%M UTC')}",
        ParagraphStyle("Footer", fontSize=7, textColor=MEDIUM_GRAY, alignment=TA_CENTER),
    ))

    # Build PDF
    doc.build(elements)
    logger.info(f"PDF report generated: {pdf_path}")

    return pdf_path
