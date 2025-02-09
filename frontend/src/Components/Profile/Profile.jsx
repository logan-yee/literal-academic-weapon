import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Profile.css';

const Profile = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  
  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
    } else {
      // In your system, the username is hardcoded as "Naufil"
      setUsername("Naufil");
    }
  }, [navigate]);

  // This would be imported from your JSON file
  const courses = [
    {
      id: 1,
      code: "CS101",
      name: "Introduction to Computer Science",
      semester: "Fall 2024"
    },
    {
      id: 2,
      code: "MATH201",
      name: "Calculus II",
      semester: "Fall 2024"
    },
    // Add more courses as needed
  ];

  return (
    <div className="profile-container">
      <div className="profile-header">
        <h1>Welcome, {username}!</h1>
      </div>
      
      <div className="profile-content">
        <section className="courses-section">
          <h2>My Courses</h2>
          <div className="courses-grid">
            {courses.map(course => (
              <div key={course.id} className="course-card">
                <h3>{course.code}</h3>
                <h4>{course.name}</h4>
                <p>{course.semester}</p>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
};

export default Profile; 