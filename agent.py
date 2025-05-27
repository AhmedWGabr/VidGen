import json

def validate_segment(seg):
    required_fields = ["start", "end", "narration"]
    for field in required_fields:
        if field not in seg:
            raise ValueError(f"Missing required field: {field}")
    if float(seg["end"]) <= float(seg["start"]):
        raise ValueError("End time must be greater than start time")

def parse_detailed_script(detailed_script):
    """
    Parses the detailed script from Gemini (expected as JSON list of segments)
    and splits it into commands for video, TTS, audio, and image models.
    Assigns a unique face and seed for each character.

    Returns:
        dict: {
            "video": [segment_dict, ...],
            "tts": [narration_text, ...],
            "audio": [audio_text, ...],
            "image": [{"character": name, "face_prompt": prompt, "seed": seed}, ...]
        }
    """
    import hashlib
    try:
        segments = json.loads(detailed_script)
        video_cmds = []
        tts_cmds = []
        audio_cmds = []
        image_cmds = []
        character_faces = {}
        for seg in segments:
            validate_segment(seg)
            # Assume seg["image"] contains a character name or description
            char_desc = seg.get("image", "")
            if char_desc:
                # Use character name as key, assign unique seed and prompt
                char_name = char_desc.strip().split(":")[0] if ":" in char_desc else char_desc.strip()
                if char_name not in character_faces:
                    # Deterministic seed from character name
                    seed = int(hashlib.sha256(char_name.encode()).hexdigest(), 16) % (2**32)
                    character_faces[char_name] = {
                        "character": char_name,
                        "face_prompt": char_desc,
                        "seed": seed
                    }
                seg["character_face"] = character_faces[char_name]
            video_cmds.append(seg)
            tts_cmds.append(seg.get("narration", ""))
            audio_cmds.append(seg.get("audio", ""))
        image_cmds = list(character_faces.values())
        return {
            "video": video_cmds,
            "tts": tts_cmds,
            "audio": audio_cmds,
            "image": image_cmds
        }
    except Exception as e:
        return {
            "video": [],
            "tts": [],
            "audio": [],
            "image": [],
            "error": f"Failed to parse Gemini output: {str(e)}"
        }
