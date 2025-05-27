import os
import logging
from vidgen.core.config import VideoGenConfig
import threading

_image_pipeline = None
_image_pipeline_lock = threading.Lock()

def get_image_pipeline():
    global _image_pipeline
    with _image_pipeline_lock:
        if _image_pipeline is None:
            try:
                from diffusers import StableDiffusionPipeline
                import torch
                _image_pipeline = StableDiffusionPipeline.from_pretrained(
                    VideoGenConfig.STABLE_DIFFUSION_MODEL,
                    torch_dtype=torch.float16
                )
                _image_pipeline = _image_pipeline.to("cuda" if torch.cuda.is_available() else "cpu")
            except Exception as e:
                logging.getLogger("VidGen.models.image").error(f"Failed to load Stable Diffusion pipeline: {e}")
                raise
        return _image_pipeline

def generate_character_image(image_command, seed=42):
    """
    Generate a character image from the given prompt.
    
    Args:
        image_command (str or dict): Image generation prompt or command dictionary
        seed (int): Random seed for reproducible generation
        
    Returns:
        str: Path to the generated image file
    """
    logger = logging.getLogger("VidGen.models.image")
    
    # Handle both string prompts and command dictionaries
    if isinstance(image_command, dict):
        prompt = image_command.get("face_prompt", image_command.get("character", ""))
        character_name = image_command.get("character", "unknown")
        seed = image_command.get("seed", seed)
    else:
        prompt = str(image_command) if image_command else ""
        character_name = "character"
    
    if not prompt.strip():
        logger.warning("Empty image prompt provided")
        return "placeholder_image.png"
    
    try:
        import torch
        import uuid
        
        # Generate unique filename based on character and seed
        safe_char_name = "".join(c for c in character_name if c.isalnum() or c in ('-', '_'))
        output_filename = f"character_{safe_char_name}_{uuid.uuid4().hex[:8]}.png"
        output_path = os.path.join(VideoGenConfig.OUTPUT_DIR, "images", output_filename)
        
        # Ensure images directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        generator = torch.Generator(device="cuda" if torch.cuda.is_available() else "cpu").manual_seed(int(seed))
        pipe = get_image_pipeline()
        
        logger.info(f"Generating image for: {prompt[:50]}... (seed: {seed})")
        result = pipe(prompt, generator=generator)
        image = result.images[0]
        
        image.save(output_path)
        logger.info(f"Character image generated: {output_path}")
        
        return output_path
        
    except Exception as e:
        logger.error(f"Error generating image for prompt '{prompt}': {e}")
        return "placeholder_image.png"
