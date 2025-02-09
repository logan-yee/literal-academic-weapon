from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from scrape2 import get_announcements, get_assignments, get_courses, select_course
from implement_study_plan import run_schedule_creator
import json
import os
import logging

app = FastAPI()

# Configure CORS with more permissive settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",    # Vite default
        "http://localhost:3000",    # Common React port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)

@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI Backend!"}

@app.get("/api/courses")
def fetch_courses():
    courses = get_courses()
    return {"courses": courses}

@app.get("/api/announcements")
def fetch_announcements():
    announcements = get_announcements()
    return {"announcements": announcements}

@app.get("/api/assignments")
def fetch_assignments():
    assignments = get_assignments()
    return {"assignments": assignments}

@app.get("/api/schedule")
async def get_schedule():
    try:
        # Get the absolute path to the schedule file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        schedule_path = os.path.join(current_dir, "backend_schedules", "study_schedule_1739093364.js")
        
        logger.info(f"Attempting to read schedule from: {schedule_path}")
        
        # Check if file exists
        if not os.path.exists(schedule_path):
            logger.error(f"Schedule file not found at: {schedule_path}")
            raise FileNotFoundError(f"Schedule file not found at: {schedule_path}")
        
        # Read the JS file and convert to JSON
        with open(schedule_path, "r") as file:
            content = file.read()
            # Remove "module.exports = " and the trailing semicolon
            json_str = content.replace("module.exports = ", "").rstrip(";")
            schedule_data = json.loads(json_str)
            logger.info("Successfully loaded schedule data")
            return schedule_data
            
    except FileNotFoundError as e:
        logger.error(f"File not found error: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error parsing schedule data: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/select-course/{course_id}")
def choose_course(course_id: str):
    result = select_course(course_id)
    return {"selected_course": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)