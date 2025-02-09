import React, { useState, useEffect } from "react";

const Courses = () => {
  const [courses, setCourses] = useState([]); // State to store courses data
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch courses from the backend
    fetch("http://127.0.0.1:5000/api/courses") // Replace with your backend URL
      .then((response) => response.json())
      .then((data) => {
        setCourses(data.courses); // Update state with fetched data
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching courses:", error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <p>Loading...</p>;
  }

  return (
    <div>
      <h1>Courses</h1>
      <ul>
        {courses.map((course, index) => (
          <li key={index}>{course}</li>
        ))}
      </ul>
    </div>
  );
};

export default Courses;
