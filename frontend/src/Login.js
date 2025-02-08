import { useState } from "react"
import axios from "axios"
import { useNavigate, Link } from "react-router-dom"
import Swal from "sweetalert2"

function LoginForm(){

    const navigate = useNavigate()

    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")

    async function handleLogin(e){
        e.preventDefault()
        try {
            const requestBody = {email, password}
            const response = await axios.post('https://api.p2.lc2s5.foxhub.space/login', requestBody)
            localStorage.setItem('access_token', response.data.access_token)
            navigate('/')
        } catch (error) {
            console.log(error);
            Swal.fire({
                icon: "error",
                title: "Oops...",
                text: error.response.data.message
            });
        }
    }

    return (
        <div className="container" style={{marginTop:"10vh"}}>
            <form onSubmit={handleLogin}>
                <h2>Login to your account</h2>
                <p>Welcome back!</p>
                <div className="mb-3">
                    <label htmlFor="email" className="form-label">Email address :</label>
                    <input onChange={e => {setEmail(e.target.value)}} type="email" className="form-control" id="email"/>
                </div>
                <div className="mb-3">
                    <label htmlFor="password" className="form-label">Password :</label>
                    <input onChange={e => {setPassword(e.target.value)}} type="password" className="form-control" id="password"/>
                </div>
                <button type="submit" className="btn btn-primary">LOG IN</button>
                <p style={{marginTop:"2vh"}}>Don't have an account?<Link to={'/register'}>Create an account</Link></p>
                <p><br />Demo User: <br />Email: user@example.com <br />Password: password12345</p>
            </form>
        </div>
    )
}

export default LoginForm