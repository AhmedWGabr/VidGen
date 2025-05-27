def parse_detailed_script(detailed_script):
    """
    Parses the detailed script from Gemini and splits it into commands
    for video, TTS, audio, and image models.

    Args:
        detailed_script (str): The detailed script from Gemini.

    Returns:
        dict: {
            "video": [...],
            "tts": [...],
            "audio": [...],
            "image": [...]
        }
    """
    # Placeholder: Replace with actual parsing logic
    return {
        "video": ["scene 1: ...", "scene 2: ..."],
        "tts": ["narration 1", "dialogue 2"],
        "audio": ["background music 1", "effect 2"],
        "image": ["character face 1", "character face 2"]
    }
