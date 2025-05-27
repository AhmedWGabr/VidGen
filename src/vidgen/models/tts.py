import os
import logging
from vidgen.core.config import VideoGenConfig

def generate_tts_audio(tts_command):
    """
    Generate text-to-speech audio from the given text command.
    
    Args:
        tts_command (str): Text to convert to speech
        
    Returns:
        str: Path to the generated audio file
    """
    logger = logging.getLogger("VidGen.models.tts")
    
    if not tts_command or tts_command.strip() == "":
        logger.warning("Empty TTS command provided")
        return None
    
    try:
        from bark import SAMPLE_RATE, generate_audio
        import scipy.io.wavfile
        import uuid
        
        # Generate unique filename
        output_filename = f"tts_audio_{uuid.uuid4().hex[:8]}.wav"
        output_path = os.path.join(VideoGenConfig.OUTPUT_DIR, "audio", output_filename)
        
        # Ensure audio directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        logger.info(f"Generating TTS for: {tts_command[:50]}...")
        audio_array = generate_audio(tts_command)
        
        scipy.io.wavfile.write(output_path, SAMPLE_RATE, audio_array)
        logger.info(f"TTS audio generated: {output_path}")
        
        return output_path
        
    except ImportError as e:
        logger.error(f"Bark TTS not available: {e}")
        return None
    except Exception as e:
        logger.error(f"Error generating TTS audio: {e}")
        return None
