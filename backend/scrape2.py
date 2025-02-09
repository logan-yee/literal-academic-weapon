import sys
import json
import requests

print("Python Executable:", sys.executable)

# Canvas API URL and token
API_URL = "https://learn.ontariotechu.ca/api/v1"
API_TOKEN = "13377~u2MxkTCccXQvRLNAD4UBhLQP7PNMrxNknWY9rym267YhnDvN6hxGZYJHnz4PDtPf" # Insert API token

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

# Step 1: Fetch the list of courses for the authenticated user
def get_courses():
    response = requests.get(f"{API_URL}/courses", headers=headers)
    
    if response.status_code == 200:
        try:
            courses = response.json()
            save_to_json("courses.json", courses)  # Save courses to JSON file
            return courses
        except requests.exceptions.JSONDecodeError:
            print("Error: Received invalid JSON response.")
            print("Response Content:", response.text)
            return None
    else:
        print(f"Failed to fetch courses (HTTP {response.status_code})")
        print("Response Content:", response.text)
        return None

# Step 2: Let the user select a course by name
def select_course(courses):
    if not courses:
        print("No courses found.")
        return None

    print("Available Courses:")
    for index, course in enumerate(courses):
        course_name = course.get("name", "Unnamed Course")  # Handle missing names
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

# Step 3: Fetch announcements for the selected course
def get_announcements(course_id):
    response = requests.get(
        f"{API_URL}/announcements", 
        headers=headers, 
        params={"context_codes[]": f"course_{course_id}"}
    )

    if response.status_code == 200:
        try:
            announcements = response.json()
            save_to_json("announcements.json", announcements)  # Save to JSON
            return announcements
        except requests.exceptions.JSONDecodeError:
            print("Error: Received invalid JSON response.")
            print("Response Content:", response.text)
            return None
    else:
        print(f"Failed to fetch announcements (HTTP {response.status_code})")
        print("Response Content:", response.text)
        return None

# Step 4: Fetch assignments for the selected course
def get_assignments(course_id):
    response = requests.get(
        f"{API_URL}/courses/{course_id}/assignments", 
        headers=headers
    )

    if response.status_code == 200:
        try:
            assignments = response.json()
            save_to_json("assignments.json", assignments)  # Save to JSON
            return assignments
        except requests.exceptions.JSONDecodeError:
            print("Error: Received invalid JSON response.")
            print("Response Content:", response.text)
            return None
    else:
        print(f"Failed to fetch assignments (HTTP {response.status_code})")
        print("Response Content:", response.text)
        return None

# Main workflow
if __name__ == "__main__":
    courses = get_courses()

    if courses:
        course_id = select_course(courses)

        if course_id:
            print(f"Selected Course ID: {course_id}")

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