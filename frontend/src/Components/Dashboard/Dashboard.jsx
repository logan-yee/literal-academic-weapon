import { Calendar } from "./Calendar"
import "./Dashboard.css"

export function Dashboard() {
  return (
    <div className="dashboard">
      <main className="dashboard-main">
        <button className="start-studying-btn">Start Studying</button>
        <Calendar />
      </main>
    </div>
  )
}

