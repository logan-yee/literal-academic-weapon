import warnings
import logging
import json
from PIL import Image
import torch

# Filter out specific warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
logging.getLogger("transformers").setLevel(logging.ERROR)

# Import LangChain components for prompt building and LLM chaining.
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.llms import Ollama as OllamaLLM

# Import the InternVL model loader and cleanup helpers.
from internvl_loader import load_internvl_model, load_image, cleanup_model

# -------------------------------
# Setup Logging
# -------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# -------------------------------
# Global Model Loading
# -------------------------------
try:
    # Load InternVL and its tokenizer
    internvl_model, tokenizer, device, *_ = load_internvl_model()
    logger.info("InternVL Model loaded successfully")

    # Initialize Llama via Ollama 
    llm = OllamaLLM(model="llama2", temperature=0.3)
    
    # Define output parser
    json_parser = JsonOutputParser()

    # Define a prompt template for classification
    classification_prompt = PromptTemplate(
        input_variables=["extracted_text", "definition"],
        template=(
            "Analyze the following screenshot description:\n"
            "{extracted_text}\n\n"
            "Based on this definition of procrastination:\n"
            "{definition}\n\n"
            "Determine if the screenshot indicates procrastination or productive behavior. "
            "Return your analysis as a JSON object with:\n"
            "  - 'label': either 'procrastination' or 'productive'\n"
            "  - 'score': a confidence score between 0 and 1\n"
            "  - 'reasoning': a brief explanation of your decision.\n\n"
            "JSON Response:"
        )
    )

    # Create modern chain
    classification_chain = (
        RunnablePassthrough() 
        | classification_prompt 
        | llm 
        | json_parser
    )

except Exception as e:
    logger.error(f"Error loading models: {e}")
    raise

# -------------------------------
# Step 1: InternVL OCR Function
# -------------------------------
def internvl_ocr(image_path):
    """
    Loads the image and uses InternVL to generate an image description.
    Focuses on extracting textual content from the screenshot.
    
    :param image_path: Path to the screenshot image.
    :return: A string description of the image.
    """
    try:
        # Process image
        pixel_values = load_image(image_path, max_num=12).to(torch.bfloat16).to(device)
        
        # Create text prompt
        prompt = "<image>\nPlease describe this screenshot in detail, focusing on any visible text content."
        
        # Generate response
        generation_config = dict(max_new_tokens=512, do_sample=True, temperature=0.7)
        response = internvl_model.chat(tokenizer, pixel_values, prompt, generation_config)
        
        logger.info(f"OCR result: {response[:100]}...")
        return response

    except Exception as e:
        logger.error(f"Error in internvl_ocr: {e}")
        raise

    finally:
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

# -------------------------------
# Step 2: Llama Classification Function
# -------------------------------
def llama_classification(ocr_result, definition):
    """
    Uses Llama 2 (via Ollama) to classify the image description.
    
    :param ocr_result: The text output from InternVL.
    :param definition: A string (or JSON string) defining what constitutes procrastination.
    :return: A JSON object with classification details.
    """
    try:
        result = classification_chain.invoke({
            "extracted_text": ocr_result,
            "definition": definition
        })
        logger.info(f"Classification result: {result}")
        return result

    except Exception as e:
        logger.error(f"Error in llama_classification: {e}")
        return {"label": "error", "score": 0.0, "reasoning": f"Error: {e}"}

# -------------------------------
# Pipeline Runner Function
# -------------------------------
def run_pipeline(image_path, definition):
    """
    Runs the pipeline by first extracting text from the image and then classifying the result.
    
    :param image_path: Path to the screenshot image.
    :param definition: User input defining what constitutes procrastination.
    :return: Final classification result as a JSON object.
    """
    logger.info("=== Starting Pipeline ===")
    logger.info(f"Image path: {image_path}")
    logger.info(f"Definition: {definition}")

    # Step 1: Extract text description from the image.
    ocr_result = internvl_ocr(image_path)
    print("\nInternVL Output:", ocr_result, "\n")
    
    # Step 2: Classify the extracted text.
    classification_result = llama_classification(ocr_result, definition)

    logger.info("=== Pipeline Complete ===")
    return classification_result

# -------------------------------
# Main Execution
# -------------------------------
if __name__ == '__main__':
    # Example usage:
    image_path = "backend/screenshots/screenshot_2025-01-01_18-33-51.png"
    
    # Provide a JSON string (or plain text) that defines what constitutes procrastination.
    definition = '{"definition": "Procrastination includes social media, entertainment, and non-study activities."}'
    
    # Run the pipeline synchronously.
    final_output = run_pipeline(image_path, definition)
    print("Final Output:", final_output)
    
    # Cleanup resources.
    cleanup_model(internvl_model)
