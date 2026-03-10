import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import KpiCard from "../components/KpiCard";

import API from "../api/axios";

function DashboardHome() {

  const navigate = useNavigate();

  const [stats, setStats] = useState({
    datasets: 0,
    rows: 0,
    analytics: 0,
    insights: 0
  });

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {

    try {

      const res = await API.get("/datasets");

      const datasets = res.data || [];

      let totalRows = 0;

      datasets.forEach(d => {
        totalRows += d.rows || 0;
      });

      setStats({
        datasets: datasets.length,
        rows: totalRows,
        analytics: datasets.length,
        insights: datasets.length * 5
      });

    } catch (err) {
      console.error("Failed to load dashboard stats", err);
    }

  };

  return (

    <div className="flex">

      <Sidebar />

      <div className="flex-1">

        <Navbar />

        <div className="p-8">

          <h1 className="text-2xl font-bold mb-6">
            Dashboard
          </h1>

          {/* KPI SECTION */}

          <div className="grid grid-cols-4 gap-6 mb-10">

            <KpiCard
              title="Datasets Uploaded"
              value={stats.datasets}
            />

            <KpiCard
              title="Rows Processed"
              value={stats.rows}
            />

            <KpiCard
              title="Analytics Generated"
              value={stats.analytics}
            />

            <KpiCard
              title="Insights Created"
              value={stats.insights}
            />

          </div>


          {/* QUICK ACTIONS */}

          <div className="grid grid-cols-3 gap-6">

            <div
              onClick={() => navigate("/datasets")}
              className="bg-white shadow rounded p-6 cursor-pointer hover:shadow-md"
            >
              <h3 className="text-gray-500 text-sm mb-2">
                Manage Datasets
              </h3>

              <p className="text-lg font-semibold text-indigo-600">
                View Uploaded Datasets
              </p>
            </div>


            <div
              onClick={() => navigate("/upload-dataset")}
              className="bg-white shadow rounded p-6 cursor-pointer hover:shadow-md"
            >
              <h3 className="text-gray-500 text-sm mb-2">
                Upload Data
              </h3>

              <p className="text-lg font-semibold text-indigo-600">
                Upload New Dataset
              </p>
            </div>


            <div
              onClick={() => navigate("/datasets")}
              className="bg-white shadow rounded p-6 cursor-pointer hover:shadow-md"
            >
              <h3 className="text-gray-500 text-sm mb-2">
                Start Analytics
              </h3>

              <p className="text-lg font-semibold text-indigo-600">
                Analyze Dataset
              </p>
            </div>

          </div>

        </div>

      </div>

    </div>

  );
}

export default DashboardHome;