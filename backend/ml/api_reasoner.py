import logging
import json
import os
from openai import OpenAI
from backend.config import settings

logger = logging.getLogger(__name__)
client = OpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)
MODEL_NAME = "llama-3.3-70b-versatile"

def generate_ai_advisory(disease: str, crop: str, confidence: float, severity: str) -> str:
    """
    Generate AI advisory for plant disease using Groq.
    """
    try:
        if not settings.GROQ_API_KEY:
            logger.warning("GROQ_API_KEY not set. Skipping AI advisory.")
            return "AI Advisory configuration missing."

        if "unknown" in disease.lower():
            prompt = (
                f"The user has submitted a plant image that was not recognized by our model (identified as '{disease}'). "
                f"Confidence score: {confidence:.2f}. "
                f"Please inform the user that the system could not identify the specific disease with certainty. "
                f"Advise them to:\n"
                f"1. Check if the image is clear and well-lit.\n"
                f"2. Ensure the image focuses on the affected leaf area.\n"
                f"3. Use the 'Report Issue' feature to send this case to an agricultural expert for manual review.\n"
                f"Keep the tone helpful and guiding."
            )
        elif "healthy" in disease.lower():
            prompt = (
                f"The model detected that the {crop} plant is HEALTHY (Confidence: {confidence:.2f}). "
                f"Provide a positive message confirming the plant looks healthy. "
                f"Include 3-4 general tips for maintaining good plant health, such as correct watering practices, "
                f"soil nutrition, and regular monitoring. "
                f"Keep the tone encouraging."
            )
        else:
            prompt = (
                f"You are an expert plant pathologist and agricultural consultant. "
                f"Analyze the following detection:\n"
                f"- Disease: {disease}\n"
                f"- Crop: {crop}\n"
                f"- Confidence: {confidence:.2f}\n"
                f"- Severity Stage: {severity}\n\n"
                f"Provide a detailed advisory using EXACTLY the following headings (use Markdown):\n\n"
                f"### Why this disease occurs\n"
                f"[Explain the environmental conditions or vectors that favor this disease]\n\n"
                f"### Visible Symptoms\n"
                f"[List the key visual signs to look for]\n\n"
                f"### Root Cause\n"
                f"[Identify the pathogen type: Fungal, Bacterial, Viral, etc., and specific organism if known]\n\n"
                f"### Immediate Action\n"
                f"[Steps to take right now to stop spread]\n\n"
                f"### Treatment Recommendations\n"
                f"[Organic and chemical control options]\n\n"
                f"### Fertilizer Suggestions\n"
                f"[Recommendations for nutrient management to boost immunity or recovery]\n\n"
                f"### Preventive Measures\n"
                f"[Long-term practices to prevent recurrence]\n\n"
                f"Keep the tone professional yet accessible to farmers."
            )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful agricultural AI assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=MODEL_NAME,
            temperature=0.7,
            max_tokens=1024,
        )

        return chat_completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating AI advisory: {e}")
        return "AI Advisory unavailable at the moment. Please consult a local expert."

def translate_text(text: str, target_language: str) -> str:
    """
    Translate text to target language using Groq.
    """
    try:
        if not settings.GROQ_API_KEY:
             return text

        prompt = f"Translate the following text to {target_language}. Return ONLY the translated text, no preamble or quotes:\n\n{text}"
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": "You are a professional translator. Output only the translation."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            model=MODEL_NAME,
            temperature=0.3
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error translating text: {e}")
        return text

def translate_batch(texts: dict[str, str], target_language: str) -> dict[str, str]:
    """
    Translate a batch of texts (dictionary values) to target language.
    """
    if not texts or not settings.GROQ_API_KEY:
        return texts
        
    try:
        prompt = (
            f"Translate the values of the following JSON dictionary to {target_language}. "
            f"Return ONLY the valid JSON with the same keys and translated values. "
            f"Do not include markdown code blocks (```json ... ```), just the raw JSON string.\n\n"
            f"{json.dumps(texts, ensure_ascii=False)}"
        )

        chat_completion = client.chat.completions.create(
             messages=[
                {
                    "role": "system", 
                    "content": "You are a translator API. Output only valid JSON."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            model=MODEL_NAME,
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        result = chat_completion.choices[0].message.content
        return json.loads(result)
    except Exception as e:
        logger.error(f"Error in batch translation: {e}")
        return texts
