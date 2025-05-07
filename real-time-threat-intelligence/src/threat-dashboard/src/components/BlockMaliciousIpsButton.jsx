import React, { useState } from "react";

const BlockMaliciousIpsButton = () => {
    const [message, setMessage] = useState("");

    const handleBlockMaliciousIps = async () => {
        try {
            const response = await fetch("/api/block_malicious_ips", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
            });

            const data = await response.json();
            setMessage(data.message); // Show success or error message
        } catch (error) {
            setMessage("Error blocking IPs.");
        }
    };

    return (
        <div>
            <button onClick={handleBlockMaliciousIps}>Block Malicious IPs</button>
            {message && <p>{message}</p>}
        </div>
    );
};

export default BlockMaliciousIpsButton;
