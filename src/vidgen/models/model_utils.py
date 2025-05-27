# Utility functions for models
import logging
import os
import torch
from pathlib import Path
import shutil
from typing import Dict, Optional
from vidgen.core.config import VideoGenConfig

logger = logging.getLogger("VidGen.models.utils")

def check_cuda_availability():
    """
    Check if CUDA is available for GPU acceleration.
    
    Returns:
        bool: True if CUDA is available, False otherwise
    """
    is_available = torch.cuda.is_available()
    if is_available:
        device_count = torch.cuda.device_count()
        device_name = torch.cuda.get_device_name(0) if device_count > 0 else "Unknown"
        logger.info(f"CUDA is available: {device_count} device(s), using {device_name}")
    else:
        logger.warning("CUDA is not available, using CPU only. This will significantly slow down processing.")
    
    return is_available

def check_model_cache(model_name, cache_dir=None):
    """
    Check if model exists in the cache directory.
    
    Args:
        model_name (str): Name of the model to check
        cache_dir (str, optional): Path to cache directory. Defaults to ~/.cache/huggingface.
        
    Returns:
        bool: True if model exists in cache, False otherwise
    """
    if cache_dir is None:
        cache_dir = os.path.expanduser("~/.cache/huggingface/models")
    
    # Convert model name to directory format (replace / with --)
    safe_model_name = model_name.replace("/", "--")
    model_path = Path(cache_dir) / safe_model_name
    
    return model_path.exists()

def download_model(model_name, cache_dir=None):
    """
    Force download of a model to cache.
    
    Args:
        model_name (str): Name of the model to download
        cache_dir (str, optional): Path to cache directory
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from huggingface_hub import snapshot_download
        snapshot_download(repo_id=model_name, cache_dir=cache_dir)
        return True
    except Exception as e:
        logger.error(f"Failed to download model {model_name}: {e}")
        return False

def optimize_model_memory(model):
    """
    Apply memory optimizations to a PyTorch model.
    
    Args:
        model (torch.nn.Module): Model to optimize
        
    Returns:
        torch.nn.Module: Optimized model
    """
    if check_cuda_availability():
        # Use half-precision floating point
        model = model.half()
        
        # Enable model efficiency features
        if hasattr(model, "enable_attention_slicing"):
            model.enable_attention_slicing()
            
        if hasattr(model, "enable_sequential_cpu_offload"):
            model.enable_sequential_cpu_offload()
            
        if hasattr(model, "enable_model_cpu_offload"):
            model.enable_model_cpu_offload()
    
    return model

def clear_model_cache(model=None):
    """
    Clear GPU memory cache.
    
    Args:
        model (torch.nn.Module, optional): Model to unload from memory
    """
    if model is not None:
        del model
    
    # Empty CUDA cache
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        logger.debug("CUDA cache cleared")

def backup_model_weights(model_path, backup_dir):
    """
    Create a backup of model weights.
    
    Args:
        model_path (str): Path to model weights file
        backup_dir (str): Directory to store backups
    """
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir, exist_ok=True)
    
    model_name = os.path.basename(model_path)
    backup_path = os.path.join(backup_dir, f"{model_name}.bak")
    
    try:
        shutil.copy2(model_path, backup_path)
        logger.info(f"Model backup created: {backup_path}")
    except Exception as e:
        logger.error(f"Failed to create model backup: {e}")

def setup_huggingface_auth():
    """
    Set up Hugging Face authentication in environment variables.
    
    This ensures that the Hugging Face Hub library can access models
    using the configured token from VideoGenConfig.
    """
    if VideoGenConfig.HUGGINGFACE_TOKEN:
        # Set all possible HF token environment variables
        os.environ["HUGGINGFACE_HUB_TOKEN"] = VideoGenConfig.HUGGINGFACE_TOKEN
        os.environ["HF_TOKEN"] = VideoGenConfig.HUGGINGFACE_TOKEN
        os.environ["HUGGINGFACE_TOKEN"] = VideoGenConfig.HUGGINGFACE_TOKEN
        logger.info("Hugging Face authentication configured")
    else:
        logger.debug("No Hugging Face token configured - using public model access only")

def validate_model_access(model_name: str) -> Dict[str, bool]:
    """
    Validate that a model can be accessed with current authentication.
    
    Args:
        model_name: Name of the model to validate
        
    Returns:
        dict: Validation results including access status and error info
    """
    validation = {
        "accessible": False,
        "requires_auth": False,
        "error": None
    }
    
    try:
        # Setup auth before testing
        setup_huggingface_auth()
        
        # Try to access model info (lightweight check)
        from huggingface_hub import model_info
        info = model_info(model_name, token=VideoGenConfig.HUGGINGFACE_TOKEN)
        validation["accessible"] = True
        validation["requires_auth"] = info.private if hasattr(info, 'private') else False
        
    except ImportError:
        validation["error"] = "huggingface_hub not installed"
    except Exception as e:
        validation["error"] = str(e)
        if "401" in str(e) or "authentication" in str(e).lower():
            validation["requires_auth"] = True
            
    return validation
