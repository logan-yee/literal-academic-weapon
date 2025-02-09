from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scrape2 import get_announcements, get_assignments, get_courses, select_course
from implement_study_plan import run_schedule_creator

app = FastAPI()

# Enable CORS for frontend requests (Node.js, React, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific frontend URL for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
def generate_schedule():
    schedule = run_schedule_creator()
    return {"schedule": schedule}

@app.get("/api/select-course/{course_id}")
def choose_course(course_id: str):
    result = select_course(course_id)
    return {"selected_course": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)