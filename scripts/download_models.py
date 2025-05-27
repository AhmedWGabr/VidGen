#!/usr/bin/env python
"""
Script to download and cache all required models for VidGen.
"""
import os
import sys
import logging
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('model_download')

def download_stable_diffusion():
    """Download and cache the Stable Diffusion model."""
    try:
        from diffusers import StableDiffusionPipeline
        import torch
        
        logger.info("Downloading Stable Diffusion model...")
        
        # Use the CPU for setup to avoid CUDA out-of-memory errors
        model_id = "runwayml/stable-diffusion-v1-5"
        pipeline = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )
        
        # Save model to disk to ensure it's cached
        if torch.cuda.is_available():
            pipeline = pipeline.to("cuda")
            # Generate a small test image to verify setup
            _ = pipeline("A test image to verify Stable Diffusion setup")
            logger.info("Successfully downloaded and verified Stable Diffusion model with GPU acceleration")
        else:
            logger.info("Successfully downloaded Stable Diffusion model for CPU use (GPU recommended for production)")
            
    except Exception as e:
        logger.error(f"Error downloading Stable Diffusion model: {e}")
        return False
    
    return True

def download_bark_tts():
    """Download and cache the Bark TTS model."""
    try:
        logger.info("Downloading Bark TTS model...")
        from bark import preload_models
        
        # Preload Bark models
        preload_models()
        
        # Try a simple generation to verify setup
        from bark import generate_audio, SAMPLE_RATE
        import scipy.io.wavfile as wavfile
        
        logger.info("Testing Bark TTS with a short generation...")
        audio = generate_audio("This is a test for Bark text to speech.")
        
        # Save test file
        test_dir = Path("./outputs/temp")
        test_dir.mkdir(exist_ok=True, parents=True)
        wavfile.write(test_dir / "bark_test.wav", SAMPLE_RATE, audio)
        
        logger.info("Successfully downloaded and tested Bark TTS model")
        
    except Exception as e:
        logger.error(f"Error downloading Bark TTS model: {e}")
        return False
    
    return True

def main():
    """Main function to download all models."""
    logger.info("Starting download of all required models for VidGen")
    
    # Create necessary directories
    os.makedirs("outputs/temp", exist_ok=True)
    
    success = True
    
    # Download Stable Diffusion
    if not download_stable_diffusion():
        success = False
    
    # Download Bark TTS
    if not download_bark_tts():
        success = False
    
    if success:
        logger.info("All models downloaded successfully!")
    else:
        logger.warning("Some models failed to download. Check the logs for details.")
        
if __name__ == "__main__":
    main()
