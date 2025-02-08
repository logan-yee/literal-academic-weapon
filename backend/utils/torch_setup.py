import torch

def setup_torch():
    """
    Configure PyTorch with CUDA settings and return device information.
    Returns:
        device: torch.device
        is_cuda_available: bool
        cuda_device_name: str or None
    """
    # Check CUDA availability
    is_cuda_available = torch.cuda.is_available()
    
    if is_cuda_available:
        # Get the current CUDA device
        cuda_device = torch.cuda.current_device()
        cuda_device_name = torch.cuda.get_device_name(cuda_device)
        
        # Set device to CUDA
        device = torch.device("cuda")
        
        # Print CUDA information
        print(f"CUDA is available. Using device: {cuda_device_name}")
        print(f"CUDA version: {torch.version.cuda}")
        print(f"Total GPU memory: {torch.cuda.get_device_properties(device).total_memory / 1e9:.2f} GB")
    else:
        device = torch.device("cpu")
        cuda_device_name = None
        print("CUDA is not available. Using CPU.")
    
    return device, is_cuda_available, cuda_device_name