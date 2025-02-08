import {GoogleLogin} from 'react-google-login';

const clientId = "402497065697-kaip15utdkkka9v7eice6l3d966vp8hg.apps.googleusercontent.com";

function Login() {

    const onSuccess = (res) => {console.log("Successful login")}
    const onFailure = (res) => {console.log ("Failed to log in")}

    <div id='loginButton'>

        <GoogleLogin

            clientID={clientId}
            buttonText="Log in"
            onSuccess={onSuccess}
            onFailure={onFailure}
            cookiePolicy={'single_host_origin'}
            isSignedIn={true}

        />

    </div>

}

export default Login;