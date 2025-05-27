"""
Audio generation module for VidGen.

This module provides comprehensive audio generation capabilities including:
- Procedural background audio synthesis (ambient, music, effects)
- Audio command analysis and type detection
- Multi-track audio mixing with FFmpeg
- Frequency pattern generation for different audio styles

The module supports various audio types and automatically generates appropriate
soundscapes based on text descriptions.
"""

import os
import logging
import subprocess
import re
import random
import math
from typing import Tuple, Optional
from vidgen.core.config import VideoGenConfig

def generate_background_audio(audio_command: str) -> str:
    """
    Generate background audio/music from audio command description.
    
    Supports different audio types: ambient, music, and sound effects.
    Uses procedural synthesis with FFmpeg to create contextually appropriate audio.
    
    Args:
        audio_command (str): Description of the background audio to generate.
                           Examples: "melancholy orchestral music", "forest ambience", 
                           "upbeat electronic music", "silence"
        
    Returns:
        str: Path to the generated audio file (.wav format)
        
    Raises:
        AudioGenerationError: If audio generation fails
        
    Example:
        >>> audio_path = generate_background_audio("peaceful nature sounds")
        >>> print(audio_path)  # outputs/audio/background_audio_abc123.wav
    """
    logger = logging.getLogger("VidGen.models.audio")
    
    if not audio_command or audio_command.strip() == "":
        logger.info("No audio command provided, creating silent audio")
        audio_command = "silence"
    
    try:
        import uuid
        output_filename = f"background_audio_{uuid.uuid4().hex[:8]}.wav"
        output_path = os.path.join(VideoGenConfig.OUTPUT_DIR, "audio", output_filename)
        
        # Ensure audio directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Analyze audio command to determine type and parameters
        audio_type, duration, frequency_pattern = _analyze_audio_command(audio_command)
        
        if audio_type == "silence":
            return _generate_silence(output_path, duration)
        elif audio_type == "ambient":
            return _generate_ambient_audio(output_path, audio_command, duration, frequency_pattern)
        elif audio_type == "music":
            return _generate_music_audio(output_path, audio_command, duration)
        else:
            # Default to ambient for unknown types
            return _generate_ambient_audio(output_path, audio_command, duration, frequency_pattern)
        
    except Exception as e:
        logger.error(f"Error generating background audio: {e}")
        # Return a fallback silent audio file
        fallback_path = os.path.join(VideoGenConfig.OUTPUT_DIR, "audio", "silence_fallback.wav")
        try:
            return _generate_silence(fallback_path, 5)
        except:
            return None

def _analyze_audio_command(audio_command):
    """
    Analyze audio command to determine type, duration, and characteristics.
    
    Returns:
        tuple: (audio_type, duration, frequency_pattern)
    """
    command_lower = audio_command.lower()
    
    # Default values
    audio_type = "ambient"
    duration = 5.0
    frequency_pattern = "low"
    
    # Determine audio type
    if "silence" in command_lower or "quiet" in command_lower:
        audio_type = "silence"
    elif any(word in command_lower for word in ["music", "melody", "song", "tune"]):
        audio_type = "music"
    elif any(word in command_lower for word in ["ambient", "atmosphere", "background", "noise"]):
        audio_type = "ambient"
    
    # Extract duration if specified
    duration_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:sec|second|s)', command_lower)
    if duration_match:
        duration = float(duration_match.group(1))
    
    # Determine frequency characteristics
    if any(word in command_lower for word in ["deep", "low", "bass", "rumble"]):
        frequency_pattern = "low"
    elif any(word in command_lower for word in ["high", "bright", "chirp", "bell"]):
        frequency_pattern = "high"
    elif any(word in command_lower for word in ["middle", "mid", "voice"]):
        frequency_pattern = "mid"
    else:
        frequency_pattern = "mixed"
    
    return audio_type, duration, frequency_pattern

def _generate_silence(output_path, duration):
    """Generate silent audio file."""
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"anullsrc=r=44100:cl=mono",
        "-t", str(duration),
        "-q:a", "9",
        "-acodec", "pcm_s16le",
        output_path
    ]
    
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path

def _generate_ambient_audio(output_path, description, duration, frequency_pattern):
    """
    Generate ambient audio using procedural sound synthesis.
    Creates atmospheric sounds based on description.
    """
    logger = logging.getLogger("VidGen.models.audio")
    
    try:
        # Create base noise and filter it based on description
        if "laboratory" in description.lower() or "tech" in description.lower():
            # Tech ambient with occasional beeps
            filter_complex = _create_tech_ambient_filter(duration, frequency_pattern)
        elif "nature" in description.lower() or "forest" in description.lower():
            # Nature ambient
            filter_complex = _create_nature_ambient_filter(duration, frequency_pattern)
        elif "urban" in description.lower() or "city" in description.lower():
            # Urban ambient
            filter_complex = _create_urban_ambient_filter(duration, frequency_pattern)
        else:
            # Generic ambient
            filter_complex = _create_generic_ambient_filter(duration, frequency_pattern)
        
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", filter_complex,
            "-t", str(duration),
            "-q:a", "4",
            "-acodec", "pcm_s16le",
            output_path
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        logger.info(f"Generated ambient audio: {output_path}")
        return output_path
        
    except Exception as e:
        logger.warning(f"Failed to generate ambient audio, falling back to silence: {e}")
        return _generate_silence(output_path, duration)

