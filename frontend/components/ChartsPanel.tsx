"use client";

import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function ChartsPanel({
  components,
}: {
  components?: { style: number; image: number } | null;
}) {
  const stylePct = components ? Math.round(components.style * 100) : 65;
  const imagePct = components ? Math.round(components.image * 100) : 72;
  const data = {
    labels: ["Style", "Image"],
    datasets: [
      {
        label: "Contribution (%)",
        data: [stylePct, imagePct],
        backgroundColor: "rgba(99, 102, 241, 0.6)",
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: "top" as const },
      title: { display: true, text: "Identity Confidence Breakdown" },
    },
  };

  return (
    <div className="bg-background border border-black/10 dark:border-white/10 rounded-md p-4">
      <Bar data={data} options={options} />
    </div>
  );
}


