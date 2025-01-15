from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from pathlib import Path

# Utility function that loads a model from models folder if available otherwise from huggingface transformers
def load_llm_model(model_name, models_dir):
    models_dir = Path(models_dir).resolve()
    model_dir = models_dir / model_name.split('/')[-1]
    
    should_download = not (model_dir.exists() and any(model_dir.iterdir()))
    load_path = model_name if should_download else model_dir
    
    device_config = _setup_device_config()
    
    try:
        models_dir.mkdir(parents=True, exist_ok=True)
        
        tokenizer = AutoTokenizer.from_pretrained(load_path)
        
        model_config = {
            "torch_dtype": device_config["torch_dtype"],
            "low_cpu_mem_usage": True,
            "use_safetensors": True,
            "device_map": device_config["device"]
        }
        
        model = AutoModelForCausalLM.from_pretrained(load_path, **model_config)
        
        if should_download:
            model.save_pretrained(model_dir)
            tokenizer.save_pretrained(model_dir)

        return model, tokenizer

    except Exception as e:
        raise RuntimeError(f"Failed to load model: {str(e)}")

# Configure device and dtype settings based on available hardware.
def _setup_device_config() -> dict:
    cuda_available = torch.cuda.is_available()
    device = "cuda:0" if cuda_available else "cpu"
    
    if cuda_available and torch.cuda.is_bf16_supported():
        torch_dtype = torch.bfloat16
    elif cuda_available:
        torch_dtype = torch.float16
    else:
        torch_dtype = torch.float32
        
    return {
        "device": device,
        "torch_dtype": torch_dtype
    }
    