"""
AI Prediction Engine
Runs medical image classification using Vision Transformer, ResNet50, and ensemble methods.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models
from transformers import ViTForImageClassification, ViTImageProcessor
from PIL import Image
import numpy as np
import logging
import os

logger = logging.getLogger("medivision.ai.prediction")

# Disease labels for heart-related conditions
HEART_DISEASE_LABELS = [
    "Normal",
    "Arrhythmia",
    "Atrial Fibrillation",
    "Cardiomegaly",
    "Congestive Heart Failure",
    "Coronary Artery Disease",
    "Heart Valve Disease",
    "Hypertrophic Cardiomyopathy",
    "Myocardial Infarction",
    "Pericardial Effusion",
]


class PredictionEngine:
    """Medical image prediction engine with ensemble models."""

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.vit_model = None
        self.resnet_model = None
        self.vit_processor = None
        self.custom_cnn = None
        self._models_loaded = False

    def load_models(self):
        """Load all AI models. Called lazily on first prediction."""
        if self._models_loaded:
            return

        logger.info("Loading AI models...")
        try:
            # Vision Transformer
            model_name = "google/vit-base-patch16-224"
            self.vit_processor = ViTImageProcessor.from_pretrained(model_name)
            self.vit_model = ViTForImageClassification.from_pretrained(
                model_name,
                num_labels=len(HEART_DISEASE_LABELS),
                ignore_mismatched_sizes=True,
            )
            self.vit_model.to(self.device)
            self.vit_model.eval()

            # ResNet50
            self.resnet_model = models.resnet50(pretrained=True)
            # Modify final layer for heart disease classification
            num_features = self.resnet_model.fc.in_features
            self.resnet_model.fc = nn.Sequential(
                nn.Dropout(0.3),
                nn.Linear(num_features, 512),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(512, len(HEART_DISEASE_LABELS)),
            )
            self.resnet_model.to(self.device)
            self.resnet_model.eval()

            # Custom CNN for medical images
            self.custom_cnn = MedicalCNN(num_classes=len(HEART_DISEASE_LABELS))
            self.custom_cnn.to(self.device)
            self.custom_cnn.eval()

            self._models_loaded = True
            logger.info("All AI models loaded successfully")

        except Exception as e:
            logger.error(f"Failed to load models: {e}")
            logger.info("Falling back to simulation mode")
            self._models_loaded = False

    def predict_vit(self, image: Image.Image) -> dict:
        """Run Vision Transformer prediction."""
        if not self._models_loaded:
            return self._simulate_prediction("vit")

        try:
            inputs = self.vit_processor(images=image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            with torch.no_grad():
                outputs = self.vit_model(**inputs)
                probabilities = F.softmax(outputs.logits, dim=-1)
                confidence, predicted_idx = torch.max(probabilities, dim=-1)

            pred_idx = predicted_idx.item()
            return {
                "model": "ViT",
                "prediction": "Disease Detected" if pred_idx > 0 else "No Disease Detected",
                "disease_name": HEART_DISEASE_LABELS[pred_idx],
                "confidence": confidence.item(),
                "probabilities": {
                    HEART_DISEASE_LABELS[i]: prob.item()
                    for i, prob in enumerate(probabilities[0])
                },
            }
        except Exception as e:
            logger.error(f"ViT prediction failed: {e}")
            return self._simulate_prediction("vit")

    def predict_resnet(self, image: Image.Image) -> dict:
        """Run ResNet50 prediction."""
        if not self._models_loaded:
            return self._simulate_prediction("resnet")

        try:
            from torchvision import transforms
            transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ])

            input_tensor = transform(image).unsqueeze(0).to(self.device)

            with torch.no_grad():
                outputs = self.resnet_model(input_tensor)
                probabilities = F.softmax(outputs, dim=-1)
                confidence, predicted_idx = torch.max(probabilities, dim=-1)

            pred_idx = predicted_idx.item()
            return {
                "model": "ResNet50",
                "prediction": "Disease Detected" if pred_idx > 0 else "No Disease Detected",
                "disease_name": HEART_DISEASE_LABELS[pred_idx],
                "confidence": confidence.item(),
                "probabilities": {
                    HEART_DISEASE_LABELS[i]: prob.item()
                    for i, prob in enumerate(probabilities[0])
                },
            }
        except Exception as e:
            logger.error(f"ResNet prediction failed: {e}")
            return self._simulate_prediction("resnet")

    def predict_custom_cnn(self, image: Image.Image) -> dict:
        """Run custom CNN prediction."""
        if not self._models_loaded or self.custom_cnn is None:
            return self._simulate_prediction("custom_cnn")

        try:
            from torchvision import transforms
            transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ])

            input_tensor = transform(image).unsqueeze(0).to(self.device)

            with torch.no_grad():
                outputs = self.custom_cnn(input_tensor)
                probabilities = F.softmax(outputs, dim=-1)
                confidence, predicted_idx = torch.max(probabilities, dim=-1)

            pred_idx = predicted_idx.item()
            return {
                "model": "CustomCNN",
                "prediction": "Disease Detected" if pred_idx > 0 else "No Disease Detected",
                "disease_name": HEART_DISEASE_LABELS[pred_idx],
                "confidence": confidence.item(),
            }
        except Exception as e:
            logger.error(f"Custom CNN prediction failed: {e}")
            return self._simulate_prediction("custom_cnn")

    def ensemble_predict(self, vit_result: dict, resnet_result: dict) -> dict:
        """Combine predictions from multiple models using weighted ensemble."""
        # Weights: ViT=0.45, ResNet=0.35, CustomCNN=0.20
        vit_weight = 0.45
        resnet_weight = 0.35

        # Average confidence
        avg_confidence = (
            vit_result["confidence"] * vit_weight +
            resnet_result["confidence"] * resnet_weight
        ) / (vit_weight + resnet_weight)

        # Majority vote for prediction
        predictions = [vit_result["prediction"], resnet_result["prediction"]]
        disease_votes = [vit_result.get("disease_name", ""), resnet_result.get("disease_name", "")]

        if predictions.count("Disease Detected") > predictions.count("No Disease Detected"):
            final_prediction = "Disease Detected"
            # Pick disease with highest confidence
            disease_name = vit_result.get("disease_name") if vit_result["confidence"] > resnet_result["confidence"] else resnet_result.get("disease_name")
        elif predictions.count("No Disease Detected") > predictions.count("Disease Detected"):
            final_prediction = "No Disease Detected"
            disease_name = None
        else:
            # Tie-break by confidence
            if vit_result["confidence"] >= resnet_result["confidence"]:
                final_prediction = vit_result["prediction"]
                disease_name = vit_result.get("disease_name")
            else:
                final_prediction = resnet_result["prediction"]
                disease_name = resnet_result.get("disease_name")

        # Detect patterns
        patterns = []
        if avg_confidence > 0.7:
            patterns.append("High confidence abnormality detected")
        if vit_result.get("disease_name") == resnet_result.get("disease_name") and vit_result.get("disease_name"):
            patterns.append(f"Both models agree on {vit_result['disease_name']}")

        return {
            "prediction": final_prediction,
            "disease_name": disease_name,
            "confidence": avg_confidence,
            "patterns": patterns,
            "model_agreement": vit_result["prediction"] == resnet_result["prediction"],
            "individual_results": {
                "vit": vit_result,
                "resnet": resnet_result,
            },
        }

    def _simulate_prediction(self, model_name: str) -> dict:
        """Simulate prediction when models are not available (development mode)."""
        import random
        random.seed(hash(model_name) % 10000)

        is_disease = random.random() > 0.5
        confidence = random.uniform(0.65, 0.97)
        disease_idx = random.randint(1, len(HEART_DISEASE_LABELS) - 1) if is_disease else 0

        return {
            "model": model_name,
            "prediction": "Disease Detected" if is_disease else "No Disease Detected",
            "disease_name": HEART_DISEASE_LABELS[disease_idx] if is_disease else None,
            "confidence": confidence,
            "simulated": True,
        }


class MedicalCNN(nn.Module):
    """Custom CNN architecture for medical image classification."""

    def __init__(self, num_classes: int = 10):
        super(MedicalCNN, self).__init__()

        self.features = nn.Sequential(
            # Block 1
            nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1),

            # Block 2
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),

            # Block 3
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),

            # Block 4
            nn.Conv2d(256, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((1, 1)),
        )

        self.classifier = nn.Sequential(
            nn.Dropout(0.4),
            nn.Linear(512, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(256, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x
