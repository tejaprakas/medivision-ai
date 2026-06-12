"""
Image Upload Service
Handles file validation, saving, and preprocessing.
"""

import os
from fastapi import UploadFile
from PIL import Image
import io

# Allowed file types
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".dcm"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "application/dicom"}
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB


def validate_image(file: UploadFile) -> tuple[bool, str]:
    """Validate uploaded image file."""
    filename = file.filename or ""
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
    if file.content_type and file.content_type not in ALLOWED_MIME_TYPES:
        return False, f"Invalid MIME type: {file.content_type}"
    return True, ""


async def save_upload_file(file: UploadFile, directory: str, filename: str) -> str:
    """Save uploaded file to disk."""
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, filename)
    content = await file.read()

    # Verify it's actually an image using PIL
    try:
        img = Image.open(io.BytesIO(content))
        img.verify()
    except Exception:
        raise ValueError("File is not a valid image")

    # Check file size
    if len(content) > MAX_FILE_SIZE:
        raise ValueError(f"File too large. Max size: {MAX_FILE_SIZE // (1024*1024)}MB")

    with open(file_path, "wb") as f:
        f.write(content)
    return file_path


def preprocess_image(image_path: str, target_size: tuple = (224, 224)) -> Image.Image:
    """Preprocess image for AI model input."""
    from PIL import Image, ImageEnhance
    import cv2
    import numpy as np

    if image_path.endswith(".dcm"):
        try:
            import pydicom
            dcm = pydicom.dcmread(image_path)
            img_array = dcm.pixel_array
            img_array = ((img_array - img_array.min()) / (img_array.max() - img_array.min()) * 255).astype(np.uint8)
            img = Image.fromarray(img_array)
            if img.mode != "RGB":
                img = img.convert("RGB")
        except ImportError:
            raise ValueError("pydicom not installed")
    else:
        img = Image.open(image_path).convert("RGB")

    # Enhance contrast using CLAHE
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    lab = cv2.cvtColor(img_cv, cv2.COLOR_BGR2LAB)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    lab[:, :, 0] = clahe.apply(lab[:, :, 0])
    img_cv = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    img = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
    img = img.resize(target_size, Image.LANCZOS)
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.5)
    return img


def get_image_info(image_path: str) -> dict:
    """Get image metadata."""
    img = Image.open(image_path)
    return {
        "width": img.width,
        "height": img.height,
        "mode": img.mode,
        "format": img.format,
        "size_bytes": os.path.getsize(image_path),
    }
