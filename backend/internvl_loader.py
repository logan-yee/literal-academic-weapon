import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))  # Add the current directory to Python path
from utils.torch_setup import setup_torch
import torch
from transformers import AutoTokenizer, AutoModel, AutoProcessor

def load_internvl_model():
    """
    Loads the InternVL2.5-2B-MPO model with optimized CUDA settings.
    Returns the model, tokenizer and processor.
    """
    # Set up CUDA
    device, is_cuda_available, cuda_device_name = setup_torch()
    
    path = "OpenGVLab/InternVL2_5-2B-MPO"
    
    # Configure model settings based on CUDA availability
    model_kwargs = {
        "torch_dtype": torch.bfloat16,
        "low_cpu_mem_usage": True,
        "trust_remote_code": True
    }
    
    if is_cuda_available:
        model_kwargs["use_flash_attn"] = True
        model_kwargs["device_map"] = "auto"  # Automatically manage model placement
    
    # Load the model with optimized settings
    model = AutoModel.from_pretrained(path, **model_kwargs)
    
    if is_cuda_available:
        model = model.eval().cuda()
    else:
        model = model.eval()
    
    # Load the tokenizer and processor with trust_remote_code=True
    tokenizer = AutoTokenizer.from_pretrained(path, trust_remote_code=True, use_fast=False)
    processor = AutoProcessor.from_pretrained(path, trust_remote_code=True)
    
    return model, tokenizer, processor, device
