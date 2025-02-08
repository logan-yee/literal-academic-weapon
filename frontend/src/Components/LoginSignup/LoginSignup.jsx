import React, { useState } from "react";
import './LoginSignup.css'

const LoginSignup = () => {

    /*
    const initValues = {name:"", email:"", password:""}
    const formValues = [formValues, setFormValues] = useState(initValues)
    const formErrors = [formErrors, setFormErrors] = useState({});
    const isSubmit = [isSubmit, setIsSubmit] = useState(false);

    const change = (e) => {

        const {name, value} = e.target;
        setFormValues({...formValues, [name]: value});

    }

    const submit = (e) => {

        e.preventDefault();
        setFormErrors(validate(formValues));

    }

    const validate = (values) => {

        const errors = {};
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/i;

        if (!values.name) {errors.name = "Name cannot be blank";}
        if (!values.email) {errors.email = "Email cannot be blank";}
        if (!values.password) {errors.password = "Password cannot be blank";}

        return errors;

    }*/

    return (

        <div className="container">

            <div className="header">

                <div className="text">Login</div>
                <div className="underline"></div>

            </div>

            <div className="inputs" /*onSubmit={submit}*/>

                <div className="input">
                    <input type="name" placeholder="Name" /*value={formValues.name} onChange={change}*//>
                </div>

                <div className="input">
                    <input type="email" placeholder="Email" /*value={formValues.email} onChange={change}*//>
                </div>

                <div className="input">
                    <input type="password" placeholder="Password" /*value={formValues.password} onChange={change}*//>
                </div>

            </div>

            <div className="submit-container">

                <div className="submit">Login</div>

            </div>

        </div>

    )

}

export default LoginSignup;