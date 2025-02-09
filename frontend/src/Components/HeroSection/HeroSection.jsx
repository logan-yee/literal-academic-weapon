"use client"

import { useState } from "react"
import "./HeroSection.css"

export function HeroSection() {
  const [activeTab, setActiveTab] = useState("projects")

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
            Projects
          </button>
          <button
            className={`tab ${activeTab === "portfolios" ? "active" : ""}`}
            onClick={() => setActiveTab("portfolios")}
          >
            Portfolios
          </button>
          <button
            className={`tab ${activeTab === "processes" ? "active" : ""}`}
            onClick={() => setActiveTab("processes")}
          >
            Processes
          </button>
          <button
            className={`tab ${activeTab === "resources" ? "active" : ""}`}
            onClick={() => setActiveTab("resources")}
          >
            Resources
          </button>
        </div>

        <div className="content-grid">
          <div className="content-left">
            <h2 className="content-subtitle">Ai Powered Academic Tool</h2>
            <h3 className="content-heading">Stay in sync and on schedule</h3>
            <p className="content-text">
              
            </p>
            <button className="get-started-button">Get started</button>
          </div>
          <div className="content-right">
            <img
              src="https://ih1.redbubble.net/image.4529032670.5247/bg,f8f8f8-flat,750x,075,f-pad,750x1000,f8f8f8.jpg"
              alt="Monday.com interface"
              className="hero-image"
            />
          </div>
        </div>
      </div>
    </div>
  )
}

