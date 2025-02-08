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

        <div className="container">

            <header>

                <div className="text">Productivity Stats</div>
                <div className="underline"></div>

            </header>

            <div className="stats">

                <div className="stat">
                    
                    <span className="subsection">Hours Working: </span>
                    <span className="value"> {work}</span>
                    
                </div>

                <div className="stat">
                    
                    <span className="subsection">Hours Procrastinating: </span> 
                    <span className="value"> {proc}</span>

                </div>

            </div>

            <div className="circles">

                <div className="circle"><CircularProgressbar 
                    value={workperc} 
                    text={`${workperc}%`} 
                    
                    styles={buildStyles({

                        pathColor: '#e62429',
                        textColor: '#e62429'

                    })}
                
                /></div>

                <div className="circle"><CircularProgressbar 
                    value={procperc} 
                    text={`${procperc}%`} 
                    
                    styles={buildStyles({

                        pathColor: '#e62429',
                        textColor: '#e62429'

                    })}

                /></div>

            </div>

        </div>

    )

}

export default Stats;