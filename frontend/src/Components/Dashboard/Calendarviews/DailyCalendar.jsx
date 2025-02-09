import React, { useState } from 'react';
import './DailyCalendar.css';

export function DailyCalendar() {
  const hours = Array.from({ length: 24 }, (_, i) => i); // 0-23 hours
  const [selectedHour, setSelectedHour] = useState(null);

  const formatHour = (hour) => {
    const period = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour % 12 || 12;
    return `${displayHour}:00 ${period}`;
  };

  return (
    <div className="daily-calendar">
      <div className="time-slots">
        {hours.map((hour) => (
          <div
            key={hour}
            className={`time-slot ${selectedHour === hour ? 'selected' : ''}`}
            onClick={() => setSelectedHour(hour)}
          >
            <div className="time-label">{formatHour(hour)}</div>
            <div className="time-content">
              {/* Placeholder for events/tasks */}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}