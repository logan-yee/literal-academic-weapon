import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import { SiteHeader } from "./Components/SiteHeader/SiteHeader"
import { HeroSection } from "./Components/HeroSection/HeroSection"
import { Dashboard } from "./Components/Dashboard/Dashboard"
import "./App.css"
import LoginSignup from "./Components/LoginSignup/LoginSignup"

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
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/LoginSignup" element={<LoginSignup />} />
        </Routes>
      </div>
    </Router>

  )
}

export default App

