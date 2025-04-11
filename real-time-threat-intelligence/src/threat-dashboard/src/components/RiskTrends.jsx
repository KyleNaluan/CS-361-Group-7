import React from "react";
import { Line } from "react-chartjs-2";
import {
    Chart as ChartJS,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement,
    Title,
    Tooltip,
    Legend,
} from "chart.js";

ChartJS.register(
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement,
    Title,
    Tooltip,
    Legend
);

function RiskTrends() {
    // Example Data - No live data yet
    const data = {
        labels: ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6"],
        datasets: [
            {
                label: "Average Risk Score",
                data: [10, 22, 30, 35, 42, 38],
                fill: false,
                borderColor: "red",
                tension: 0.3,
                pointBackgroundColor: "black",
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: "top",
            },
            title: {
                display: true,
                text: "Risk Score Trend (by Week)",
            },
        },
        scales: {
            y: {
                beginAtZero: true,
                max: 50,
            },
        },
    };

    return (
        <div className="risk-trends">
            <h2 className="section-title">Risk Trends</h2>
            <div style={{ height: "250px" }}>
                <Line data={data} options={options} />
            </div>
        </div>
    );
}

export default RiskTrends;
