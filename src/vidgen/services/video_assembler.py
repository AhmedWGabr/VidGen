import subprocess
import os
import logging
from vidgen.core.config import VideoGenConfig

logger = logging.getLogger("VidGen.assemble")

def assemble_video(video_segments, tts_audios, background_audios, character_images, output_path=None):
    if not video_segments:
        logger.error("No video segments provided for assembly.")
        return "no_video_segments.mp4"

    if output_path is None:
        output_path = os.path.join(VideoGenConfig.OUTPUT_DIR, "final_video.mp4")

    try:
        segments_txt = os.path.join(VideoGenConfig.TEMP_DIR, "segments.txt")
        with open(segments_txt, "w") as f:
            for seg in video_segments:
                f.write(f"file '{seg}'\n")
        concat_cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", segments_txt,
            "-c", "copy", os.path.join(VideoGenConfig.TEMP_DIR, "temp_video.mp4")
        ]
        subprocess.run(concat_cmd, check=True)

        if tts_audios and background_audios:
            audio_inputs = []
            for tts, bg in zip(tts_audios, background_audios):
                mixed = os.path.join(VideoGenConfig.TEMP_DIR, f"mixed_{os.path.basename(tts)}")
                mix_cmd = [
                    "ffmpeg", "-y", "-i", tts, "-i", bg, "-filter_complex",
                    "[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=2", mixed
                ]
                subprocess.run(mix_cmd, check=True)
                audio_inputs.append(mixed)
            audios_txt = os.path.join(VideoGenConfig.TEMP_DIR, "audios.txt")
            with open(audios_txt, "w") as f:
                for a in audio_inputs:
                    f.write(f"file '{a}'\n")
            concat_audio_cmd = [
                "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", audios_txt,
                "-c", "copy", os.path.join(VideoGenConfig.TEMP_DIR, "final_audio.wav")
            ]
            subprocess.run(concat_audio_cmd, check=True)
            audio_file = os.path.join(VideoGenConfig.TEMP_DIR, "final_audio.wav")
        elif tts_audios:
            audios_txt = os.path.join(VideoGenConfig.TEMP_DIR, "audios.txt")
            with open(audios_txt, "w") as f:
                for a in tts_audios:
                    f.write(f"file '{a}'\n")
            concat_audio_cmd = [
                "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", audios_txt,
                "-c", "copy", os.path.join(VideoGenConfig.TEMP_DIR, "final_audio.wav")
            ]
            subprocess.run(concat_audio_cmd, check=True)
            audio_file = os.path.join(VideoGenConfig.TEMP_DIR, "final_audio.wav")
        else:
            audio_file = None

        temp_video = os.path.join(VideoGenConfig.TEMP_DIR, "temp_video.mp4")
        if audio_file:
            final_cmd = [
                "ffmpeg", "-y", "-i", temp_video, "-i", audio_file,
                "-c:v", "copy", "-c:a", "aac", "-shortest", output_path
            ]
            subprocess.run(final_cmd, check=True)
            logger.info(f"Final video with audio saved to {output_path}")
        else:
            # Just copy the temp video if no audio
            import shutil
            shutil.copy2(temp_video, output_path)
            logger.info(f"Final video (no audio) saved to {output_path}")

        # Add character overlays if available
        if character_images:
            overlay_path = os.path.join(VideoGenConfig.TEMP_DIR, "with_characters.mp4")
            overlay_cmd = [
                "ffmpeg", "-y", "-i", output_path
            ]
            
            for idx, img in enumerate(character_images):
                overlay_cmd.extend(["-i", img])
            
            filter_complex = ""
            for idx in range(len(character_images)):
                # Position each character at different locations
                x_pos = 50 + (idx * 150)
                filter_complex += f"[{idx+1}:v]scale=150:-1[char{idx}]; "
                if idx == 0:
                    filter_complex += f"[0:v][char{idx}]overlay=x={x_pos}:y=50"
                else:
                    filter_complex += f"[tmp{idx-1}][char{idx}]overlay=x={x_pos}:y=50"
                
                if idx < len(character_images) - 1:
                    filter_complex += f"[tmp{idx}]; "
            
            overlay_cmd.extend(["-filter_complex", filter_complex])
            overlay_cmd.extend(["-c:a", "copy", overlay_path])
            
            try:
                subprocess.run(overlay_cmd, check=True)
                # Replace output with the version with character overlays
                shutil.copy2(overlay_path, output_path)
                logger.info(f"Added character overlays to video: {output_path}")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to add character overlays: {e}")
                # Keep the version without overlays

        return output_path
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Video assembly failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during video assembly: {e}")
        return None

def cleanup_temp_files():
    """Remove temporary files created during video assembly"""
    temp_pattern = os.path.join(VideoGenConfig.TEMP_DIR, "*")
    cleanup_cmd = ["rm", "-f", temp_pattern]
    try:
        subprocess.run(cleanup_cmd, check=True, shell=True)
        logger.info("Temporary files cleaned up")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to clean up temporary files: {e}")