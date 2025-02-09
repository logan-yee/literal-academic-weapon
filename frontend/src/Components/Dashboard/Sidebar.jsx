import { Link } from "react-router-dom"
import "./Sidebar.css"

export function Sidebar() {
  return (
    <aside className="sidebar">
      <nav>
        <ul>
          <li>
            <Link to="/dashboard">Dashboard</Link>
          </li>
          <li>
            <Link to="/dashboard/statistics">Statistics</Link>
          </li>
          <li>
            <Link to="/dashboard/profile">Profile</Link>
          </li>
        </ul>
      </nav>
    </aside>
  )
}

