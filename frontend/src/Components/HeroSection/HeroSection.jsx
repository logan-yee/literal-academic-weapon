"use client"

import { useState } from "react"
import "./HeroSection.css"
import { useNavigate } from "react-router-dom"

export function HeroSection() {
  const [activeTab, setActiveTab] = useState("projects")
  const navigate = useNavigate()

  return (
    <div className="hero-section">
      <div className="hero-container">
        <h1 className="hero-title">
          Gotta lock in?
          <br />
          Become an Academic Weapon
        </h1>

        <div className="tabs">
          <button
            className={`tab ${activeTab === "projects" ? "active" : ""}`}
            onClick={() => setActiveTab("projects")}
          >
            The Project
          </button>
          <button
            className={`tab ${activeTab === "about" ? "active" : ""}`}
            onClick={() => setActiveTab("about")}
          >
            About
          </button>
          <button
            className={`tab ${activeTab === "processes" ? "active" : ""}`}
            onClick={() => setActiveTab("processes")}
          >
            Processes
          </button>
        </div>


        <div className="content-grid">
          <div className={`content-slider ${activeTab}`}>
            <div className="content-slide projects">
              <div className="content-left">
                <h2 className="content-subtitle">AI Powered Academic Tool</h2>
                <h3 className="content-heading">Stay in sync and on schedule</h3>
                <p className="content-text">
                  Transform your academic journey with our AI-powered study companion. 
                  Get personalized study plans, smart reminders, and efficient learning tools.
                </p>
                <button 
                  className="get-started-button"
                  onClick={() => navigate("/LoginSignup")}
                >
                  Get started
                </button>

              </div>
              <div className="content-right">
                <img
                  src="https://ih1.redbubble.net/image.4529032670.5247/bg,f8f8f8-flat,750x,075,f-pad,750x1000,f8f8f8.jpg"
                  alt="Monday.com interface"
                  className="hero-image"
                />
              </div>
            </div>

            <div className="content-slide about">
              <div className="content-left">
                <h2 className="content-subtitle">About Academic Weapon</h2>
                <h3 className="content-heading">Your Study Success Partner</h3>
                <p className="content-text">
                  Academic Weapon is designed to help students excel in their studies
                  through smart organization, AI-powered assistance, and effective time
                  management. Our platform adapts to your learning style and helps you
                  achieve your academic goals.
                </p>
              </div>
              <div className="content-right">
                <img
                  src="https://wojakland.com/wp-content/grand-media/image/shocked_soyjak.png"
                  alt="About section image"
                  className="hero-image"
                />
              </div>
            </div>

            <div className="content-slide processes">
              <div className="content-center">
                <h2 className="content-subtitle text-center">Tools and Technologies</h2>
                <h3 className="content-heading text-center">Powered by Innovation</h3>
                <div className="tech-list">
                  <p className="text-center">Built with cutting-edge technologies including:</p>
                  <ul className="tech-items">
                    <li>Advanced AI algorithms for personalized learning</li>
                    <li>Real-time progress tracking</li>
                    <li>Smart scheduling system</li>
                    <li>Cloud-based collaboration tools</li>
                    <li>Secure data protection</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

