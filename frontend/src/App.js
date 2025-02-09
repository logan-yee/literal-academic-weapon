import { BrowserRouter as Router } from "react-router-dom"
import { SiteHeader } from "./Components/SiteHeader/SiteHeader"
import { SubNav } from "./Components/SubNav/SubNav"
import { HeroSection } from "./Components/HeroSection/HeroSection"
import "./App.css"
import LoginSignup from "./Components/LoginSignup/LoginSignup"

function App() {
  return (
    <Router>
      <div className="app">
        <SiteHeader />
        <SubNav />
        <main>
          <HeroSection />
        </main>
      </div>
    </Router>
  )
}

export default App