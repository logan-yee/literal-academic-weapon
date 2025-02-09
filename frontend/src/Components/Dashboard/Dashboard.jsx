import { Calendar } from "./Calendar"
import "./Dashboard.css"
import { useState } from "react"

export function Dashboard() {
  const [inputText, setInputText] = useState("")
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  const handleSubmit = async () => {
    try {
      const response = await fetch('/api/analyze-screenshots', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ topic: inputText }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to start screenshot analysis');
      }
      
      // Don't clear input text here since we want to show the cancel button
      // Instead, you might want to set some state to track that analysis is running
      setIsAnalyzing(true);
    } catch (error) {
      console.error('Error starting screenshot analysis:', error);
    }
  }

  const handleCancel = async () => {
    try {
      const response = await fetch('/api/cancel-analysis', {
        method: 'POST',
      });
      
      if (!response.ok) {
        throw new Error('Failed to cancel analysis');
      }
      
      setIsAnalyzing(false);
      setInputText('');
    } catch (error) {
      console.error('Error canceling analysis:', error);
    }
  }

  return (
    <div className="dashboard-content">
      <div className="content-wrapper">
        <div className="input-container">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="What topic are you studying...?"
            className="study-input"
            disabled={isAnalyzing}
          />
          <button 
            className={isAnalyzing ? "cancel-btn active" : "start-studying-btn"}
            onClick={isAnalyzing ? handleCancel : handleSubmit}
          >
            {isAnalyzing ? "Cancel" : "Start Studying"}
          </button>
        </div>
        <Calendar />
      </div>
    </div>
  )
}

