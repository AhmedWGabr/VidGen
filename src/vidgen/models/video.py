import os
import subprocess
import logging
from vidgen.core.config import VideoGenConfig
from vidgen.models.image import generate_character_image
from vidgen.models.tts import generate_tts_audio

def generate_video_segment(video_command, face_cache=None, default_duration=5):
    """
    Generate a video segment by combining a generated character image and TTS audio.
    Uses segment duration and character face/seed if provided.
    
    Args:
        video_command (dict): Dictionary containing segment information
        face_cache (dict): Cache mapping (character, seed) -> image_path to avoid regenerating faces
        default_duration (int): Default duration if not specified in command
        
    Returns:
        str: Path to the generated video segment
    """
    import uuid
    logger = logging.getLogger("VidGen.models.video")
    
    try:
        # Extract information from video command
        narration = video_command.get("narration", "")
        duration = float(video_command.get("end", 0)) - float(video_command.get("start", 0))
        if duration <= 0:
            duration = default_duration
            logger.warning(f"Invalid duration calculated, using default: {default_duration}s")
        
        character_face = video_command.get("character_face", {})
        char_name = character_face.get("character", "")
        face_prompt = character_face.get("face_prompt", "")
        face_seed = character_face.get("seed", 42)
        
        # Generate or retrieve character image
        if face_cache is not None and char_name:
            cache_key = (char_name, face_seed)
            if cache_key in face_cache:
                image_path = face_cache[cache_key]
                logger.debug(f"Using cached image for character: {char_name}")
            else:
                image_path = generate_character_image(face_prompt, seed=face_seed)
                if image_path and image_path != "placeholder_image.png":
                    face_cache[cache_key] = image_path
        else:
            image_path = generate_character_image(face_prompt, seed=face_seed)
        
        # Generate TTS audio
        audio_path = generate_tts_audio(narration)
        
        # Ensure we have valid paths
        if not image_path or image_path == "placeholder_image.png":
            logger.warning("Using placeholder image for video segment")
            # Create a simple colored background as fallback
            image_path = create_fallback_image()
        
        if not audio_path:
            logger.warning("No audio generated, creating silent video")
            # Create silent audio
            audio_path = create_silent_audio(duration)
        
        # Generate unique output filename
        segment_id = uuid.uuid4().hex[:8]
        output_filename = f"video_segment_{segment_id}.mp4"
        output_path = os.path.join(VideoGenConfig.OUTPUT_DIR, "videos", output_filename)
        
        # Ensure videos directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Create video using ffmpeg
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
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info(f"Generated video segment: {output_path}")
        return output_path
        
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg failed to generate video segment: {e.stderr}")
        raise
    except Exception as e:
        logger.error(f"Failed to generate video segment: {e}")
        raise

