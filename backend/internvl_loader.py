import sys
import logging
from pathlib import Path
from typing import Tuple, Optional
sys.path.append(str(Path(__file__).parent))
import torch
from transformers import AutoTokenizer, AutoModel
import torchvision.transforms as T
from torchvision.transforms.functional import InterpolationMode
from PIL import Image

# Image Preprocessing Constants
IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)

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

def build_transform(input_size):
    """Build image transformation pipeline."""
    transform = T.Compose([
        T.Lambda(lambda img: img.convert('RGB') if img.mode != 'RGB' else img),
        T.Resize((input_size, input_size), interpolation=InterpolationMode.BICUBIC),
        T.ToTensor(),
        T.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
    ])
    return transform

def find_closest_aspect_ratio(aspect_ratio, target_ratios, width, height, image_size):
    """Find the closest matching aspect ratio for image processing."""
    best_ratio_diff = float('inf')
    best_ratio = (1, 1)
    area = width * height
    for ratio in target_ratios:
        target_aspect_ratio = ratio[0] / ratio[1]
        ratio_diff = abs(aspect_ratio - target_aspect_ratio)
        if ratio_diff < best_ratio_diff:
            best_ratio_diff = ratio_diff
            best_ratio = ratio
        elif ratio_diff == best_ratio_diff:
            if area > 0.5 * image_size * image_size * ratio[0] * ratio[1]:
                best_ratio = ratio
    return best_ratio

def dynamic_preprocess(image, min_num=1, max_num=12, image_size=448, use_thumbnail=False):
    """Dynamically preprocess image based on aspect ratio."""
    orig_width, orig_height = image.size
    aspect_ratio = orig_width / orig_height
    target_ratios = set(
        (i, j) for n in range(min_num, max_num + 1) 
        for i in range(1, n + 1) 
        for j in range(1, n + 1) 
        if i * j <= max_num and i * j >= min_num
    )
    target_ratios = sorted(target_ratios, key=lambda x: x[0] * x[1])
    target_aspect_ratio = find_closest_aspect_ratio(
        aspect_ratio, target_ratios, orig_width, orig_height, image_size)
    
    target_width = image_size * target_aspect_ratio[0]
    target_height = image_size * target_aspect_ratio[1]
    blocks = target_aspect_ratio[0] * target_aspect_ratio[1]
    resized_img = image.resize((target_width, target_height))
    
    processed_images = []
    for i in range(blocks):
        box = (
            (i % (target_width // image_size)) * image_size,
            (i // (target_width // image_size)) * image_size,
            ((i % (target_width // image_size)) + 1) * image_size,
            ((i // (target_width // image_size)) + 1) * image_size
        )
        split_img = resized_img.crop(box)
        processed_images.append(split_img)
    
    if use_thumbnail and len(processed_images) != 1:
        thumbnail_img = image.resize((image_size, image_size))
        processed_images.append(thumbnail_img)
    return processed_images

def load_image(image_file, input_size=448, max_num=12):
    """Load and preprocess image."""
    image = Image.open(image_file).convert('RGB')
    transform = build_transform(input_size=input_size)
    images = dynamic_preprocess(image, image_size=input_size, use_thumbnail=True, max_num=max_num)
    pixel_values = [transform(image) for image in images]
    pixel_values = torch.stack(pixel_values)
    return pixel_values

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
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {device}")
        
        # Load model and tokenizer
        model_path = "OpenGVLab/InternVL2_5-2B-MPO"
        
        model = AutoModel.from_pretrained(
            model_path,
            torch_dtype=torch.bfloat16,
            low_cpu_mem_usage=True,
            use_flash_attn=True,
            trust_remote_code=True
        ).eval().to(device)
        
        tokenizer = AutoTokenizer.from_pretrained(
            model_path, 
            trust_remote_code=True, 
            use_fast=False
        )
        
        logger.info("Successfully loaded InternVL model and tokenizer")
        return model, tokenizer, None, device  # Return None for processor to maintain compatibility
        
    except Exception as e:
        logger.error(f"Error loading InternVL model: {e}")
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
