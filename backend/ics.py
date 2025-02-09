
import json
import os
import datetime
import pytz
from icalendar import Calendar, Event
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import Dict, List

optimized_schedule = {
    "schedule": {
        "2025-02-08": {
            "10:00 AM": "Study Math",
            "11:00 AM": "Physics Review"
        },
        "2025-02-09": {
            "09:30 AM": "Read History Notes",
            "01:00 PM": "Work on Project"
        }
    }
}

def export_to_ics(optimized_schedule, filename="study_schedule.ics"):
    cal = Calendar()
    timezone = pytz.timezone("America/Toronto")

    for date, time_slots in optimized_schedule.schedule.items():
        for time, task in time_slots.items():
            event = Event()
            event.add('summary', task)
            event_date = datetime.datetime.strptime(f"{date} {time}", "%Y-%m-%d %I:%M %p")
            event.add('dtstart', timezone.localize(event_date))
            event.add('dtend', timezone.localize(event_date + datetime.timedelta(minutes=30)))
            cal.add_component(event)

    with open(filename, 'wb') as f:
        f.write(cal.to_ical())
    print(f"ICS file created: {filename}")