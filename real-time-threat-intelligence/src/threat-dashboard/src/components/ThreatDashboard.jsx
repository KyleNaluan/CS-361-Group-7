import React from "react";
import ThreatLogs from "./ThreatLogs";
import RiskScores from "./RiskScores";
import RealTimeAlerts from "./RealTimeAlerts";
import AssetList from "./AssetList";
import RiskTrends from "./RiskTrends";
import IncidentResponse from "../components/IncidentResponse";
import CBASummary from "./CBASummary";

function ThreatDashboard() {
    return (
        <div>
            {/* Header */}
            <div className="dashboard-header" style={{ padding: "1.5rem 2rem", background: "#1f2937", color: "white" }}>
                <h1 className="dashboard-title" style={{ fontSize: "2rem", marginBottom: "0.5rem" }}>
                    Real-Time Threat Intelligence
                </h1>
                <p className="dashboard-subtitle" style={{ color: "#555" }}>
                    Live Threat Updates will be displayed here.
                </p>
            </div>

            {/* 🔷 Row 1: Logs + Alerts + Risk Trends */}
            <div className="row-1" style={{ display: "flex", gap: "1rem", padding: "1rem 1.5rem" }}>
                <div style={{ flex: 1 }}><ThreatLogs /></div>
                <div style={{ flex: 1 }}><RealTimeAlerts /></div>
                <div style={{ flex: 1 }}><RiskTrends /></div>
            </div>

            {/* 🔶 Row 2: Risk Scores + Asset Inventory + CBA Summary */}
            <div className="row-2" style={{ display: "flex", gap: "1.5rem", padding: "1rem 2rem" }}>
                <div style={{ flex: 1 }}><RiskScores /></div>
                <div style={{ flex: 1 }}><AssetList /></div>
                <div style={{ flex: 1 }}><CBASummary /></div>
            </div>

            {/* 🔵 Final: Incident Response */}
            <div className="incident-response-section" style={{ padding: "2rem" }}>
                <IncidentResponse />
            </div>
        </div>
    );
}

export default ThreatDashboard;
