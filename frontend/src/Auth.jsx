import { useState } from "react";

const API_URL = "http://127.0.0.1:8001";

function Auth({ onLoginSuccess }) {
  const [regUsername, setRegUsername] = useState("");
  const [regEmail, setRegEmail] = useState("");
  const [regPassword, setRegPassword] = useState("");
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [message, setMessage] = useState("");

  function handleRegister() {
    fetch(`${API_URL}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: regUsername,
        email: regEmail,
        password: regPassword,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.detail) {
          setMessage("Error: " + data.detail);
        } else {
          setMessage("Registered successfully! Now please log in.");
          setRegUsername("");
          setRegEmail("");
          setRegPassword("");
        }
      });
  }

  function handleLogin() {
    fetch(`${API_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: loginEmail,
        password: loginPassword,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.detail) {
          setMessage("Error: " + data.detail);
        } else {
          onLoginSuccess(data.access_token);
        }
      });
  }

  return (
    <div>
      <h3>Authentication</h3>

      <p><b>{message}</b></p>

      <b>Register New User</b><br /><br />
      <b>Username: </b>
      <input
        placeholder="Username"
        value={regUsername}
        onChange={(e) => setRegUsername(e.target.value)}
      />
      <br /><br />

      <b>Email: </b>
      <input
        placeholder="Email"
        value={regEmail}
        onChange={(e) => setRegEmail(e.target.value)}
      />
      <br /><br />

      <b>Password: </b>
      <input
        type="password"
        placeholder="Password"
        value={regPassword}
        onChange={(e) => setRegPassword(e.target.value)}
      />
      <br /><br />

      <button onClick={handleRegister}>Register</button>

      <br /><br />
      <hr />
      <br />

      <b>Login</b><br /><br />
      <b>Email: </b>
      <input
        placeholder="Email"
        value={loginEmail}
        onChange={(e) => setLoginEmail(e.target.value)}
      />
      <br /><br />

      <b>Password: </b>
      <input
        type="password"
        placeholder="Password"
        value={loginPassword}
        onChange={(e) => setLoginPassword(e.target.value)}
      />
      <br /><br />

      <button onClick={handleLogin}>Log In</button>
    </div>
  );
}

export default Auth;
