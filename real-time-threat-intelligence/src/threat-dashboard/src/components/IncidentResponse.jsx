import React, { useState, useEffect } from "react";

function IncidentResponse() {
    const [responses, setResponses] = useState([]);
    const [expandedIndex, setExpandedIndex] = useState(null);

    useEffect(() => {
        fetch("http://localhost:8080/api/incidents")
            .then((res) => res.json())
            .then((data) => {
                console.log("Fetched incident data:", data); // Debugging line
                setResponses(data);
            })
            .catch((err) => {
                console.error("Failed to fetch incident responses:", err);
            });
    }, []);

    const toggleExpand = (index) => {
        setExpandedIndex(expandedIndex === index ? null : index);
    };

    const getPriorityClass = (priority) => {
        switch (priority?.toLowerCase()) {
            case "high":
                return "priority-badge high";
            case "medium":
                return "priority-badge medium";
            case "low":
                return "priority-badge low";
            default:
                return "priority-badge";
        }
    };

    return (
        <div style={{ padding: "20px" }}>
            <h2 style={{ fontSize: "22px", fontWeight: "bold", textAlign: "center" }}>
                🛡 Incident Response Plans
            </h2>

            {responses.length === 0 ? (
                <p style={{ textAlign: "center", color: "#777", marginTop: "10px" }}>
                    No incident responses available.
                </p>
            ) : (
                <div style={{ marginTop: "20px" }}>
                    {responses.map((res, index) => (
                        <div
                            key={index}
                            style={{
                                border: "1px solid #ccc",
                                borderRadius: "10px",
                                padding: "15px",
                                marginBottom: "15px",
                                backgroundColor: "#f8f9fa",
                                boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
                                cursor: "pointer"
                            }}
                            onClick={() => toggleExpand(index)}
                        >
                            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                                <div>
                                    <p style={{ fontWeight: "bold", fontSize: "18px" }}>
                                        {res?.threat_name || "Unknown Threat"}
                                    </p>
                                    <span className={getPriorityClass(res?.priority)}>
                                        {res?.priority || "Unknown"} Priority
                                    </span>
                                </div>
                                <p style={{ fontSize: "14px", color: "#555" }}>Risk Score: {res?.risk_score || "N/A"}</p>
                            </div>

                            {expandedIndex === index && (
                                <div style={{ marginTop: "10px", fontSize: "14px", color: "#333" }}>
                                    <p><strong>NIST Phases:</strong></p>
                                    <ul style={{ marginBottom: "10px", paddingLeft: "20px" }}>
                                        {(res?.nist_phases || []).map((phase, i) => (
                                            <li key={i}>• {phase}</li>
                                        ))}
                                    </ul>

                                    <p><strong>Mitigation Strategy:</strong></p>
                                    <p style={{ fontStyle: "italic" }}>{res?.mitigation || "N/A"}</p>

                                    <p style={{ marginTop: "10px" }}><strong>Response Steps:</strong></p>
                                    <ul style={{ paddingLeft: "20px" }}>
                                        {(res?.steps || []).map((step, i) => (
                                            <li key={i} style={{ marginBottom: "6px" }}>• {step}</li>
                                        ))}
                                    </ul>

                                    <p style={{ marginTop: "10px", fontSize: "12px", color: "#666" }}>
                                        IP Address: {res?.ip || "N/A"}
                                    </p>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default IncidentResponse;
