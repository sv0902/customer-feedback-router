import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

def classify_feedback(text):
    fallback = {
        "intent": "Unknown",
        "topic": "General",
        "priority": "Low",
        "confidence": 0.0,
        "status": "needs_review"
    }

    if not text or text.strip() == "":
        return fallback

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[AI Error]: GEMINI_API_KEY not found in environment!")
        return fallback

    prompt = f"""
    Classify this customer feedback: "{text}"
    Return ONLY a valid JSON object matching this schema:
    {{"intent": "...", "topic": "...", "priority": "...", "confidence": 0.0}}
    """

    try:
        client = genai.Client(api_key=api_key)
        res = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        clean = res.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean)

        conf = float(data.get("confidence", 0.0))
        data["confidence"] = conf
        data["status"] = "processed" if conf >= 0.7 else "needs_review"
        return data

    except Exception as e:
        print(f"[AI Error]: {e}")
        return fallback

if __name__ == "__main__":
    result = classify_feedback("The app crashes when I try to login.")
    print("Test output:", result)