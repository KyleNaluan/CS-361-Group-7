import React, { useEffect, useState } from "react";

function ThreatLogs() {
    const [threats, setThreats] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch("http://127.0.0.1:8080/api/threats")
            .then((res) => {
                if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
                return res.json();
            })
            .then((data) => {
                setThreats(data);
            })
            .catch((err) => {
                console.error("Error fetching threat logs:", err);
                setError("Failed to load threat logs.");
            });
    }, []);

    return (
        <div className="threat-logs">
            <h2 className="section-title">Threat Logs</h2>

            {error ? (
                <p className="body-text">{error}</p>
            ) : (
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>IP Address</th>
                            <th>Threat Type</th>
                            <th>Risk Score</th>
                            <th>Details</th>
                            <th>Source</th>
                        </tr>
                    </thead>
                    <tbody>
                        {threats.length > 0 ? (
                            threats.map((t, index) => (
                                <tr key={index}>
                                    <td>{new Date(t.timestamp).toLocaleString()}</td>
                                    <td>{t.ip}</td>
                                    <td>{t.type}</td>
                                    <td>{t.risk_score}</td>
                                    <td>{t.details || "N/A"}</td>
                                    <td>{t.source}</td>
                                </tr>
                            ))
                        ) : (
                            <tr>
                                <td colSpan="6">No threat logs available.</td>
                            </tr>
                        )}
                    </tbody>
                </table>
            )}
        </div>
    );
}

export default ThreatLogs;
