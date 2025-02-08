import sys
import logging
from pathlib import Path
from typing import Tuple, Optional
sys.path.append(str(Path(__file__).parent))
from utils.torch_setup import setup_torch
import torch
from transformers import AutoTokenizer, AutoModel, AutoProcessor

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('internvl.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ModelLoadError(Exception):
    """Custom exception for model loading errors"""
    pass

def check_gpu_memory() -> Tuple[float, float]:
    """
    Check GPU memory usage.
    Returns:
        Tuple of (allocated_memory_gb, total_memory_gb)
    """
    if torch.cuda.is_available():
        allocated = torch.cuda.memory_allocated() / 1e9  # Convert to GB
        total = torch.cuda.get_device_properties(0).total_memory / 1e9
        return allocated, total
    return 0.0, 0.0

def load_internvl_model():
    """
    Loads and optimizes the InternVL2.5-2B-MPO model specifically for image analysis and chat.
    Returns:
        model: Optimized model for chat-based image analysis
        tokenizer: Tokenizer configured for the model
        processor: Image processor
        device: torch.device for computation
    Raises:
        ModelLoadError: If model loading fails
        RuntimeError: If CUDA errors occur
        Exception: For other unexpected errors
    """
    try:
        logger.info("Starting model loading process...")
        
        # Set up CUDA
        device, is_cuda_available, cuda_device_name = setup_torch()
        logger.info(f"CUDA available: {is_cuda_available}, Device: {cuda_device_name}")
        
        if is_cuda_available:
            allocated_mem, total_mem = check_gpu_memory()
            logger.info(f"Initial GPU Memory - Allocated: {allocated_mem:.2f}GB, Total: {total_mem:.2f}GB")
        
        path = "OpenGVLab/InternVL2_5-2B-MPO"
        
        # Model configuration
        model_kwargs = {
            "torch_dtype": torch.bfloat16,
            "low_cpu_mem_usage": True,
            "trust_remote_code": True
        }
        
        if is_cuda_available:
            model_kwargs.update({
                "use_flash_attn": True,
                "device_map": "auto",
                "max_memory": None,
                "offload_folder": "offload"
            })
            logger.info(f"Using CUDA optimizations with settings: {model_kwargs}")
        
        # Load model with error handling
        try:
            logger.info("Loading model...")
            model = AutoModel.from_pretrained(path, **model_kwargs)
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise ModelLoadError(f"Model loading failed: {str(e)}")
        
        if is_cuda_available:
            try:
                model = model.eval().cuda()
                torch.backends.cudnn.benchmark = True
                torch.backends.cuda.matmul.allow_tf32 = True
                logger.info("Model moved to CUDA and optimizations enabled")
            except RuntimeError as e:
                logger.error(f"CUDA error: {str(e)}")
                raise
        else:
            model = model.eval()
        
        # Load tokenizer
        try:
            logger.info("Loading tokenizer...")
            tokenizer = AutoTokenizer.from_pretrained(
                path,
                trust_remote_code=True,
                use_fast=False,
                model_max_length=512
            )
            logger.info("Tokenizer loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load tokenizer: {str(e)}")
            raise ModelLoadError(f"Tokenizer loading failed: {str(e)}")
        
        # Load processor
        try:
            logger.info("Loading processor...")
            processor = AutoProcessor.from_pretrained(
                path,
                trust_remote_code=True,
                do_resize=True,
                size={"height": 224, "width": 224},
                do_normalize=True
            )
            logger.info("Processor loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load processor: {str(e)}")
            raise ModelLoadError(f"Processor loading failed: {str(e)}")
        
        # Pre-warm model
        if is_cuda_available:
            try:
                logger.info("Pre-warming model...")
                dummy_input = torch.zeros(1, 3, 224, 224, device=device, dtype=torch.bfloat16)
                with torch.no_grad():
                    _ = model(dummy_input)
                logger.info("Model pre-warming completed")
            except Exception as e:
                logger.warning(f"Pre-warming failed (non-critical): {str(e)}")
            
            # Log final memory usage
            allocated_mem, total_mem = check_gpu_memory()
            logger.info(f"Final GPU Memory - Allocated: {allocated_mem:.2f}GB, Total: {total_mem:.2f}GB")
        
        return model, tokenizer, processor, device
        
    except Exception as e:
        logger.error(f"Unexpected error during model loading: {str(e)}", exc_info=True)
        raise

def cleanup_model(model: Optional[AutoModel] = None) -> None:
    """
    Cleanup function to free GPU memory with error handling.
    Args:
        model: The model to cleanup (optional)
    """
    try:
        logger.info("Starting model cleanup...")
        if model is not None and hasattr(model, 'cuda') and torch.cuda.is_available():
            initial_mem, total_mem = check_gpu_memory()
            logger.info(f"Initial cleanup memory - Allocated: {initial_mem:.2f}GB")
            
            model.cpu()
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
            
            final_mem, _ = check_gpu_memory()
            logger.info(f"Final cleanup memory - Allocated: {final_mem:.2f}GB")
            logger.info(f"Freed approximately {max(0, initial_mem - final_mem):.2f}GB of GPU memory")
    except Exception as e:
        logger.error(f"Error during model cleanup: {str(e)}", exc_info=True)
        raise

def get_model_info(model: AutoModel) -> dict:
    """
    Get information about the model's configuration and memory usage.
    Args:
        model: The loaded model
    Returns:
        dict containing model information
    """
    try:
        info = {
            "model_type": type(model).__name__,
            "parameters": sum(p.numel() for p in model.parameters()),
            "device": next(model.parameters()).device,
            "dtype": next(model.parameters()).dtype,
        }
        
        if torch.cuda.is_available():
            allocated_mem, total_mem = check_gpu_memory()
            info.update({
                "gpu_memory_allocated_gb": allocated_mem,
                "gpu_memory_total_gb": total_mem,
                "cuda_device": torch.cuda.get_device_name(0)
            })
        
        return info
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}", exc_info=True)
        return {"error": str(e)}
