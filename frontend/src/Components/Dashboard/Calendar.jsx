"use client"

import { useState } from "react"
import { DailyCalendar } from "./Calendarviews/DailyCalendar"
import { WeeklyCalendar } from "./Calendarviews/WeeklyCalendar"
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
          <WeeklyCalendar />
        )}
      </div>
    </div>
  )
}

