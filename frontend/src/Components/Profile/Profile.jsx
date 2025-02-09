import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Profile.css';

const Profile = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log('Fetching courses...');
        const response = await fetch('http://127.0.0.1:5000/api/courses');
        
        if (!response.ok) {
          console.error('Response not OK:', response.status);
          throw new Error(`Failed to fetch courses: ${response.status}`);
        }

        const data = await response.json();
        console.log('Raw API response:', data);  // Debug log
        
        if (!data) {
          throw new Error('No data received from API');
        }

        // Handle the data structure from your Canvas API
        const formattedCourses = data.map(course => ({
          id: course.id,
          code: course.course_code || course.name,
          name: course.name,
          term: course.enrollment_term_id
        }));
        
        console.log('Formatted courses:', formattedCourses);
        setCourses(formattedCourses);
        setUsername("Naufil");
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [navigate]);

  return (
    <div className="profile-container">
      <div className="profile-header">
        <h1>Welcome, {username}!</h1>
      </div>
      
      <div className="profile-content">
        <section className="courses-section">
          <h2>My Courses</h2>
          <div className="courses-grid">
            {Array.isArray(courses) && courses.length > 0 ? (
              courses.map(course => (
                <div key={course.id} className="course-card">
                  <h3>{course.code}</h3>
                  <h4>{course.name}</h4>
                  <p>Term: {course.term}</p>
                </div>
              ))
            ) : (
              <p>No courses found. {loading ? 'Loading...' : ''}</p>
            )}
          </div>
        </section>
      </div>
    </div>
  );
};

export default Profile; 