import React, { useState, useEffect } from 'react';
import './DailyCalendar.css';

export function DailyCalendar() {
  const hours = Array.from({ length: 24 }, (_, i) => i); // 0-23 hours
  const [selectedHour, setSelectedHour] = useState(null);
  const [scheduleData, setScheduleData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSchedule = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/schedule', {
          method: 'GET',
          headers: {
            'Accept': 'application/json',
          },
        });
        
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Failed to fetch schedule: ${errorText}`);
        }
        
        const data = await response.json();
        console.log('Fetched schedule data:', data); // Debug log
        setScheduleData(data);
      } catch (err) {
        console.error('Error fetching schedule:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchSchedule();
  }, []);

  const formatHour = (hour) => {
    const period = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour % 12 || 12;
    const formattedTime = `${displayHour}:00 ${period}`.toLowerCase();
    console.log('Formatting hour:', hour, 'to:', formattedTime); // Debug time formatting
    return formattedTime;
  };

  const getScheduleStatus = (hour) => {
    if (!scheduleData?.schedule) return false;
    const timeKey = formatHour(hour);
    const status = scheduleData.schedule[timeKey];
    console.log('Checking status for:', timeKey, 'Result:', status); // Debug schedule status
    return status;
  };

  if (loading) {
    return <div>Loading schedule...</div>;
  }

  if (error) {
    return <div>Error loading schedule: {error}</div>;
  }

  if (!scheduleData || !scheduleData.schedule) {
    return <div>No schedule data available</div>;
  }

  return (
    <div className="daily-calendar">
      <div className="time-slots">
        {hours.map((hour) => (
          <div
            key={hour}
            className={`time-slot ${selectedHour === hour ? 'selected' : ''} ${
              getScheduleStatus(hour) ? 'scheduled' : ''
            }`}
            onClick={() => setSelectedHour(hour)}
          >
            <div className="time-label">{formatHour(hour)}</div>
            <div className="time-content">
              {getScheduleStatus(hour) && <span className="study-indicator">Study Time</span>}
            </div>
          </div>
        ))}
      </div>
      {scheduleData.explanation && (
        <div className="schedule-explanation">
          <pre>{scheduleData.explanation}</pre>
        </div>
      )}
    </div>
  );
}