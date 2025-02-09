import { Outlet } from 'react-router-dom'
import { Sidebar } from "../Sidebar"
import "./DashboardLayout.css"

const DashboardLayout = () => {
  return (
    <div className="dashboard-layout">
      <Sidebar />
      <main className="dashboard-main">
        <Outlet />
      </main>
    </div>
  )
}

export default DashboardLayout