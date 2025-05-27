import os

import subprocess

def generate_video_segment(video_command):
    """
    Generate a video segment by combining a generated character image and TTS audio.
    """
    from models import generate_character_image, generate_tts_audio
    import uuid

    # Generate image and audio for the segment
    image_path = generate_character_image(video_command.get("image", ""), seed=42)
    audio_path = generate_tts_audio(video_command.get("narration", ""))

    output_path = f"video_segment_{uuid.uuid4().hex}.mp4"
    # Create a video from the image and audio using ffmpeg
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", image_path,
        "-i", audio_path,
        "-c:v", "libx264", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest", "-t", "5",
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
