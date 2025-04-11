import React from "react";
import ThreatLogs from "./ThreatLogs";
import RiskScores from "./RiskScores";
import RealTimeAlerts from "./RealTimeAlerts";
import AssetList from "./AssetList";
import RiskTrends from "./RiskTrends";

function ThreatDashboard() {
  return (
    <div>
      {/* Header */}
      <div className="dashboard-header">
        <h1 className="dashboard-title">Real-Time Threat Intelligence</h1>
        <p className="dashboard-subtitle">
          Live Threat Updates will be displayed here.
        </p>
      </div>

      {/* Dashboard Grid */}
      <div className="dashboard-grid">
        {/* Left Column */}
        <div className="left-column">
          <ThreatLogs />
          <RiskScores />
        </div>

        {/* Right Column */}
        <div className="right-column">
          <RealTimeAlerts />
          <RiskTrends />
        </div>



        {/* Bottom Section */}
        <div className="asset-section">
          <AssetList />
        </div>
      </div>

    </div>
  );
}

export default ThreatDashboard;
