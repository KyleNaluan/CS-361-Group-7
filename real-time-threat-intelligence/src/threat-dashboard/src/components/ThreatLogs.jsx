import React, { useEffect, useState } from "react";

function ThreatLogs() {
  const [threats, setThreats] = useState([]);
  const [filteredThreats, setFilteredThreats] = useState([]);
  const [minRiskScore, setMinRiskScore] = useState(0);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/threats")
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return res.json();
      })
      .then((data) => {
        setThreats(data);
        setFilteredThreats(data);
      })
      .catch((err) => {
        console.error("Error fetching threat data:", err);
        setError("Failed to load threat logs.");
      });
  }, []);

  useEffect(() => {
    const filtered = threats.filter((t) => t.risk_score >= minRiskScore);
    setFilteredThreats(filtered);
  }, [minRiskScore, threats]);

  return (
    <div className="threat-logs">
      <h2 className="section-title">Threat Logs</h2>

      {/* 🔍 Filter Dropdown */}
      <label htmlFor="riskFilter">Filter by Risk Score:</label>
      <select
        id="riskFilter"
        value={minRiskScore}
        onChange={(e) => setMinRiskScore(Number(e.target.value))}
        style={{ margin: "10px 0" }}
      >
        <option value={0}>All Threats</option>
        <option value={10}>≥ 10</option>
        <option value={20}>≥ 20</option>
      </select>

      {error ? (
        <p className="body-text">{error}</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>IP Address</th>
              <th>Threat Type</th>
              <th>Risk Score</th>
            </tr>
          </thead>
          <tbody>
            {filteredThreats.length > 0 ? (
              filteredThreats.map((t, index) => (
                <tr key={index}>
                  <td>{t.ip}</td>
                  <td>{t.type}</td>
                  <td>{t.risk_score}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="3">No threats match the filter.</td>
              </tr>
            )}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default ThreatLogs;
