import { Calendar } from "./Calendar"
import "./Dashboard.css"
import { useState } from "react"

export function Dashboard() {
  const [inputText, setInputText] = useState("")

  const handleSubmit = async () => {
    try {
      const response = await fetch('/api/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText }),
      })
      if (!response.ok) {
        throw new Error('Network response was not ok')
      }
      // Clear input after successful submission
      setInputText("")
    } catch (error) {
      console.error('Error submitting text:', error)
    }
  }

  return (
    <div className="dashboard">
      <main className="dashboard-main">
        <div className="input-container">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="What topic are you studying...?"
            className="study-input"
          />
          <button 
            className="start-studying-btn"
            onClick={handleSubmit}
          >
            Start Studying
          </button>
        </div>
        <Calendar />
      </main>
    </div>
  )
}

