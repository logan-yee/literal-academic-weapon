"use client"

import { useState } from "react"
import { DailyCalendar } from "./Calendarviews/DailyCalendar"
import "./Calendar.css"

export function Calendar() {
  const [view, setView] = useState("daily")

  return (
    <div className="calendar">
      <div className="calendar-header">
        <h2>Calendar</h2>
        <div className="view-toggle">
          <button className={view === "daily" ? "active" : ""} onClick={() => setView("daily")}>
            Daily
          </button>
          <button className={view === "weekly" ? "active" : ""} onClick={() => setView("weekly")}>
            Weekly
          </button>
        </div>
      </div>
      <div className="calendar-body">
        {view === "daily" ? (
          <DailyCalendar />
        ) : (
          <div className="weekly-view">
            {/* Placeholder for weekly calendar view */}
            <p>Weekly calendar view goes here</p>
          </div>
        )}
      </div>
    </div>
  )
}

