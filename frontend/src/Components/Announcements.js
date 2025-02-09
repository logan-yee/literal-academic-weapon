import React, { useState, useEffect } from "react";

const Announcements = () => {
  const [announcements, setAnnouncements] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/announcements")
      .then((response) => response.json())
      .then((data) => setAnnouncements(data.announcements))
      .catch((error) => console.error("Error fetching announcements:", error));
  }, []);

  return (
    <div>
      <h1>Announcements</h1>
      <ul>
        {announcements.map((announcement, index) => (
          <li key={index}>{announcement}</li>
        ))}
      </ul>
    </div>
  );
};

export default Announcements;
