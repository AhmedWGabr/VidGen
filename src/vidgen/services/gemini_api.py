import requests
import logging
from vidgen.core.config import VideoGenConfig

logger = logging.getLogger("VidGen.services.gemini_api")

def call_gemini_api(script, api_key, segment_duration=5):
    """
    Calls Gemini API (gemini-2.0-flash-001) with a structured prompt to control output.
    Requests timestamps and segment durations.
    
    Args:
        script (str): The script to process
        api_key (str): The Gemini API key
        segment_duration (int): Target segment duration in seconds
        
    Returns:
        str: The JSON string response from Gemini API, or None if failed
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{VideoGenConfig.GEMINI_MODEL}:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": api_key}
    
    prompt = (
        f"Expand the following scene script into a detailed, timestamped breakdown for video generation. "
        f"Divide the script into segments of approximately {segment_duration} seconds each. "
        f"For each segment, provide:\n"
        f"- Start and end timestamps\n"
        f"- Scene description\n"
        f"- Narration/dialogue\n"
        f"- Background audio/music\n"
        f"- Visual/motion details\n"
        f"- Character face/image description\n\n"
        f"Output as a JSON list, one object per segment, with keys: start, end, scene, narration, audio, visual, image.\n\n"
        f"Script:\n{script}"
    )
    
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, headers=headers, params=params, json=data, timeout=60)
        response.raise_for_status()
        
        # Extract the text content from Gemini's response format
        response_data = response.json()
        if "candidates" in response_data and len(response_data["candidates"]) > 0:
            candidate = response_data["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                text_content = candidate["content"]["parts"][0].get("text", "")
                logger.info(f"Received response from Gemini API: {len(text_content)} characters")
                return text_content
        
        logger.error("Unexpected Gemini API response format")
        return None
        
    except requests.RequestException as e:
        logger.error(f"Gemini API call failed: {e}")
        return None
