import json
import os
from pydantic import BaseModel, Field
from typing import Dict
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_ollama import OllamaLLM

# Define the Pydantic model for the expected JSON structure
class StudySchedule(BaseModel):
    schedule: Dict[str, bool] = Field(..., description="Schedule for 24 hours")
    explanation: str = Field(..., description="Explanation of how the schedule optimizes productivity and minimizes procrastination")

# Load analyses from the directory
def load_analyses_from_directory(directory_path):
    """
    Loads all JSON files from the 'analyses' directory and returns them as a list of analysis objects.
    """
    all_analyses = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r') as json_file:
                analyses = json.load(json_file)
                all_analyses.extend(analyses)
    return all_analyses

# Use LangChain to invoke the LLaMA model
def create_study_schedule(analyses):
    """
    Creates an optimized study schedule based on the screenshot analysis using LLaMA 3.1 and LangChain's OllamaLLM integration.
    """
    #analysis_data = "\n".join([json.dumps(analysis) for analysis in analyses])

    print("Analysis data: ", analysis_data)
    # this will be dynamic from frontend
    hours = "5"
    # Define the prompt for the LLaMA model
    prompt = f"""
    You are a productivity coach analyzing the user's screen activity patterns to create an optimized study schedule. The user has specific times when they are productive and other times when they are prone to procrastination. Your task is to:

    1. Identify when the user is productive using the Verdict parameter in the data collected from the user's screen activity.
    2. Identify when the user is procrastinating using the Verdict parameter in the data collected from the user's screen activity.
    3. For productive hours, allocate focused study time in 30-minute intervals.
    5. Ensure the total study time for the day is at least {hours} hours.

    Here is the data collected from the user's screen activity:

    {analysis_data}

    You must analyze the user's behavior based on the following parameters:
    - Timestamp: When the activity took place. Prioritize productive activities that happen consistently around the same times.
    - Website: Whether the user is on the internet. If they are on a website, check if it's work-related or a source of procrastination.
    - Content: A description of what the user is doing. Use this to determine if the activity is productive or procrastination.
    - Justification: Why the activity is classified as productive or unproductive.
    - Verdict: If the user is procrastinating (True) or being productive (False).

    Based on this analysis, generate an optimized study schedule. Use focused blocks for productive periods and the Pomodoro technique for procrastination periods. Provide the output in the following JSON format:

    {{
    "schedule": {{
        "12:00 am": true or false,
        "12:30 am": true or false,
        "1:00 am": true or false,
        "1:30 am": true or false,
        ...
        "11:30 pm": true or false
    }},
    "explanation": "Provide a detailed explanation of how this schedule is designed to optimize the user's productivity and minimize procrastination."
    }}
    """

    # Initialize LangChain's Ollama LLM for llama3.1
    llm = OllamaLLM(model="llama3.1")

    # Create the JSON Output Parser
    json_parser = JsonOutputParser(pydantic_object=StudySchedule)

    # Build the prompt template
    template = PromptTemplate(
        template="{format_instructions}\n{prompt}",
        input_variables=["prompt"],
        partial_variables={"format_instructions": json_parser.get_format_instructions()},
    )

    # Format the template with the provided prompt
    formatted_prompt = template.format(prompt=prompt)

    try:
        # Use LangChain to send the prompt and get the response
        print("Sending request to LLama3.1 with LangChain...")
        response = llm.invoke(formatted_prompt)

        # Parse the response into the defined JSON format using the output parser
        parsed_response = json_parser.parse(response)
        
        print(parsed_response)
        # Return the parsed schedule
        return parsed_response

    except Exception as e:
        print(f"Error during LangChain API request: {e}")
        return None

# Main function to run the schedule creator
def run_schedule_creator():
    analyses_directory = "analyses"
    all_analyses = load_analyses_from_directory(analyses_directory)

    # Print all analyses for debugging purposes
    print(f"Analyses: {json.dumps(all_analyses, indent=2)}")

    # Generate the optimized study schedule based on the analyses
    schedule = create_study_schedule(all_analyses)

    if schedule:
        # Print the generated schedule
        print(f"Generated Study Schedule:\n{json.dumps(schedule, indent=2)}")
    else:
        print("Error during schedule creation")

if __name__ == "__main__":
    run_schedule_creator()


#creates a schedule
