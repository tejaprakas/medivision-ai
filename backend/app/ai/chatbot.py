"""
AI Medical Chatbot Service
Uses BioGPT/BioBERT for medical text generation and Q&A.
"""

import logging
from typing import List, Optional

logger = logging.getLogger("medivision.ai.chatbot")

# Medical knowledge base for fallback responses
MEDICAL_KNOWLEDGE = {
    "heart disease": {
        "description": "Heart disease refers to several types of heart conditions. The most common type in the United States is coronary artery disease (CAD), which affects blood flow to the heart.",
        "symptoms": "Common symptoms include chest pain, shortness of breath, fatigue, irregular heartbeat, and swelling in legs or feet.",
        "prevention": "Maintain a healthy diet, exercise regularly, avoid smoking, manage stress, and get regular check-ups.",
        "risk_factors": "High blood pressure, high cholesterol, diabetes, obesity, smoking, family history, and sedentary lifestyle.",
    },
    "arrhythmia": {
        "description": "Arrhythmia is an irregular heartbeat. The heart may beat too fast (tachycardia), too slow (bradycardia), or with an irregular pattern.",
        "symptoms": "Palpitations, chest pain, dizziness, fainting, fatigue, and shortness of breath.",
        "prevention": "Limit caffeine and alcohol, manage stress, avoid stimulants, and maintain a healthy weight.",
    },
    "cardiomegaly": {
        "description": "Cardiomegaly means an enlarged heart. It's not a disease but a sign of another condition.",
        "symptoms": "Shortness of breath, swelling in legs, fatigue, and irregular heartbeat.",
        "prevention": "Control blood pressure, treat underlying conditions, and maintain heart-healthy habits.",
    },
    "myocardial infarction": {
        "description": "A myocardial infarction (heart attack) occurs when blood flow to part of the heart is blocked, causing damage to the heart muscle.",
        "symptoms": "Chest pain or discomfort, shortness of breath, nausea, cold sweat, and pain in arms, neck, or jaw.",
        "prevention": "Healthy diet, regular exercise, no smoking, managing cholesterol and blood pressure.",
    },
}

# Multilingual greetings
GREETINGS = {
    "english": "Hello! I'm your AI medical assistant. How can I help you today?",
    "telugu": "నమస్కారం! నేను మీ AI వైద్య సహాయకుడిని. నేను మీకు ఎలా సహాయపడగలను?",
    "hindi": "नमस्ते! मैं आपका AI चिकित्सा सहायक हूं। मैं आपकी कैसे मदद कर सकता हूं?",
    "tamil": "வணக்கம்! நான் உங்கள் AI மருத்துவ உதவியாளர். நான் உங்களுக்கு எப்படி உதவ முடியும்?",
}

# Suggested prompts
SUGGESTED_PROMPTS = [
    "What are the symptoms of heart disease?",
    "How can I prevent heart disease?",
    "Explain my ECG report",
    "What does high cholesterol mean?",
    "What is a normal blood pressure?",
    "How to maintain a healthy heart?",
]


