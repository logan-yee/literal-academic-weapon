import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import { SiteHeader } from "./Components/SiteHeader/SiteHeader"
import { HeroSection } from "./Components/HeroSection/HeroSection"
import { Dashboard } from "./Components/Dashboard/Dashboard"
import "./App.css"
import LoginSignup from "./Components/LoginSignup/LoginSignup"
import Stats from "./Components/Stats/Stats"
import DashboardLayout from "./Components/Dashboard/Layout/DashboardLayout"
import Profile from "./Components/Profile/Profile"


function App() {
  return (
    <Router>
      <div className="app">
        <SiteHeader />
        <Routes>
          <Route
            path="/"
            element={
              <main>
                <HeroSection />
              </main>
            }
          />
          <Route path="/dashboard" element={<DashboardLayout><Dashboard /></DashboardLayout>} />
          <Route path="/LoginSignup" element={<LoginSignup />} />
          <Route path="/stats" element={<DashboardLayout><Stats /></DashboardLayout>} />
          <Route path="/dashboard/profile" element={<DashboardLayout><Profile /></DashboardLayout>} />
        </Routes>
      </div>
    </Router>

  )
}

export default App

