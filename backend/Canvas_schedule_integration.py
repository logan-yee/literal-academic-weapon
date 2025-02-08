import json
import os
import datetime
import pytz
from icalendar import Calendar, Event

# Load study schedule
def load_study_schedule(schedule_file):
    with open(schedule_file, 'r') as f:
        return json.load(f)

# Load Canvas assignments
def load_canvas_assignments(assignments_file):
    with open(assignments_file, 'r') as f:
        return json.load(f)

# Merge study schedule with assignments
def merge_schedule_with_assignments(study_schedule, assignments):
    merged_schedule = []
    
    for date, time_slots in study_schedule['schedule'].items():
        for time, is_study_time in time_slots.items():
            if is_study_time:
                assigned_task = None
                for assignment in assignments:
                    due_date = assignment['due_at'][:10]  # Extract YYYY-MM-DD
                    if date == due_date:
                        assigned_task = assignment['name']
                        assignments.remove(assignment)
                        break
                
                merged_schedule.append({
                    'date': date,
                    'time': time,
                    'task': assigned_task if assigned_task else 'Self Study'
                })
    return merged_schedule

# Allow user to manually add topics
def add_manual_topics(merged_schedule):
    print("Would you like to add extra study topics? (y/n)")
    if input().lower() == 'y':
        for entry in merged_schedule:
            print(f"{entry['date']} {entry['time']} - {entry['task']}")
            topic = input("Enter a topic to study (or press Enter to keep current): ")
            if topic:
                entry['task'] = topic
    return merged_schedule

# Export to .ICS file
def export_to_ics(merged_schedule, filename="study_schedule.ics"):
    cal = Calendar()
    timezone = pytz.timezone("America/Toronto")  # Change as needed
    
    for entry in merged_schedule:
        event = Event()
        event.add('summary', entry['task'])
        event_date = datetime.datetime.strptime(f"{entry['date']} {entry['time']}", "%Y-%m-%d %I:%M %p")
        event.add('dtstart', timezone.localize(event_date))
        event.add('dtend', timezone.localize(event_date + datetime.timedelta(minutes=30)))
        cal.add_component(event)
    
    with open(filename, 'wb') as f:
        f.write(cal.to_ical())
    print(f"ICS file created: {filename}")

# Main function
def main():
    study_schedule = load_study_schedule("study_schedule.json")
    assignments = load_canvas_assignments("canvas_assignments.json")
    
    merged_schedule = merge_schedule_with_assignments(study_schedule, assignments)
    merged_schedule = add_manual_topics(merged_schedule)
    export_to_ics(merged_schedule)

if __name__ == "__main__":
    main()
