import subprocess
import os
import logging
from config import Config, VideoGenConfig

logger = logging.getLogger("VidGen.assemble")

def assemble_video(video_segments, tts_audios, background_audios, character_images, output_path=None):
    """
    Assemble video segments, TTS audio, background audio, and character images into a final video using ffmpeg.
    Args:
        video_segments (list): Paths to video segment files.
        tts_audios (list): Paths to TTS audio files.
        background_audios (list): Paths to background audio files.
        character_images (list): Paths to character image files.
        output_path (str): Output video file path.
    Returns:
        str: Path to final assembled video.
    """
    if not video_segments:
        logger.error("No video segments provided for assembly.")
        return "no_video_segments.mp4"

    if output_path is None:
        output_path = os.path.join(VideoGenConfig.OUTPUT_DIR, "final_video.mp4")

    try:
        # Concatenate video segments
        segments_txt = os.path.join(VideoGenConfig.TEMP_DIR, "segments.txt")
        with open(segments_txt, "w") as f:
            for seg in video_segments:
                f.write(f"file '{seg}'\n")
        concat_cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", segments_txt,
            "-c", "copy", os.path.join(VideoGenConfig.TEMP_DIR, "temp_video.mp4")
        ]
        subprocess.run(concat_cmd, check=True)

        # Mix TTS and background audio
        if tts_audios and background_audios:
            audio_inputs = []
            for tts, bg in zip(tts_audios, background_audios):
                mixed = os.path.join(Config.TEMP_DIR, f"mixed_{os.path.basename(tts)}")
                mix_cmd = [
                    "ffmpeg", "-y", "-i", tts, "-i", bg, "-filter_complex",
                    "[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=2", mixed
                ]
                subprocess.run(mix_cmd, check=True)
                audio_inputs.append(mixed)
            audios_txt = os.path.join(Config.TEMP_DIR, "audios.txt")
            with open(audios_txt, "w") as f:
                for a in audio_inputs:
                    f.write(f"file '{a}'\n")
            concat_audio_cmd = [
                "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", audios_txt,
                "-c", "copy", os.path.join(Config.TEMP_DIR, "final_audio.wav")
            ]
            subprocess.run(concat_audio_cmd, check=True)
            audio_file = os.path.join(Config.TEMP_DIR, "final_audio.wav")
        elif tts_audios:
            audios_txt = os.path.join(Config.TEMP_DIR, "audios.txt")
            with open(audios_txt, "w") as f:
                for a in tts_audios:
                    f.write(f"file '{a}'\n")
            concat_audio_cmd = [
                "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", audios_txt,
                "-c", "copy", os.path.join(Config.TEMP_DIR, "final_audio.wav")
            ]
            subprocess.run(concat_audio_cmd, check=True)
            audio_file = os.path.join(Config.TEMP_DIR, "final_audio.wav")
        else:
            audio_file = None

        # Combine video and audio
        temp_video = os.path.join(Config.TEMP_DIR, "temp_video.mp4")
        if audio_file:
            final_cmd = [
                "ffmpeg", "-y", "-i", temp_video, "-i", audio_file, "-c:v", "copy", "-c:a", "aac", output_path
            ]
            subprocess.run(final_cmd, check=True)
        else:
            # No audio, just video
            subprocess.run(["copy", temp_video, output_path], shell=True, check=True)

        return output_path
    except Exception as e:
        logger.error(f"Failed to assemble video: {e}")
        raise
