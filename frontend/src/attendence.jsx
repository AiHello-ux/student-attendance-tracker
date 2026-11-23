import { useState, useEffect } from "react";

function Attendence({ token, onLogout }) {
  const [records, setRecords] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8001/attendance", {
      method: "GET",
      headers: {
        token: token,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        setRecords(data);
      });
  }, []);

  return (
    <div>
      <h3>Attendance Dashboard</h3>
      <button onClick={onLogout}>Logout</button>

      {records.length === 0 ? (
        <p>No attendance records found.</p>
      ) : (
        records.map((item, index) => (
          <div key={index}>
            <p>Student Name: {item.student_name}</p>
            <p>Roll Number: {item.roll_no}</p>
            <p>Attendance Date: {item.attendance_date}</p>
            <p>Status: {item.status}</p>
          </div>
        ))
      )}
    </div>
  );
}

export default Attendence;