def _generate_music_audio(output_path, description, duration):
    """
    Generate simple musical audio using tone synthesis.
    Creates basic melodies or harmonic content.
    """
    logger = logging.getLogger("VidGen.models.audio")
    
    try:
        # Determine musical characteristics from description
        tempo = "slow" if any(word in description.lower() for word in ["slow", "calm", "peaceful"]) else "medium"
        key = "minor" if any(word in description.lower() for word in ["sad", "dark", "melancholy"]) else "major"
        
        # Create musical filter
        filter_complex = _create_music_filter(duration, tempo, key)
        
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", filter_complex,
            "-t", str(duration),
            "-q:a", "4",
            "-acodec", "pcm_s16le",
            output_path
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        logger.info(f"Generated music audio: {output_path}")
        return output_path
        
    except Exception as e:
        logger.warning(f"Failed to generate music audio, falling back to ambient: {e}")
        return _generate_ambient_audio(output_path, description, duration, "mixed")

def _create_tech_ambient_filter(duration, frequency_pattern):
    """Create filter for tech/laboratory ambient sounds."""
    if frequency_pattern == "low":
        base_freq = 60
        noise_type = "brownian"
    elif frequency_pattern == "high":
        base_freq = 800
        noise_type = "white"
    else:
        base_freq = 200
        noise_type = "pink"
    
    # Add occasional beeps
    beep_freq = random.randint(800, 1200)
    return f"anoisesrc=c=pink:r=44100:a=0.1,highpass=f={base_freq},lowpass=f={base_freq*10}[base];sine=f={beep_freq}:d=0.1[beep];[base][beep]amix=inputs=2:duration=longest:weights=1 0.2"

def _create_nature_ambient_filter(duration, frequency_pattern):
    """Create filter for nature ambient sounds."""
    if frequency_pattern == "low":
        return "anoisesrc=c=brownian:r=44100:a=0.05,highpass=f=20,lowpass=f=400"
    elif frequency_pattern == "high":
        return "anoisesrc=c=white:r=44100:a=0.03,highpass=f=2000,lowpass=f=8000"
    else:
        return "anoisesrc=c=pink:r=44100:a=0.04,highpass=f=100,lowpass=f=2000"

def _create_urban_ambient_filter(duration, frequency_pattern):
    """Create filter for urban ambient sounds."""
    return "anoisesrc=c=pink:r=44100:a=0.06,highpass=f=80,lowpass=f=1500"

def _create_generic_ambient_filter(duration, frequency_pattern):
    """Create filter for generic ambient sounds."""
    if frequency_pattern == "low":
        return "anoisesrc=c=brownian:r=44100:a=0.04,highpass=f=40,lowpass=f=300"
    elif frequency_pattern == "high":
        return "anoisesrc=c=white:r=44100:a=0.02,highpass=f=1000,lowpass=f=5000"
    else:
        return "anoisesrc=c=pink:r=44100:a=0.03,highpass=f=200,lowpass=f=2000"

def _create_music_filter(duration, tempo, key):
    """Create filter for simple musical content."""
    # Create a simple chord progression using sine waves
    if key == "major":
        # C major chord (C, E, G)
        frequencies = [261.63, 329.63, 392.00]  # C4, E4, G4
    else:
        # C minor chord (C, Eb, G)
        frequencies = [261.63, 311.13, 392.00]  # C4, Eb4, G4
    
    # Create individual sine waves and mix them
    sine_filters = []
    for i, freq in enumerate(frequencies):
        volume = 0.3 - (i * 0.05)  # Decrease volume for higher notes
        sine_filters.append(f"sine=f={freq}:d={duration}:volume={volume}")
    
    # Mix the sine waves
    if len(sine_filters) == 3:
        return f"{sine_filters[0]}[s1];{sine_filters[1]}[s2];{sine_filters[2]}[s3];[s1][s2][s3]amix=inputs=3:duration=longest"
    else:
        return sine_filters[0]

def mix_audio(tracks, levels=None, output_path=None):
    """
    Mix multiple audio tracks with specified levels.
    
    Args:
        tracks (list): List of audio file paths
        levels (list): List of volume levels (0.0 to 1.0) for each track
        output_path (str): Output path for mixed audio
        
    Returns:
        str: Path to the mixed audio file
    """
    logger = logging.getLogger("VidGen.models.audio")
    
    if not tracks:
        return None
    
    if len(tracks) == 1:
        return tracks[0]
    
    if levels is None:
        levels = [1.0] * len(tracks)
    
    if output_path is None:
        import uuid
        output_filename = f"mixed_audio_{uuid.uuid4().hex[:8]}.wav"
        output_path = os.path.join(VideoGenConfig.OUTPUT_DIR, "audio", output_filename)
    
    try:
        # Build FFmpeg command for mixing
        cmd = ["ffmpeg", "-y"]
        
        # Add input files
        for track in tracks:
            cmd.extend(["-i", track])
        
        # Build filter complex for mixing
        filter_parts = []
        for i, level in enumerate(levels):
            filter_parts.append(f"[{i}:a]volume={level}[a{i}]")
        
        mix_inputs = "".join(f"[a{i}]" for i in range(len(tracks)))
        filter_parts.append(f"{mix_inputs}amix=inputs={len(tracks)}:duration=longest[out]")
        
        filter_complex = ";".join(filter_parts)
        
        cmd.extend([
            "-filter_complex", filter_complex,
            "-map", "[out]",
            "-q:a", "4",
            "-acodec", "pcm_s16le",
            output_path
        ])
        
        subprocess.run(cmd, check=True, capture_output=True)
        logger.info(f"Mixed {len(tracks)} audio tracks: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Failed to mix audio tracks: {e}")
        return tracks[0]  # Return first track as fallback
