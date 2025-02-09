import React, { useState } from 'react';
import './WeeklyCalendar.css';

export function WeeklyCalendar() {
  const hours = Array.from({ length: 24 }, (_, i) => i);
  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const [selectedCell, setSelectedCell] = useState(null);

  const formatHour = (hour) => {
    const period = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour % 12 || 12;
    return `${displayHour}:00 ${period}`;
  };

  return (
    <div className="weekly-calendar">
      <div className="week-header">
        <div className="time-header"></div>
        {days.map((day) => (
          <div key={day} className="day-header">
            {day}
          </div>
        ))}
      </div>
      <div className="time-grid">
        {hours.map((hour) => (
          <div key={hour} className="time-row">
            <div className="time-label">{formatHour(hour)}</div>
            {days.map((day, index) => (
              <div
                key={`${day}-${hour}`}
                className={`time-cell ${selectedCell === `${day}-${hour}` ? 'selected' : ''}`}
                onClick={() => setSelectedCell(`${day}-${hour}`)}
              >
                {/* Content goes here */}
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}