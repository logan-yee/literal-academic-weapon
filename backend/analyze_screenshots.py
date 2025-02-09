import warnings
import logging
import json
import torch
from datetime import datetime
import os
import time
from screenshot_taker import capture_screenshot

# Import the voice notification module
from voice_notification import speak

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
from utils.internvl_loader import load_internvl_model, load_image, cleanup_model

# At the top of the file, update the logging configuration
import logging

# Clear any existing handlers to prevent duplication
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Configure logging once
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('analyze.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def create_definition(study_topic: str) -> str:
    """
    Creates a definition string combining the base procrastination definition
    with the user's specific study topic.
    
    Args:
        study_topic: The topic the user should be studying/working on
    """
    base_definition = "Procrastination includes social media, entertainment, "
    return (f'{{"definition": "{base_definition} and any activities unrelated to {study_topic}. '
            f'Productive behavior includes activities related to studying/working on {study_topic}"}}')

# -------------------------------
# Global Model Loading
# -------------------------------
try:
    # Load InternVL and its tokenizer
    internvl_model, tokenizer, device, *_ = load_internvl_model()
    logger.info("InternVL Model loaded successfully")

    # Initialize Llama via Ollama 
    llm = OllamaLLM(model="llama3", temperature=0.3)
    
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
            "Focus on analyzing the primary content of the screenshot. Be very strict with your analysis. Determine if the screenshot indicates procrastination or productive behavior, based on the definition of procrastination."
            "Return your analysis as a JSON object with:\n"
            "  - 'label': either 'procrastination' or 'productive'\n"
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
    Uses Llama 3 (via Ollama) to classify the image description.
    
    :param ocr_result: The text output from InternVL.
    :param definition: A string (or JSON string) defining what constitutes procrastination.
    :return: A JSON object with classification details.
    """
    try:
        # Get classification from Llama
        result = classification_chain.invoke({
            "extracted_text": ocr_result,
            "definition": definition
        })
        
        # Format the result in the desired structure
        formatted_result = [{
    
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Content": ocr_result[:100],  # First 100 chars of content
            "Justification": result.get("reasoning", "No reasoning provided"),
            "Verdict": result.get("label") == "procrastination"
        }]

        # Create analyses directory if it doesn't exist
        os.makedirs("analyses", exist_ok=True)
        
        # Generate filename with timestamp
        filename = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join("analyses", filename)
        
        # Save to JSON file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(formatted_result, f, indent=4)
            
        logger.info(f"Analysis saved to {filepath}")
        return formatted_result

    except Exception as e:
        logger.error(f"Error in llama_classification: {e}")
        return [{
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Content": "Error processing content",
            "Justification": f"Error: {str(e)}",
            "Verdict": False
        }]

# -------------------------------
# Pipeline Runner Function
# -------------------------------
def run_pipeline(image_path, definition):
    """
    Runs the pipeline by first extracting text from the image and then classifying the result.
    """
    logger.info("=== Starting Pipeline ===")
    logger.info(f"Image path: {image_path}")
    logger.info(f"Definition: {definition}")

    # Step 1: Extract text description from the image
    ocr_result = internvl_ocr(image_path)
    logger.debug(f"InternVL Output: {ocr_result}")  # Changed to debug level
    
    # Step 2: Classify the extracted text
    classification_result = llama_classification(ocr_result, definition)
    logger.info(f"Classification result: {classification_result}")

    # Check if procrastination was detected
    if classification_result[0]["Verdict"]:
        logger.info("Procrastination detected - triggering voice notification")
        speak("You have been caught procrastinating, please look at the schedule your AI assistant to make you an academic weapon.")
    else:
        logger.info("No procrastination detected - no voice notification")

    logger.info("=== Pipeline Complete ===")
    return classification_result

# -------------------------------
# Get Latest Screenshot Function
# -------------------------------
def get_latest_screenshot():
    """
    Captures a new screenshot and gets its path.
    Returns:
        str: Path to the captured screenshot, or None if failed
    """
    try:
        # Capture new screenshot
        screenshot_path = capture_screenshot()
        logger.info(f"New screenshot captured: {screenshot_path}")
        
        if not os.path.exists(screenshot_path):
            logger.error(f"Screenshot was not created: {screenshot_path}")
            return None
            
        return screenshot_path
        
    except Exception as e:
        logger.error(f"Error capturing/getting screenshot: {e}")
        return None

# -------------------------------
# Main Execution
# -------------------------------
if __name__ == '__main__':
    # Get user input for study topic (only once at start)
    study_topic = "Programming"
    
    # Create the full definition
    definition = create_definition(study_topic)
    
    try:
        while True:
            # Get new screenshot and analyze it
            image_path = get_latest_screenshot()
            if image_path:
                # Run the pipeline synchronously
                final_output = run_pipeline(image_path, definition)
                print("Final Output:", final_output)
            
            # Wait for 10 minutes before next capture
            logger.info("Waiting 1 minute before next screenshot...")
            time.sleep(60)  # 60 seconds = 1 minute
            
    except KeyboardInterrupt:
        logger.info("Screenshot analysis stopped by user")
        # Cleanup resources
        cleanup_model(internvl_model)
    except Exception as e:
        logger.error(f"Error in main loop: {e}")
        # Cleanup resources
        cleanup_model(internvl_model)
