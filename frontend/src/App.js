import { BrowserRouter as Router } from "react-router-dom"
import { HeroSection } from "./Components/HeroSection/HeroSection"
import "./App.css"
import LoginSignup from "./Components/LoginSignup/LoginSignup"

function App() {
  return (
    <Router>
      <div className="app">
        <main>
          <HeroSection />
        </main>
      </div>
    </Router>
  )
}

export default App