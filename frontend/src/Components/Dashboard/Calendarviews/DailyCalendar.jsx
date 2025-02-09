import React, { useState, useEffect } from 'react';
import './WeeklyCalendar.css';

export function WeeklyCalendar() {
  const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const hours = Array.from({ length: 24 }, (_, i) => i); // 0-23 hours
  const [selectedDay, setSelectedDay] = useState(new Date().getDay());
  const [scheduleData, setScheduleData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSchedule = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/schedule', {
          method: 'GET',
          headers: { 'Accept': 'application/json' },
        });
        
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Failed to fetch schedule: ${errorText}`);
        }
        
        const data = await response.json();
        console.log('Fetched schedule data:', data);
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
    return `${displayHour}:00 ${period}`;
  };

  const getScheduleStatus = (day, hour) => {
    if (!scheduleData?.schedule) return false;
    const timeKey = formatHour(hour);
    return scheduleData.schedule[day]?.[timeKey] || false;
  };

  if (loading) return <div>Loading schedule...</div>;
  if (error) return <div>Error loading schedule: {error}</div>;
  if (!scheduleData || !scheduleData.schedule) return <div>No schedule data available</div>;

  return (
    <div className="weekly-calendar">
      <div className="day-selector">
        {daysOfWeek.map((day, index) => (
          <button key={day} onClick={() => setSelectedDay(index)} className={selectedDay === index ? 'active' : ''}>
            {day}
          </button>
        ))}
      </div>
      <div className="time-slots">
        {hours.map((hour) => (
          <div key={hour} className={`time-slot ${getScheduleStatus(daysOfWeek[selectedDay], hour) ? 'scheduled' : ''}`}>
            <div className="time-label">{formatHour(hour)}</div>
            <div className="time-content">
              {getScheduleStatus(daysOfWeek[selectedDay], hour) && <span className="study-indicator">Study Time</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
