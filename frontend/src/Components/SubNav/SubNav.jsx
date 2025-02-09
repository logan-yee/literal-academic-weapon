import { Link } from "react-router-dom"
import "./SubNav.css"

export function SubNav() {
  return (
    <nav className="sub-nav">
      <div className="sub-nav-container">
        <Link to="/" className="work-management-link">
          <svg className="work-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path
              d="M12 2L2 7L12 12L22 7L12 2Z"
              fill="#6C6CFF"
              stroke="#6C6CFF"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <span>work management</span>
        </Link>
        <div className="sub-nav-links">
          <Link to="/overview" className="active">
            Overview
          </Link>
          <Link to="/marketing">For Marketing</Link>
          <Link to="/pmo">For PMO</Link>
          <Link to="/pricing">Pricing</Link>
        </div>
      </div>
    </nav>
  )
}

