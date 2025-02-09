import json
import os
from pydantic import BaseModel, Field
from typing import Dict
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_ollama import OllamaLLM

#cmd prompt: ollama pull mistral

# Define the Pydantic model for expected JSON output
class StudySchedule(BaseModel):
    schedule: Dict[str, bool] = Field(..., description="Schedule for 24 hours")
    explanation: str = Field(..., description="Explanation of how the schedule optimizes productivity")

# Load analyses from the directory
def load_analyses_from_directory(directory_path):
    if not os.path.exists(directory_path):
        print(f"Directory '{directory_path}' not found. Creating it now...")
        os.makedirs(directory_path)
    
    all_analyses = []
    
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            file_path = os.path.join(directory_path, filename)
            
            # Skip empty files
            if os.path.getsize(file_path) == 0:
                print(f"Skipping empty file: {filename}")
                continue

            try:
                with open(file_path, 'r') as json_file:
                    analyses = json.load(json_file)
                    if analyses:  # Ensure JSON is not empty
                        all_analyses.extend(analyses)
                    else:
                        print(f"Skipping empty JSON content in: {filename}")

            except json.JSONDecodeError:
                print(f"Skipping invalid JSON file: {filename}")
    
    return all_analyses


# Generate a study schedule using Ollama RAG
def create_study_schedule(analyses):
    analysis_data = "\n".join([json.dumps(analysis) for analysis in analyses])  # Convert JSON to string format

    print("Analysis data: ", analysis_data)  # Debugging print

    hours = "5"  # This could be dynamic from frontend
    hoursofstudy = "user dependent"  # This could be dynamic from frontend
    prompt = f"""
    You are a productivity coach analyzing the user's screen activity patterns to create an optimized study schedule.
    
    1. Identify productive and procrastination hours using the "Verdict" field.
    2. Allocate focused study time in 1-hour intervals during productive hours.
    3. Ensure total study time is at least {hours} hours.
    4. If the total study time is less than {hours} hours, suggest additional study hours during procrastination hours.

    Data collected from user's screen activity:
    {analysis_data}

    Return output in Json format and nothing else and remove all comments including backslashes.:

    {{
        "schedule": {{
            "01:00 am": true or false,
            ...
            "11:00 pm": true or false
        }},
        "explanation": "Detailed explanation on how the schedule optimizes productivity."
    }}
    """

    # Initialize LangChain's Ollama LLM
    llm = OllamaLLM(model="mistral")  # Alternative model

    # Create the JSON Output Parser
    json_parser = JsonOutputParser(pydantic_object=StudySchedule)

    # Build the prompt template
    template = PromptTemplate(
        template="{format_instructions}\n{prompt}",
        input_variables=["prompt"],
        partial_variables={"format_instructions": json_parser.get_format_instructions()},
    )

    # Format the template
    formatted_prompt = template.format(prompt=prompt)

    try:
        # Use LangChain to send prompt to Ollama
        print("Sending request to LLaMA 3 with LangChain...")
        response = llm.invoke(formatted_prompt)  # Ensure Ollama supports this method

        # Parse the JSON response
        parsed_response = json_parser.parse(response)

        print(parsed_response)  # Debugging
        return parsed_response

    except Exception as e:
        print(f"Error during request: {e}")
        return None

# Main function to run the schedule creator
def run_schedule_creator():
    analyses_directory = "analyses"
    all_analyses = load_analyses_from_directory(analyses_directory)

    print(f"Analyses: {json.dumps(all_analyses, indent=2)}")  # Debugging

    schedule = create_study_schedule(all_analyses)

    if schedule:
        try:
            # If it's a string, ensure it's valid JSON
            if isinstance(schedule, str):
                schedule = json.loads(schedule)  # Convert string to dictionary

            print(f"Generated Study Schedule:\n{json.dumps(schedule, indent=2)}")
        except json.JSONDecodeError as e:
            print("JSON Parsing Error:", e)
    else:
        print("Error during schedule creation")

if __name__ == "__main__":
    run_schedule_creator()