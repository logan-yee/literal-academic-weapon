import "./App.css"
// import Logout from "./Components/logout";
// import { useEffect } from "react";
// import {gapi} from "gapi-script";
// import Login from "./Components/login";
// import stats from "./Components/Stats/Stats.jsx"
import Stats from "./Components/Stats/Stats.jsx";
// import LoginSignup from "./Components/LoginSignup/LoginSignup.jsx";
// const clientId = "402497065697-kaip15utdkkka9v7eice6l3d966vp8hg.apps.googleusercontent.com";

function App() {

//   useEffect(() => {
  
//     function start() {

//       gapi.client.init({

//         clientId:clientId,
//         scope:""

//       })

//     };

//     gapi.load("client:auth2", start)
  
// });

  return (

    <div>

      <Stats />

    </div>

  );

}

export default App;