import React, { useState, useEffect } from "react";

function AssetList() {
    const [assets, setAssets] = useState([]);

    useEffect(() => {
        fetch("http://localhost:8080/api/assets")
            .then((response) => response.json())
            .then((data) => setAssets(data))
            .catch((error) => console.error("Error fetching assets:", error));
    }, []);

    return (
        <div className="asset-list" style={{ background: "#fff", padding: "1.5rem", borderRadius: "0.5rem", boxShadow: "0 2px 10px rgba(0,0,0,0.08)" }}>
            <h2 style={{ marginBottom: "1rem", fontSize: "1.5rem" }}>Asset Inventory</h2>
            <div className="asset-list-container" style={{ overflowX: "auto" }}>
                <table style={{ width: "100%", borderCollapse: "collapse" }}>
                    <thead>
                        <tr>
                            <th style={{ width: "25%", textAlign: "left", padding: "0.5rem" }}>Asset Name</th>
                            <th style={{ width: "20%", textAlign: "left", padding: "0.5rem" }}>Type</th>
                            <th style={{ width: "55%", textAlign: "left", padding: "0.5rem" }}>Description</th>
                        </tr>
                    </thead>
                    <tbody>
                        {assets.length > 0 ? (
                            assets.map((asset, index) => (
                                <tr key={index} style={{ borderTop: "1px solid #ddd" }}>
                                    <td style={{ padding: "0.5rem", wordBreak: "break-word" }}>{asset.name}</td>
                                    <td style={{ padding: "0.5rem", wordBreak: "break-word" }}>{asset.type}</td>
                                    <td style={{ padding: "0.5rem", wordBreak: "break-word" }}>{asset.description}</td>
                                </tr>
                            ))
                        ) : (
                            <tr>
                                <td colSpan="3" style={{ padding: "1rem" }}>Loading assets...</td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default AssetList;