class ChatbotService:
    """AI Medical Chatbot using Hugging Face models."""

    def __init__(self):
        self.model = None
        self.tokenizer = None
        self._model_loaded = False

    def load_model(self):
        """Load BioGPT model for medical text generation."""
        if self._model_loaded:
            return

        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM

            logger.info("Loading BioGPT model...")
            model_name = "microsoft/BioGPT"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            self._model_loaded = True
            logger.info("BioGPT model loaded successfully")
        except Exception as e:
            logger.warning(f"Could not load BioGPT model: {e}. Using knowledge base fallback.")
            self._model_loaded = False

    async def generate_response(
        self,
        user_message: str,
        conversation_history: List[dict] = None,
        language: str = "english",
    ) -> str:
        """Generate AI response to user message."""
        # Try model-based response first
        if self._model_loaded:
            try:
                return await self._model_response(user_message, conversation_history)
            except Exception as e:
                logger.error(f"Model response failed: {e}")

        # Fallback to knowledge base
        return self._knowledge_base_response(user_message, language)

    async def _model_response(self, user_message: str, conversation_history: list = None) -> str:
        """Generate response using BioGPT model."""
        # Build prompt with medical context
        system_context = (
            "You are a helpful AI medical assistant. Provide accurate, helpful health information. "
            "Always recommend consulting a healthcare professional for medical decisions. "
            "Be clear that you provide educational information, not medical diagnosis.\n\n"
        )

        # Build conversation context
        context = system_context
        if conversation_history:
            for msg in conversation_history[-5:]:  # Last 5 messages
                role = "User" if msg["role"] == "user" else "Assistant"
                context += f"{role}: {msg['content']}\n"

        context += f"User: {user_message}\nAssistant:"

        inputs = self.tokenizer.encode(context, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_new_tokens=256,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Extract only the assistant's response
        if "Assistant:" in response:
            response = response.split("Assistant:")[-1].strip()

        return response

    def _knowledge_base_response(self, user_message: str, language: str) -> str:
        """Generate response from medical knowledge base."""
        message_lower = user_message.lower()

        # Check for greetings
        if any(word in message_lower for word in ["hello", "hi", "hey", "namaste", "నమస్కారం", "வணக்கம்"]):
            return GREETINGS.get(language, GREETINGS["english"])

        # Check for heart disease related queries
        for topic, info in MEDICAL_KNOWLEDGE.items():
            if topic.replace(" ", "") in message_lower.replace(" ", ""):
                if "symptom" in message_lower:
                    return f"**{topic.title()} Symptoms:**\n\n{info.get('symptoms', 'No specific symptoms information available.')}\n\n⚠️ This is for educational purposes only. Please consult a doctor for medical advice."
                elif "prevent" in message_lower:
                    return f"**Preventing {topic.title()}:**\n\n{info.get('prevention', 'No specific prevention information available.')}\n\n⚠️ This is for educational purposes only. Please consult a doctor for medical advice."
                elif "risk" in message_lower:
                    return f"**{topic.title()} Risk Factors:**\n\n{info.get('risk_factors', 'No specific risk factor information available.')}\n\n⚠️ This is for educational purposes only. Please consult a doctor for medical advice."
                else:
                    return f"**About {topic.title()}:**\n\n{info.get('description', 'No description available.')}\n\n⚠️ This is for educational purposes only. Please consult a doctor for medical advice."

        # Check for report explanation requests
        if any(word in message_lower for word in ["report", "result", "analysis", "ecg", "mri", "x-ray", "xray", "ct scan"]):
            return (
                "I'd be happy to help explain your medical report. Based on AI analysis:\n\n"
                "🔍 **Understanding Your Results:**\n"
                "• **Confidence Score** indicates how certain the AI model is about its prediction\n"
                "• **Risk Level** (Low/Moderate/High/Critical) shows the urgency of follow-up\n"
                "• **Detected Patterns** are specific features the AI identified in your image\n\n"
                "📋 **Next Steps:**\n"
                "1. Review the detailed findings in your report\n"
                "2. Share the report with your doctor\n"
                "3. Schedule a follow-up appointment if risk is moderate or higher\n\n"
                "⚠️ AI results are for preliminary screening only. Always consult a healthcare professional for diagnosis."
            )

        # Check for general health questions
        if "blood pressure" in message_lower:
            return (
                "**Normal Blood Pressure:**\n\n"
                "• Normal: Less than 120/80 mmHg\n"
                "• Elevated: 120-129/less than 80 mmHg\n"
                "• High (Stage 1): 130-139/80-89 mmHg\n"
                "• High (Stage 2): 140 or higher/90 or higher mmHg\n\n"
                "Regular monitoring is important for heart health.\n"
                "⚠️ Consult your doctor for personalized advice."
            )

        if "cholesterol" in message_lower:
            return (
                "**Healthy Cholesterol Levels:**\n\n"
                "• Total cholesterol: Less than 200 mg/dL\n"
                "• LDL (bad): Less than 100 mg/dL\n"
                "• HDL (bad): Less than 100 mg/dL\n"
                "• HDL (good): 60 mg/dL or higher\n"
                "• Triglycerides: Less than 150 mg/dL\n\n"
                "A heart-healthy diet and regular exercise can help maintain healthy levels.\n"
                "⚠️ Consult your doctor for personalized advice."
            )

        # Default response
        return (
            "Thank you for your question. As an AI medical assistant, I can provide general health information "
            "about heart health, common conditions, and wellness tips.\n\n"
            "Here are some things I can help with:\n"
            "• Explaining medical terms and conditions\n"
            "• Providing information about heart disease prevention\n"
            "• Discussing symptoms and when to see a doctor\n"
            "• General wellness and lifestyle guidance\n\n"
            "⚠️ **Important:** I provide educational information only. I cannot diagnose conditions or replace "
            "professional medical advice. Always consult a qualified healthcare provider for medical decisions.\n\n"
            "What would you like to know about?"
        )


# Global chatbot instance
chatbot_service = ChatbotService()


async def generate_chat_response(
    user_message: str,
    conversation_history: list = None,
    language: str = "english",
) -> str:
    """Global function to generate chatbot response."""
    return await chatbot_service.generate_response(
        user_message=user_message,
        conversation_history=conversation_history,
        language=language,
    )


def get_suggested_prompts() -> list[str]:
    """Get suggested chat prompts."""
    return SUGGESTED_PROMPTS
