import { useState } from "react";
import Auth from "./Auth";
import Attendance from "./Attendance";

export default function App() {
  const [token, setToken] = useState("");

  function handleLoginSuccess(newToken) {
    setToken(newToken);
  }

  function handleLogout() {
    setToken("");
  }

  return (
    <div>
      <h2 style={{ textAlign: "center" }}>
        Student Attendance Tracker
      </h2>

      {!token ? (
        <Auth onLoginSuccess={handleLoginSuccess} />
      ) : (
        <Attendance token={token} onLogout={handleLogout} />
      )}
    </div>
  );
}
