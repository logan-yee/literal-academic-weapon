import { useState, useEffect } from "react";
import "./LoginSignup.css";

function LoginSignup() {
  const initialValues = { username: "", email: "", password: "" };
  const [formValues, setFormValues] = useState(initialValues);
  const [formErrors, setFormErrors] = useState({});
  const [isSubmit, setIsSubmit] = useState(false);

  const hardName = "Naufil";
  const hardEmail = "naufilansari05@gmail.com";
  const hardPassword = "1234"

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormValues({ ...formValues, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setFormErrors(validate(formValues));
    setIsSubmit(true);
  };

  useEffect(() => {
    console.log(formErrors);
    if (Object.keys(formErrors).length === 0 && isSubmit) {
      console.log(formValues);
    }
  }, [formErrors]);
  const validate = (values) => {
    const errors = {};
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/i;
    if (!values.username) {
        errors.username = "Username is required!";
    } else if (values.username !== hardName) {
        errors.username = "Username does not exist";
    }
    if (!values.email) {
        errors.email = "Email is required!";
    } else if (!regex.test(values.email)) {
        errors.email = "This is not a valid email format!";
    } else if (values.email !== hardEmail) {
        errors.email = "Email does not exist";
    }
    if (!values.password) {
        errors.password = "Password is required";
    } else if (values.password.length < 4) {
        errors.password = "Password must be more than 4 characters";
    } else if (values.password.length > 10) {
        errors.password = "Password cannot exceed more than 10 characters";
    } else if (values.password !== hardPassword) {
        errors.password = "Incorrect password"
    }
    return errors;
  };

//   const correct = (values) => {

//     return (values.name === "Naufil" && values.email === "muhammadnaufil.ansari@ontariotechu.net" && values.password === "1234");

//   }

  return (
    <div className="container">
      {Object.keys(formErrors).length === 0 && isSubmit ? (
        <div className="ui message success">Signed in successfully</div>
      ) : (
        <div className="ui message failure">Failed to sign in </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="header"><h1>Login Form</h1></div>
        <div className="underline"></div>
        <div className="ui-form">
          <div className="field">
            <label>Username: </label>
            <input
              type="text"
              name="username"
              placeholder="Username"
              value={formValues.username}
              onChange={handleChange}
            />
          </div>
          <span className="form"><p>{formErrors.username}</p></span>
          <div className="field">
            <label>Email: </label>
            <input
              type="text"
              name="email"
              placeholder="Email"
              value={formValues.email}
              onChange={handleChange}
            />
          </div>
          <p className="form">{formErrors.email}</p>
          <div className="field">
            <label>Password: </label>
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formValues.password}
              onChange={handleChange}
            />
          </div>
          <p className="form">{formErrors.password}</p>
          <div className="submit-container"><button className="submit" onClick={handleSubmit}>Submit</button></div>
        </div>
      </form>
    </div>
  );
}

export default LoginSignup;