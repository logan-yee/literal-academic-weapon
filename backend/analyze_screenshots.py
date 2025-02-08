import base64
import os
import json
from time import sleep
from datetime import datetime
from io import BytesIO
from PIL import Image

from plyer import notification

from langchain_ollama import OllamaLLM

from screenshot_taker import capture_screenshot


# Convert image to base64
def image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error converting image to base64: {e}")
        return None

# Function to convert screenshots to PIL and then base64
def convert_screenshot_to_base64(image_path):
    pil_image = Image.open(image_path)

    # Convert RGBA to RGB if necessary
    if pil_image.mode == 'RGBA':
        pil_image = pil_image.convert('RGB')  # Convert to RGB

    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")  # Save the image as JPEG
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")  # Convert to base64
    return img_str

# Capture and analyze screenshots using LangChain
def capture_and_analyze_screenshots():
    """
    Captures screenshots, analyzes them using LangChain with the Ollama `llava` model, 
    and saves the results in a folder called 'analyses'.
    """
    all_analyses = []  # List to store all screenshot analyses

    # Ensure the 'analyses' folder exists
    if not os.path.exists('./analyses'):
        os.makedirs('./analyses')

    llm = OllamaLLM(model="llava")  # Initialize LangChain's Ollama model for analysis

    for _ in range(4):  # Capture 4 screenshots every minute
        screenshot_file = capture_screenshot()  # Function that captures screenshots

        # Convert screenshot to base64
        base64_image = convert_screenshot_to_base64(screenshot_file)

        # Prompt
        prompt =  """
        You are analyzing a screenshot of a user's computer screen. Your task is to return an objective, concise summary in a strict JSON format. Follow these steps carefully:

        1. Search for specific keywords indicating internet use (e.g., 'Google Chrome', 'Firefox', 'Edge', 'http', 'https'). If found, return 'website': true; otherwise, return 'website': false.
        2. Log relevant keywords related to the primary activity (e.g., 'VS Code', 'Word', 'Excel', 'YouTube', 'Twitter'). Use these to provide a factual description of the main content displayed on the screen without assumptions.
        3. Determine productivity based on keywords: classify tasks as productive (e.g., 'code', 'research', 'document', 'Python', 'C++') or unproductive (e.g., 'video', 'social', 'game'). Work-related tasks such as coding MUST ALWAYS be classified as productive.
        4. Return a strict final verdict based on keyword analysis. If unproductive keywords dominate, return 'verdict': true (procrastinating), otherwise return 'verdict': false (productive).

        Return the response as a valid JSON object with the following structure:
        {
          "website": true or false,
          "content": "short phrase summarizing the page",
          "justification": "a short justification of the activity being productive or procrastination",
          "verdict": true or false
        }

        Important Guidelines:
        - Be STRICT in your analysis. Assume any non-work-related activity is procrastination.
        - For video content (YouTube, Netflix, etc.), base your analysis on the visible title or caption of the video, not just the video thumbnail. If a video appears unrelated to work, consider it procrastination.
        - Do not overfocus on small details like icons or peripheral information. Focus on the overall activity that is most visible on the screen.
        - If no browser or internet-connected application is visible but the user is working with code, research papers, or productivity apps, consider this work-related.
        - Any art-related activities (e.g., drawing apps) or browsing that is unrelated to science, programming, or work must be considered procrastination.
        - The final verdict ("verdict") should never be null. If unsure, default to "verdict": true (procrastination).
        - IF THE USER IS DOING ANY OF THE BELOW, IT WILL BE CONSIDERED WORK RELATED UNDER ANY CIRCUMSTANCE:
            1. Coding or doing code-related activities
            2. Math or math-related activities. 
            3. ANY of the sciences, if they are doing physics, chemistry, biology, computer science, or anything engineering related. 
            4. On a code editor, researching about a science subject, or researching about mathematics.
        """
        # Use LangChain's multi-modal LLM with the image
        llm_with_image_context = llm.bind(images=[base64_image])
        response = llm_with_image_context.invoke(prompt)
        print("RAW RESPONSE FROM LLM:", response)

        # Parse the response as JSON
        response_json = clean_response(response)

        if response_json:

            # Add a timestamp to the JSON response
            analysis_timestamp = datetime.now().isoformat()
            final_result = {
                "timestamp": analysis_timestamp,
                "analysis": response_json
            }

            # Add the analysis to the list
            all_analyses.append(final_result)

             # Send a notification to the user if procrastination is detected 
            if response_json.get("verdict") is True:
                notification.notify (
                    title = "!!!BIG BORTHER IS ALWAYS WATCHING!!!",
                    message = "Ollama suspects you might be procrastinating. Get back to work."
                )

        # Wait for 60 seconds before capturing the next screenshot
        sleep(60)

    # Save the analyses to a JSON file inside the 'analyses' folder
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    analysis_filename = f"analyses/analysis_{timestamp}.json"

    with open(analysis_filename, 'w') as json_file:
        json.dump(all_analyses, json_file, indent=4)

    print(f"Analyses saved to {analysis_filename}")
    return all_analyses  # Return the list of analyses for further processing

# Function to clean response and extract the JSON
def clean_response(response_text):
    try:
        # Find the first '{' and the last '}' in the response
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}')
        
        if start_idx == -1 or end_idx == -1:
            raise ValueError("No valid JSON found in response")

        # Extract the JSON portion between the curly braces
        cleaned_text = response_text[start_idx:end_idx+1]
        return json.loads(cleaned_text)

    except (json.JSONDecodeError, ValueError) as e:
        print(f"Failed to decode JSON: {e}")
        return None

def run_analysis():
    capture_and_analyze_screenshots()

if __name__ == "__main__":
    run_analysis()