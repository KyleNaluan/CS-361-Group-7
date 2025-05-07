import React, { useEffect, useState } from "react";

function RealTimeAlerts() {
    const [alerts, setAlerts] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch("http://127.0.0.1:8080/api/threats") // same endpoint
            .then((res) => {
                if (!res.ok) throw new Error("Failed to fetch alerts");
                return res.json();
            })
            .then((data) => {
                setAlerts(data.slice(0, 3)); // Limit to 3 most recent
            })
            .catch((err) => {
                setError(err.message);
            });
    }, []);

    return (
        <div className="real-time-alerts">
            <h2 className="section-title">Real-Time Alerts</h2>
            {error ? (
                <p className="body-text">{error}</p>
            ) : (
                <ul>
                    {alerts.map((alert, idx) => (
                        <li key={idx}>
                            ⚠️ <strong>{alert.type}</strong> from <em>{alert.source}</em> — Risk Score: <b>{alert.risk_score}</b>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default RealTimeAlerts;
