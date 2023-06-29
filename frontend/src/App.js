import React, { useState } from "react";

function App() {
  const [data, setData] = useState([]);

  const handleUpload = async (event) => {
    event.preventDefault();

    const file = event.target.files[0];
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const fetchData = async () => {
    try {
      const response = await fetch("http://localhost:8000/data");
      const data = await response.json();
      console.log(data);
      setData(data.data);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div>
      <h1>Stock App</h1>
      <input type="file" onChange={handleUpload} />
      <button onClick={fetchData}>Get Data</button>
      <table>
        <thead>
          <tr>
            <th>Date Time</th>
            <th>Open</th>
            <th>High</th>
            <th>Low</th>
            <th>Close</th>
            <th>Volume</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr key={index}>
              <td>{row.datetime}</td>
              <td>{row.close}</td>
              <td>{row.high}</td>
              <td>{row.low}</td>
              <td>{row.open}</td>
              <td>{row.volume}</td>
              <td>{row.instrument}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
