"""
AI Image Processor
Handles image preprocessing and feature extraction using OpenCV and PyTorch.
"""

import torch
import numpy as np
from PIL import Image
from torchvision import transforms
import cv2
import logging

logger = logging.getLogger("medivision.ai.image_processor")


class ImageProcessor:
    """Medical image processing and feature extraction."""

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Standard ImageNet normalization for model input
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            ),
        ])

        # Medical-specific preprocessing
        self.medical_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])

    def preprocess_for_model(self, image: Image.Image) -> torch.Tensor:
        """Preprocess image for AI model input."""
        if image.mode != "RGB":
            image = image.convert("RGB")
        tensor = self.transform(image)
        return tensor.unsqueeze(0).to(self.device)

    def extract_features(self, image: Image.Image) -> dict:
        """Extract visual features from medical image using OpenCV."""
        img_array = np.array(image)

        # Convert to grayscale for analysis
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array

        features = {}

        # Statistical features
        features["mean_intensity"] = float(np.mean(gray))
        features["std_intensity"] = float(np.std(gray))
        features["min_intensity"] = float(np.min(gray))
        features["max_intensity"] = float(np.max(gray))

        # Texture features using GLCM-like analysis
        features["contrast"] = float(np.std(gray) ** 2)
        features["entropy"] = float(self._calculate_entropy(gray))

        # Edge detection
        edges = cv2.Canny(gray, 50, 150)
        features["edge_density"] = float(np.sum(edges > 0) / edges.size)

        # CLAHE enhancement
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        features["enhanced_contrast"] = float(np.std(enhanced))

        return features

    def _calculate_entropy(self, image: np.ndarray) -> float:
        """Calculate image entropy."""
        hist = cv2.calcHist([image], [0], None, [256], [0, 256])
        hist = hist.ravel() / hist.sum()
        hist = hist[hist > 0]
        return -np.sum(hist * np.log2(hist))

    def generate_heatmap(self, image: Image.Image, attention_weights: np.ndarray) -> np.ndarray:
        """Generate Grad-CAM style heatmap for visualization."""
        img_array = np.array(image.resize((224, 224)))

        # Resize attention weights to image size
        heatmap = cv2.resize(attention_weights, (224, 224))
        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

        # Overlay on original image
        if len(img_array.shape) == 2:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR)

        superimposed = cv2.addWeighted(img_array, 0.6, heatmap, 0.4, 0)
        return superimposed

    def detect_anomalies(self, image: Image.Image) -> list[str]:
        """Basic anomaly detection in medical images."""
        img_array = np.array(image.convert("L"))
        anomalies = []

        # Check for unusual intensity distributions
        mean_val = np.mean(img_array)
        std_val = np.std(img_array)

        if mean_val < 50:
            anomalies.append("Image appears unusually dark")
        elif mean_val > 200:
            anomalies.append("Image appears unusually bright")

        if std_val < 20:
            anomalies.append("Low contrast detected - image may be underexposed")

        # Check for motion blur
        laplacian_var = cv2.Laplacian(img_array, cv2.CV_64F).var()
        if laplacian_var < 100:
            anomalies.append("Possible motion blur detected")

        return anomalies
