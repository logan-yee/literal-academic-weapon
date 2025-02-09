import sys
import json
import requests
from config import API_KEY

print("Python Executable:", sys.executable)

# Canvas API URL and token
API_URL = "https://learn.ontariotechu.ca/api/v1"
API_TOKEN = API_KEY  # Insert API token

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Accept": "application/json"
}

# Function to save data as JSON
def save_to_json(filename, data):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving to {filename}: {e}")

# Fetch the list of courses for the authenticated user
def get_courses():
    response = requests.get(f"{API_URL}/courses", headers=headers)
    
    if response.status_code == 200:
        try:
            courses = response.json()
            save_to_json("courses.json", courses)
            return courses
        except requests.exceptions.JSONDecodeError:
            print("Error: Received invalid JSON response.")
            return None
    else:
        print(f"Failed to fetch courses (HTTP {response.status_code})")
        return None

# Let the user select a course by name
def select_course(courses):
    if not courses:
        print("No courses found.")
        return None

    print("Available Courses:")
    for index, course in enumerate(courses):
        course_name = course.get("name", "Unnamed Course")
        print(f"{index + 1}. {course_name} (ID: {course['id']})")

    try:
        choice = int(input("Enter the number of the course you want to select: ")) - 1
        if 0 <= choice < len(courses):
            return courses[choice]['id']
        else:
            print("Invalid selection.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

# Fetch grades for the authenticated user in the selected course
def get_grades(course_id):
    response = requests.get(f"{API_URL}/courses/{course_id}/students/submissions", headers=headers)
    
    if response.status_code == 200:
        try:
            grades = response.json()
            save_to_json("grades.json", grades)
            return grades
        except requests.exceptions.JSONDecodeError:
            print("Error: Received invalid JSON response.")
            return None
    else:
        print(f"Failed to fetch grades (HTTP {response.status_code})")
        return None

# Fetch announcements for the selected course
def get_announcements(course_id):
    response = requests.get(
        f"{API_URL}/announcements", 
        headers=headers, 
        params={"context_codes[]": f"course_{course_id}"}
    )
    
    if response.status_code == 200:
        try:
            announcements = response.json()
            save_to_json("announcements.json", announcements)
            return announcements
        except requests.exceptions.JSONDecodeError:
            print("Error: Received invalid JSON response.")
            return None
    else:
        print(f"Failed to fetch announcements (HTTP {response.status_code})")
        return None

# Fetch assignments for the selected course
def get_assignments(course_id):
    response = requests.get(
        f"{API_URL}/courses/{course_id}/assignments", 
        headers=headers
    )
    
    if response.status_code == 200:
        try:
            assignments = response.json()
            save_to_json("assignments.json", assignments)
            return assignments
        except requests.exceptions.JSONDecodeError:
            print("Error: Received invalid JSON response.")
            return None
    else:
        print(f"Failed to fetch assignments (HTTP {response.status_code})")
        return None

# Main workflow
if __name__ == "__main__":
    courses = get_courses()
    
    if courses:
        course_id = select_course(courses)
        
        if course_id:
            print(f"Selected Course ID: {course_id}")
            
            grades = get_grades(course_id)
            if grades:
                print("Grades saved to grades.json")
            else:
                print("No grades found.")
            
            announcements = get_announcements(course_id)
            if announcements:
                print("Announcements saved to announcements.json")
            else:
                print("No announcements found.")
            
            assignments = get_assignments(course_id)
            if assignments:
                print("Assignments saved to assignments.json")
            else:
                print("No assignments found.")
