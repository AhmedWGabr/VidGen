import os

import subprocess

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

    output_path = f"video_segment_{uuid.uuid4().hex}.mp4"
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
    import subprocess
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
        output_path = "tts_audio.wav"
        scipy.io.wavfile.write(output_path, SAMPLE_RATE, audio_array)
        return output_path
    except Exception as e:
        return f"tts_error_{str(e)}.wav"

def generate_background_audio(audio_command):
    """
    Placeholder for local audio/background music model.
    Returns a static silent audio file for now.
    """
    output_path = "background_audio.wav"
    os.system(f"ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t 1 -q:a 9 -acodec pcm_s16le -y {output_path}")
    return output_path

def generate_character_image(image_command, seed=42):
    """
    Generate an image using Stable Diffusion (diffusers) with a fixed seed.
    """
    try:
        from diffusers import StableDiffusionPipeline
        import torch
        import random
        generator = torch.Generator(device="cuda" if torch.cuda.is_available() else "cpu").manual_seed(int(seed))
        pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16
        )
        pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")
        image = pipe(image_command, generator=generator).images[0]
        output_path = "character_image.png"
        image.save(output_path)
        return output_path
    except Exception as e:
        return f"image_error_{str(e)}.png"
