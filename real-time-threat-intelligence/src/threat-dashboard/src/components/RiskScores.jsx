import React, { useState, useEffect } from "react";



function RiskScores() {
  const [tvaData, setTvaData] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
      fetch("http://localhost:8080/api/tva-mapping")
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        console.log("Fetched TVA data:", data);
        setTvaData(data);
      })
      .catch((error) => {
        console.error("Error fetching TVA mapping:", error);
        setError("Failed to load risk scores.");
      });
  }, []);

  return (
    <div className="risk-scores">
      <h2>Risk Scores (TVA Mapping)</h2>
      <div className="risk-scores-container">
        <table>
          <thead>
            <tr>
              <th>Asset</th>
              <th>Threat</th>
              <th>Vulnerability</th>
              <th>Likelihood</th>
              <th>Impact</th>
              <th>Risk Score</th>
            </tr>
          </thead>
          <tbody>
            {tvaData.length > 0 ? (
              tvaData.map((entry, index) => (
                <tr key={index}>
                  <td>{entry.asset}</td>
                  <td>{entry.threat}</td>
                  <td>{entry.vulnerability}</td>
                  <td>{entry.likelihood}</td>
                  <td>{entry.impact}</td>
                  <td>{entry.risk_score}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="6">Loading risk scores...</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default RiskScores;