def create_fallback_image():
    """Create a simple fallback image when character generation fails"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a simple colored background
        img = Image.new('RGB', (512, 512), color='lightblue')
        draw = ImageDraw.Draw(img)
        
        # Add some text
        try:
            font = ImageFont.load_default()
            draw.text((256, 256), "Character Image", fill='black', anchor='mm', font=font)
        except:
            draw.text((200, 240), "Character Image", fill='black')
        
        fallback_path = os.path.join(VideoGenConfig.OUTPUT_DIR, "images", "fallback_character.png")
        os.makedirs(os.path.dirname(fallback_path), exist_ok=True)
        img.save(fallback_path)
        return fallback_path
        
    except ImportError:
        logger.warning("PIL not available, cannot create fallback image")
        return "placeholder_image.png"
    except Exception as e:
        logger.error(f"Failed to create fallback image: {e}")
        return "placeholder_image.png"

def create_silent_audio(duration):
    """Create silent audio file of specified duration"""
    try:
        import uuid
        silent_filename = f"silent_audio_{uuid.uuid4().hex[:8]}.wav"
        silent_path = os.path.join(VideoGenConfig.OUTPUT_DIR, "audio", silent_filename)
        
        os.makedirs(os.path.dirname(silent_path), exist_ok=True)
        
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", f"anullsrc=r=44100:cl=mono",
            "-t", str(duration),
            "-q:a", "9",
            "-acodec", "pcm_s16le",
            silent_path
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        return silent_path
        
    except Exception as e:
        logger.error(f"Failed to create silent audio: {e}")
        return None

def generate_video_with_transitions(segments, transition_type="fade", transition_duration=0.5):
    """
    Generate a video with transitions between segments.
    
    Args:
        segments (list): List of video segment paths
        transition_type (str): Type of transition ("fade", "slide", "wipe")
        transition_duration (float): Duration of transitions in seconds
        
    Returns:
        str: Path to the final video with transitions
    """
    logger = logging.getLogger("VidGen.models.video")
    
    if not segments:
        return None
    
    if len(segments) == 1:
        return segments[0]
    
    try:
        import uuid
        output_filename = f"video_with_transitions_{uuid.uuid4().hex[:8]}.mp4"
        output_path = os.path.join(VideoGenConfig.OUTPUT_DIR, "videos", output_filename)
        
        # Build filter complex for transitions
        filter_complex = _build_transition_filter(segments, transition_type, transition_duration)
        
        cmd = ["ffmpeg", "-y"]
        
        # Add input files
        for segment in segments:
            cmd.extend(["-i", segment])
        
        cmd.extend([
            "-filter_complex", filter_complex,
            "-map", "[out]",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-preset", "medium",
            "-crf", "23",
            output_path
        ])
        
        subprocess.run(cmd, check=True, capture_output=True)
        logger.info(f"Generated video with transitions: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Failed to create video with transitions: {e}")
        # Return concatenated video without transitions as fallback
        return concatenate_videos(segments)

def add_motion_effects(video_path, effect_type="zoom_pan", intensity=0.1):
    """
    Add motion effects to a static video.
    
    Args:
        video_path (str): Path to input video
        effect_type (str): Type of motion effect ("zoom_pan", "parallax", "shake")
        intensity (float): Intensity of the effect (0.0 to 1.0)
        
    Returns:
        str: Path to video with motion effects
    """
    logger = logging.getLogger("VidGen.models.video")
    
    try:
        import uuid
        output_filename = f"video_motion_{uuid.uuid4().hex[:8]}.mp4"
        output_path = os.path.join(VideoGenConfig.OUTPUT_DIR, "videos", output_filename)
        
        # Create motion filter based on effect type
        if effect_type == "zoom_pan":
            motion_filter = _create_zoom_pan_filter(intensity)
        elif effect_type == "parallax":
            motion_filter = _create_parallax_filter(intensity)
        elif effect_type == "shake":
            motion_filter = _create_shake_filter(intensity)
        else:
            motion_filter = _create_zoom_pan_filter(intensity)
        
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vf", motion_filter,
            "-c:a", "copy",
            "-preset", "medium",
            "-crf", "23",
            output_path
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        logger.info(f"Added motion effects to video: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Failed to add motion effects: {e}")
        return video_path  # Return original video as fallback

def create_multi_angle_video(image_path, audio_path, duration, angles=None):
    """
    Create a video with multiple camera angles from a single image.
    
    Args:
        image_path (str): Path to the source image
        audio_path (str): Path to the audio file
        duration (float): Duration of the video
        angles (list): List of angle configurations
        
    Returns:
        str: Path to the multi-angle video
    """
    logger = logging.getLogger("VidGen.models.video")
    
    if angles is None:
        # Default angles: close-up, medium, wide
        angles = [
            {"zoom": 1.5, "pan_x": 0, "pan_y": -0.1, "duration": duration * 0.3},
            {"zoom": 1.0, "pan_x": 0, "pan_y": 0, "duration": duration * 0.4},
            {"zoom": 0.8, "pan_x": 0, "pan_y": 0.1, "duration": duration * 0.3}
        ]
    
    try:
        import uuid
        output_filename = f"multi_angle_video_{uuid.uuid4().hex[:8]}.mp4"
        output_path = os.path.join(VideoGenConfig.OUTPUT_DIR, "videos", output_filename)
        
        # Create filter for multi-angle effect
        angle_filters = []
        time_offset = 0
        
        for i, angle in enumerate(angles):
            angle_duration = angle["duration"]
            zoom = angle["zoom"]
            pan_x = angle["pan_x"]
            pan_y = angle["pan_y"]
            
            # Create zoompan filter for this angle
            filter_part = f"zoompan=z='{zoom}':x='{pan_x}*iw':y='{pan_y}*ih':d={int(angle_duration * 25)}:s=1280x720"
            
            if i == 0:
                angle_filters.append(f"[0:v]{filter_part}[v{i}]")
            else:
                # For subsequent angles, we need to concatenate
                angle_filters.append(f"[0:v]{filter_part}[v{i}]")
        
        # Concatenate all angle segments
        concat_filter = "".join(f"[v{i}]" for i in range(len(angles)))
        concat_filter += f"concat=n={len(angles)}:v=1:a=0[vout]"
        
        filter_complex = ";".join(angle_filters + [concat_filter])
        
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", image_path,
            "-i", audio_path,
            "-filter_complex", filter_complex,
            "-map", "[vout]",
            "-map", "1:a",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-preset", "medium",
            "-crf", "23",
            "-shortest",
            output_path
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        logger.info(f"Generated multi-angle video: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Failed to create multi-angle video: {e}")
        # Fallback to simple video generation
        return generate_video_segment({
            "narration": "",
            "start": 0,
            "end": duration,
            "character_face": {"face_prompt": "", "seed": 42}
        })

def _build_transition_filter(segments, transition_type, transition_duration):
    """Build FFmpeg filter complex for video transitions."""
    if len(segments) < 2:
        return "[0:v][0:a]copy[out]"
    
    filter_parts = []
    video_inputs = []
    audio_inputs = []
    
    for i in range(len(segments)):
        video_inputs.append(f"[{i}:v]")
        audio_inputs.append(f"[{i}:a]")
    
    if transition_type == "fade":
        # Create fade transitions between segments
        for i in range(len(segments) - 1):
            if i == 0:
                filter_parts.append(f"[0:v][1:v]xfade=transition=fade:duration={transition_duration}:offset=0[v01]")
                filter_parts.append(f"[0:a][1:a]acrossfade=d={transition_duration}[a01]")
            else:
                filter_parts.append(f"[v{i-1:02d}][{i+1}:v]xfade=transition=fade:duration={transition_duration}:offset=0[v{i:02d}{i+1}]")
                filter_parts.append(f"[a{i-1:02d}][{i+1}:a]acrossfade=d={transition_duration}[a{i:02d}{i+1}]")
    
    elif transition_type == "slide":
        # Create slide transitions
        for i in range(len(segments) - 1):
            if i == 0:
                filter_parts.append(f"[0:v][1:v]xfade=transition=slideleft:duration={transition_duration}:offset=0[v01]")
                filter_parts.append(f"[0:a][1:a]acrossfade=d={transition_duration}[a01]")
            else:
                filter_parts.append(f"[v{i-1:02d}][{i+1}:v]xfade=transition=slideleft:duration={transition_duration}:offset=0[v{i:02d}{i+1}]")
                filter_parts.append(f"[a{i-1:02d}][{i+1}:a]acrossfade=d={transition_duration}[a{i:02d}{i+1}]")
    
    else:  # Default to concatenation
        video_concat = "".join(video_inputs) + f"concat=n={len(segments)}:v=1:a=0[vout]"
        audio_concat = "".join(audio_inputs) + f"concat=n={len(segments)}:v=0:a=1[aout]"
        return f"{video_concat};{audio_concat}"
    
    # Final output mapping
    last_index = len(segments) - 2
    filter_parts.append(f"[v{last_index:02d}{last_index+1}][a{last_index:02d}{last_index+1}]concat=n=1:v=1:a=1[out]")
    
    return ";".join(filter_parts)

def _create_zoom_pan_filter(intensity):
    """Create zoom and pan filter for motion effect."""
    zoom_factor = 1 + (intensity * 0.2)  # Zoom from 1.0 to 1.2 max
    return f"zoompan=z='min(zoom+0.0015,{zoom_factor})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1280x720"

def _create_parallax_filter(intensity):
    """Create parallax effect filter."""
    pan_amount = intensity * 50  # Max 50 pixel movement
    return f"crop=1280:720:x='if(gte(t,0),{pan_amount}*sin(t*0.1),0)':y=0"

def _create_shake_filter(intensity):
    """Create camera shake effect filter."""
    shake_amount = intensity * 10  # Max 10 pixel shake
    return f"crop=1280:720:x='{shake_amount}*sin(t*10)':y='{shake_amount}*cos(t*13)'"

def concatenate_videos(video_paths):
    """
    Concatenate multiple video files into one.
    
    Args:
        video_paths (list): List of video file paths
        
    Returns:
        str: Path to the concatenated video
    """
    logger = logging.getLogger("VidGen.models.video")
    
    if not video_paths:
        return None
    
    if len(video_paths) == 1:
        return video_paths[0]
    
    try:
        import uuid
        output_filename = f"concatenated_video_{uuid.uuid4().hex[:8]}.mp4"
        output_path = os.path.join(VideoGenConfig.OUTPUT_DIR, "videos", output_filename)
        
        # Create filter complex for concatenation
        inputs = "".join(f"[{i}:v][{i}:a]" for i in range(len(video_paths)))
        filter_complex = f"{inputs}concat=n={len(video_paths)}:v=1:a=1[outv][outa]"
        
        cmd = ["ffmpeg", "-y"]
        
        # Add input files
        for video_path in video_paths:
            cmd.extend(["-i", video_path])
        
        cmd.extend([
            "-filter_complex", filter_complex,
            "-map", "[outv]",
            "-map", "[outa]",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-preset", "medium",
            "-crf", "23",
            output_path
        ])
        
        subprocess.run(cmd, check=True, capture_output=True)
        logger.info(f"Concatenated {len(video_paths)} videos: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Failed to concatenate videos: {e}")
        return video_paths[0]  # Return first video as fallback
