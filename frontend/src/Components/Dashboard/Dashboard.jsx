import { Calendar } from "./Calendar"
import "./Dashboard.css"
import { useState } from "react"

export function Dashboard() {
  const [inputText, setInputText] = useState("")
  const [analysisResult, setAnalysisResult] = useState(null)
  const [error, setError] = useState(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  const handleSubmit = async () => {
    try {
      setIsAnalyzing(true)
      setError(null)
      const response = await fetch('http://localhost:8000/api/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText }),
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to submit topic')
      }
      
      const result = await response.json()
      console.log('Analysis result:', result)
      setAnalysisResult(result.result[0])
      setInputText("")
    } catch (error) {
      console.error('Error submitting text:', error)
      setError(error.message)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const handleCancel = async () => {
    try {
      setError(null)
      const response = await fetch('http://localhost:8000/api/cancel', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to cancel analysis')
      }
      
      const result = await response.json()
      console.log('Cancel result:', result)
      
      setIsAnalyzing(false)
      setError(null)
    } catch (error) {
      console.error('Error canceling analysis:', error)
      setError(error.message)
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
            disabled={isAnalyzing}
          />
          {!isAnalyzing ? (
            <button 
              className="start-studying-btn"
              onClick={handleSubmit}
            >
              Start Studying
            </button>
          ) : (
            <button 
              className="cancel-btn"
              onClick={handleCancel}
            >
              Cancel Analysis
            </button>
          )}
        </div>
        {error && (
          <div className="error-message">
            Error: {error}
          </div>
        )}
        {analysisResult && (
          <div className={`analysis-result ${analysisResult.Verdict ? 'procrastinating' : 'studying'}`}>
            {analysisResult.Verdict ? 
              '⚠️ Procrastination Detected!' : 
              '✅ On Track - Keep Studying!'}
            <div className="analysis-justification">
              {analysisResult.Justification}
            </div>
          </div>
        )}
        <Calendar />
      </main>
    </div>
  )
}

