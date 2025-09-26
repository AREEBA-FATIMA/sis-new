"use client"

import { Pie } from "react-chartjs-2"
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js"

ChartJS.register(ArcElement, Tooltip, Legend)

type GenderChartProps = {
  male: number
  female: number
}

export default function GenderPieChart({ male, female }: GenderChartProps) {
  const data = {
    labels: ["Male", "Female"],
    datasets: [
      {
        label: "Gender Ratio",
        data: [male, female],
        backgroundColor: ["#36A2EB", "#FF6384"],
        borderColor: ["#ffffff", "#ffffff"],
        borderWidth: 1,
      },
    ],
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false, // important to control height
    plugins: {
      legend: {
        position: "bottom" as const,
      },
    },
  }

  return (
    <div style={{ width: "100%", maxWidth: "400px", height: "300px", margin: "0 auto" }}>
      <Pie data={data} options={options} />
    </div>
  )
}

