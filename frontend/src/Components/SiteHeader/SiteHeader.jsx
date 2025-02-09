"use client"

import { useState, useEffect } from "react"
import { Link } from "react-router-dom"
import "./SiteHeader.css"

export function SiteHeader() {
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      const isScrolled = window.scrollY > 10
      if (isScrolled !== scrolled) {
        setScrolled(isScrolled)
      }
    }

    document.addEventListener("scroll", handleScroll, { passive: true })

    return () => {
      document.removeEventListener("scroll", handleScroll)
    }
  }, [scrolled])

  return (
    <header className={`site-header ${scrolled ? "scrolled" : ""}`}>
      <div className="header-container">
        <div className="header-left">
          <Link to="/" className="logo-link">
            <svg className="logo-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path
                d="M12 2L2 7L12 12L22 7L12 2Z"
                fill="#6C6CFF"
                stroke="#6C6CFF"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M2 17L12 22L22 17"
                stroke="#6C6CFF"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M2 12L12 17L22 12"
                stroke="#6C6CFF"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            <span className="logo-text">monday</span>
          </Link>
        </div>
        <div className="header-right">
          <Link to="/login" className="login-link">
            Log in
          </Link>
          <button className="button button-primary">Go to my account</button>
          <button className="menu-button">
            <span className="menu-icon">☰</span>
          </button>
        </div>
      </div>
    </header>
  )
}

