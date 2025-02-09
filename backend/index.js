import express from "express"
const studySchedule = "./backend_schedules/study_schedule_1739093364.js"

console.log(studySchedule);

const app = express()

app.get("/",(req,res)=>{
    res.send("Server is ready")
})

app.get("/api/studyschedule",(req,res)=>{
    res.send(studySchedule)
})

const port = process.env.PORT || 52804

app.listen(port,()=>{
    console.log(`Serve at http://localhost:${port}`)
})