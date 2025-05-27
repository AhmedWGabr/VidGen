import os
import subprocess
from config import Config
import tempfile
import atexit
import threading

# Global cache for Stable Diffusion pipeline
_image_pipeline = None
_image_pipeline_lock = threading.Lock()
temp_files = []

def cleanup_temp_files():
    for file_path in temp_files:
        try:
            os.remove(file_path)
        except Exception:
            pass
atexit.register(cleanup_temp_files)

def get_image_pipeline():
    global _image_pipeline
    with _image_pipeline_lock:
        if _image_pipeline is None:
            from diffusers import StableDiffusionPipeline
            import torch
            _image_pipeline = StableDiffusionPipeline.from_pretrained(
                Config.STABLE_DIFFUSION_MODEL,
                torch_dtype=torch.float16
            )
            _image_pipeline = _image_pipeline.to("cuda" if torch.cuda.is_available() else "cpu")
        return _image_pipeline

def generate_video_segment(video_command, face_cache=None, default_duration=5):
    """
    Generate a video segment by combining a generated character image and TTS audio.
    Uses segment duration and character face/seed if provided.
    face_cache: dict mapping (character, seed) -> image_path to avoid regenerating faces.
    """
    import uuid

    # Extract info from video_command
    narration = video_command.get("narration", "")
    duration = float(video_command.get("end", 0)) - float(video_command.get("start", 0))
    if duration <= 0:
        duration = default_duration

    # Get character face info
    character_face = video_command.get("character_face", {})
    char_name = character_face.get("character", "")
    face_prompt = character_face.get("face_prompt", "")
    face_seed = character_face.get("seed", 42)

    # Use cache to avoid regenerating the same face
    if face_cache is not None and char_name:
        cache_key = (char_name, face_seed)
        if cache_key in face_cache:
            image_path = face_cache[cache_key]
        else:
            image_path = generate_character_image(face_prompt, seed=face_seed)
            face_cache[cache_key] = image_path
    else:
        image_path = generate_character_image(face_prompt, seed=face_seed)

    audio_path = generate_tts_audio(narration)

    output_path = os.path.join(Config.OUTPUT_DIR, f"video_segment_{uuid.uuid4().hex}.mp4")
    temp_files.append(output_path)
    # Create a video from the image and audio using ffmpeg
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", image_path,
        "-i", audio_path,
        "-c:v", "libx264", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest", "-t", str(duration),
        output_path
    ]
    subprocess.run(cmd, check=True)
    return output_path

def generate_tts_audio(tts_command):
    """
    Generate audio from text using Bark TTS.
    """
    try:
        from bark import SAMPLE_RATE, generate_audio
        import scipy.io.wavfile
        audio_array = generate_audio(tts_command)
        output_path = os.path.join(Config.OUTPUT_DIR, "tts_audio.wav")
        temp_files.append(output_path)
        scipy.io.wavfile.write(output_path, SAMPLE_RATE, audio_array)
        return output_path
    except Exception as e:
        print(f"Error generating TTS audio: {e}")
        return f"tts_error_{str(e)}.wav"

def generate_background_audio(audio_command):
    """
    Placeholder for local audio/background music model.
    Returns a static silent audio file for now.
    """
    output_path = os.path.join(Config.OUTPUT_DIR, "background_audio.wav")
    temp_files.append(output_path)
    os.system(f"ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t 1 -q:a 9 -acodec pcm_s16le -y {output_path}")
    return output_path

def generate_character_image(image_command, seed=42):
    """
    Generate an image using Stable Diffusion (diffusers) with a fixed seed.
    """
    try:
        import torch
        import random
        generator = torch.Generator(device="cuda" if torch.cuda.is_available() else "cpu").manual_seed(int(seed))
        pipe = get_image_pipeline()
        image = pipe(image_command, generator=generator).images[0]
        output_path = os.path.join(Config.OUTPUT_DIR, "character_image.png")
        temp_files.append(output_path)
        image.save(output_path)
        return output_path
    except Exception as e:
        print(f"Error generating image for prompt '{image_command}': {e}")
        return "placeholder_image.png"
