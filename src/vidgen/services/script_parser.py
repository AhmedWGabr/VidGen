import json
import logging
from vidgen.models.data_models import ScriptSegment, Character
from vidgen.utils.helpers import load_json_safe

logger = logging.getLogger("VidGen.agent")

def validate_segment(seg):
    required_fields = ["start", "end", "narration"]
    for field in required_fields:
        if field not in seg:
            logger.error(f"Missing required field: {field}")
            raise ValueError(f"Missing required field: {field}")
    if float(seg["end"]) <= float(seg["start"]):
        logger.error("End time must be greater than start time")
        raise ValueError("End time must be greater than start time")

def parse_detailed_script(detailed_script):
    import hashlib
    try:
        # Use the safe JSON loader that can handle Gemini response format
        segments = load_json_safe(detailed_script)
        
        if not segments:
            logger.error("Failed to parse JSON from detailed script")
            raise ValueError("Invalid JSON in detailed script")
        
        if not isinstance(segments, list):
            logger.error("Expected list of segments, got: %s", type(segments))
            raise ValueError("Script must be a list of segments")
        video_cmds = []
        tts_cmds = []
        audio_cmds = []
        image_cmds = []
        character_faces = {}
        for seg in segments:
            validate_segment(seg)
            char_desc = seg.get("image", "")
            if char_desc:
                char_name = char_desc.strip().split(":")[0] if ":" in char_desc else char_desc.strip()
                if char_name not in character_faces:
                    seed = int(hashlib.sha256(char_name.encode()).hexdigest(), 16) % (2**32)
                    character_faces[char_name] = {
                        "character": char_name,
                        "face_prompt": char_desc,
                        "seed": seed
                    }
                seg["character_face"] = character_faces[char_name]
            try:
                ScriptSegment(
                    timestamp=float(seg["start"]),
                    duration=float(seg["end"]) - float(seg["start"]),
                    narration=seg.get("narration", ""),
                    character=Character(name=seg["character_face"]["character"], description=seg["character_face"]["face_prompt"], seed=seg["character_face"]["seed"]) if "character_face" in seg else None,
                    scene_description=seg.get("scene", "")
                )
            except Exception as e:
                logger.error(f"Segment validation failed: {e}")
                raise
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
        logger.error(f"Failed to parse detailed script: {e}")
        raise
