from celery import Celery, chain
from transformers import AutoProcessor, VisionEncoderDecoderModel, pipeline
from PIL import Image
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import Ollama
from internvl_loader import load_internvl_model
import torch

# -------------------------------
# Celery Configuration
# -------------------------------

app = Celery(
    'ocr_pipeline',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

# -------------------------------
# Global Model Loading
# -------------------------------

# Load the InternVL model, tokenizer, processor, and device
model, tokenizer, processor, device = load_internvl_model()

# Initialize Ollama for both preconditioning and classification
llm = Ollama(model="llama3.1", temperature=0.3, base_url="http://localhost:11434")

# Define classification prompt template
classification_prompt = PromptTemplate(
    input_variables=["text", "image_description"],
    template=(
        "You are analyzing a screenshot with the following elements:\n"
        "1. Visual Description: {image_description}\n"
        "2. Extracted Text Content: {text}\n\n"
        "Based on both the visual context and text content, identify key elements and classify them.\n"
        "Consider:\n"
        "- The type of application or website visible\n"
        "- The nature of the content (work, entertainment, social, etc.)\n"
        "- Any visible UI elements or interactions\n\n"
        "Return the result as a JSON object with:\n"
        "- 'label': either 'productive' or 'procrastination'\n"
        "- 'score': confidence between 0 and 1\n"
        "- 'keywords': list of identified elements and their classifications\n"
        "- 'context': brief explanation of the classification\n\n"
        "JSON Response:"
    )
)

classification_chain = LLMChain(prompt=classification_prompt, llm=llm)

# -------------------------------
# LangChain Preconditioning Setup with Ollama
# -------------------------------
# Define a prompt template that uses a context (JSON or prompt) and the extracted text.
prompt_template = PromptTemplate(
    input_variables=["context", "extracted_text"],
    template=(
        "Using the following context: {context}\n"
        "And the extracted text: {extracted_text}\n"
        "Return a preconditioned version of the text that emphasizes the given context."
    )
)

# Create a LangChain LLMChain using the prompt template and the Ollama LLM.
llm_chain = LLMChain(prompt=prompt_template, llm=llm)

def generate_preconditioned_text(context_input, extracted_text):
    """
    Uses LangChain (with Ollama) to generate a modified version of the extracted text
    based on the provided context.
    """
    return llm_chain.run(context=context_input, extracted_text=extracted_text)

# -------------------------------
# Task 1: InternVL OCR Agent Task
# -------------------------------
@app.task
def internvl_ocr_task(image_path):
    """
    Uses InternVL2.5-2B-MPO to extract text and analyze image content.
    """
    print("\n[Step 1] Starting image analysis...")
    
    # Load and process the image
    image = Image.open(image_path).convert("RGB")
    pixel_values = processor(images=image, return_tensors="pt").to(torch.bfloat16).cuda()
    
    # Generate the description using the chat method
    question = "<image>\nPlease describe what you see in this image, focusing on any text content."
    response = model.chat(tokenizer, pixel_values, question, 
                         generation_config=dict(max_new_tokens=1024, do_sample=True))
    
    print(f"[Step 1] Extracted content: {response[:100]}...")  # Show first 100 chars
    return response

# -------------------------------
# Task 2: Preconditioning Task Using LangChain with Ollama
# -------------------------------
@app.task
def precondition_text_classifier_task(extracted_text, context_input):
    """
    Preconditions the extracted text using a JSON input or prompt.
    This simulates training or context adjustment before classification.
    Uses LangChain with an Ollama-served LLM.
    """
    print("\n[Step 2] Starting text preconditioning...")
    modified_text = generate_preconditioned_text(context_input, extracted_text)
    print(f"[Step 2] Modified text: {modified_text[:100]}...")  # Show first 100 chars
    return modified_text

# -------------------------------
# Task 3: Llama Text Analysis Task
# -------------------------------
@app.task
def llama_text_classification_task(modified_text, original_image_description):
    """
    Uses Ollama's llama2 model to analyze text and classify keywords as productive or procrastination.
    Now includes both the modified text and original image description for better context.
    """
    print("\n[Step 3] Starting text classification...")
    
    try:
        # Get classification result using both text and image description
        result_str = classification_chain.run(
            text=modified_text,
            image_description=original_image_description
        )
        
        # Parse the JSON response
        import json
        result = json.loads(result_str)
        
        print(f"[Step 3] Classification result: {result}")
        return {
            "label": result.get("label", "unknown"),
            "score": result.get("score", 0.0),
            "keywords": result.get("keywords", []),
            "context": result.get("context", "No context provided")
        }
    except Exception as e:
        print(f"[Step 3] Error in classification: {str(e)}")
        return {
            "label": "error",
            "score": 0.0,
            "keywords": [],
            "context": f"Error during classification: {str(e)}"
        }

# -------------------------------
# Task 4: Refinement Agent Task
# -------------------------------
@app.task
def refinement_agent_task(classification_result):
    """
    Invoked when the confidence is low.
    Flags the classification result for further review.
    """
    flagged_result = {
        "label": classification_result["label"],
        "confidence": classification_result["score"],
        "flag": True,
        "message": "Low confidence - requires further review."
    }
    return flagged_result

# -------------------------------
# Task 5: Decision Aggregator Task
# -------------------------------
@app.task
def decision_aggregator_task(classification_result):
    """
    Aggregates the classification result. If the confidence is below a threshold,
    calls the refinement agent.
    """
    print("\n[Step 4] Starting decision aggregation...")
    CONFIDENCE_THRESHOLD = 0.75
    if classification_result["score"] < CONFIDENCE_THRESHOLD:
        print("[Step 4] Low confidence detected, invoking refinement agent...")
        flagged_result = refinement_agent_task.delay(classification_result).get()
        final_decision = flagged_result
    else:
        print("[Step 4] Confidence threshold met, accepting classification...")
        final_decision = {
            "label": classification_result["label"],
            "confidence": classification_result["score"],
            "flag": False,
            "message": "Classification accepted."
        }
    print(f"[Step 4] Final decision: {final_decision}")
    return final_decision

# -------------------------------
# Pipeline Runner Function
# -------------------------------
def run_pipeline(image_path, context_input):
    """
    Enhanced pipeline that maintains the image description context throughout the process.
    """
    print("\n=== Starting Pipeline ===")
    print(f"Image path: {image_path}")
    print(f"Context input: {context_input}")
    
    # Step 1: Get OCR and image description
    ocr_result = internvl_ocr_task.delay(image_path).get()
    
    # Step 2: Precondition the text
    preconditioned_text = precondition_text_classifier_task.delay(
        ocr_result, 
        context_input
    ).get()
    
    # Step 3: Classify with both text and original description
    classification_result = llama_text_classification_task.delay(
        preconditioned_text,
        ocr_result  # Pass the original image description
    ).get()
    
    # Step 4: Aggregate decision
    final_decision = decision_aggregator_task.delay(classification_result).get()
    
    print("\n=== Pipeline Complete ===")
    return final_decision

# -------------------------------
# For Testing the Pipeline
# -------------------------------
if __name__ == '__main__':

    # Replace with the actual path to your image file.
    image_path = "./screenshots/screenshot_2025-01-01_18-33-51.png"
    # Provide a JSON input or prompt that defines what constitutes procrastination.
    context_input = '{"definition": "Procrastination includes social media, entertainment, and non-study activities."}'
    
    final_output = run_pipeline(image_path, context_input)
    print("Final Output:", final_output)

print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
