import React from "react";
import "./Stats.css"
import { buildStyles, CircularProgressbar } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

const Stats = () => {

    let work = 20;
    let proc = 20;
    let total = work+proc;
    let workperc = (work/total)*100;
    let procperc = (proc/total)*100;

    return (
        <div className="statistics-section">
            <div className="statistics-container">
                <header className="statistics-header">
                    <div className="statistics-title">Productivity Stats</div>
                    <div className="statistics-underline"></div>
                </header>

                <div className="statistics-stats">
                    <div className="statistics-stat">
                        <span className="statistics-work-value">{work}</span>
                        <span className="statistics-label">Hours Working</span>
                    </div>

                    <div className="statistics-stat">
                        <span className="statistics-proc-value">{proc}</span>
                        <span className="statistics-label">Hours Procrastinating</span>
                    </div>
                </div>

                <div className="statistics-circles">
                    <div className="statistics-circle">
                        <CircularProgressbar 
                            value={workperc} 
                            text={`${workperc}%`} 
                            styles={buildStyles({
                                pathColor: 'lightgreen',
                                textColor: 'lightgreen'
                            })}
                        />
                    </div>

                    <div className="statistics-circle">
                        <CircularProgressbar 
                            value={procperc} 
                            text={`${procperc}%`} 
                            styles={buildStyles({
                                pathColor: 'red',
                                textColor: 'red'
                            })}
                        />
                    </div>
                </div>
            </div>
        </div>
    )

}

export default Stats;