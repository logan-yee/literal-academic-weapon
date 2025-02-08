import { GoogleLogout } from "react-google-login";

const clientId = "402497065697-88cisicmup8ptpnjihse0qjpffpmpfd4.apps.googleusercontent.com";

function Logout() {

    const onSuccess = () => {console.log("Successful logout");}

        <div id="logoutButton">

            <GoogleLogout

                clientId={clientId}
                buttonText="Log out"
                onLogoutSuccess={onSuccess}
                isSignedIn={false}

            />

        </div>

}

export default Logout;