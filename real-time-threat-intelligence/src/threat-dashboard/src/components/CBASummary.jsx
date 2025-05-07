import React from "react";

function CBASummary() {
    const alePrior = 50000;
    const alePost = 10000;
    const acs = 15000;
    const cba = alePrior - alePost - acs;

    return (
        <div className="cba-summary" style={{
            background: "#f3f4f6",
            padding: "1.5rem",
            borderRadius: "0.75rem",
            marginTop: "2rem",
            boxShadow: "0 4px 12px rgba(0,0,0,0.1)"
        }}>
            <h2 style={{ fontSize: "1.5rem", marginBottom: "1rem" }}>💰 Cost-Benefit Analysis</h2>
            <p><strong>ALE Before:</strong> ${alePrior}</p>
            <p><strong>ALE After:</strong> ${alePost}</p>
            <p><strong>Annual Cost of Security (ACS):</strong> ${acs}</p>
            <p><strong>Net Benefit:</strong> ${cba}</p>
            <p style={{ color: cba > 0 ? "green" : "red", fontWeight: "bold" }}>
                {cba > 0
                    ? "✅ This security control is cost-effective."
                    : cba < 0
                        ? "❌ This control costs more than it saves."
                        : "⚖️ Break-even result."}
            </p>
        </div>
    );
}

export default CBASummary;
