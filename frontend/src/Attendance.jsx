import { useState, useEffect } from "react";

function Attendance({ token, onLogout }) {
  const [records, setRecords] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8001/attendance", {
      method: "GET",
      headers: {
        token: token,
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setRecords(data);
        }
      });
  }, []);

  return (
    <div>
      <h3>Attendance Dashboard</h3>
      <button onClick={onLogout}>Logout</button>
      <br /><br />

      {records.length === 0 ? (
        <p>No attendance records found.</p>
      ) : (
        records.map((item, index) => (
          <div key={index}>
            <p>Student Name: {item.student_name || item.name}</p>
            <p>Roll Number: {item.roll_no}</p>
            <p>Attendance Date: {item.attendance_date || item.date}</p>
            <p>Status: {item.status || (item.is_present ? "Present" : "Absent")}</p>
            <hr />
          </div>
        ))
      )}
    </div>
  );
}

export default Attendance;
