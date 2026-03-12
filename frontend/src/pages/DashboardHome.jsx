import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import KpiCard from "../components/KpiCard";
import DashboardSkeleton from "../components/DashboardSkeleton";
import API from "../api/axios";

function DashboardHome() {

  const navigate = useNavigate(); 
  const [loading, setLoading] = useState(true);

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
    } finally {
      setLoading(false);
    }

  };

  if (loading) {
  return (
    <div className="p-8">
      <DashboardSkeleton />
    </div>
  );
}

  return (

    <div className="flex min-h-screen text-stone-800 bg-linear-to-br
  from-stone-100
  via-stone-50
  to-stone-200">

      <Sidebar />

      <div className="flex-1">

        <Navbar />

        <div className="p-8">

          <h1 className="text-3xl font-semibold mb-2">
          Dashboard
          </h1>

          <p className="text-stone-500 mb-8">
          Monitor your datasets and analytics insights
          </p>

          {/* KPI SECTION */}

          <div className="grid grid-cols-4 gap-6 mb-12">

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
              className="bg-white border border-stone-200 rounded-xl p-6 cursor-pointer hover:shadow-md hover:bg-stone-50 transition"
            >
              <h3 className="text-stone-500 text-sm mb-2">
                Manage Datasets
              </h3>

              <p className="text-lg font-semibold text-amber-600">
                View Uploaded Datasets
              </p>
            </div>


            <div
              onClick={() => navigate("/upload-dataset")}
              className="bg-white border border-stone-200 rounded-xl p-6 cursor-pointer hover:shadow-md hover:bg-stone-50 transition"
            >
              <h3 className="text-stone-500 text-sm mb-2">
                Upload Data
              </h3>

              <p className="text-lg font-semibold text-amber-600">
                Upload New Dataset
              </p>
            </div>


            <div
              onClick={() => navigate("/datasets")}
              className="bg-white border border-stone-200 rounded-xl p-6 cursor-pointer hover:shadow-md hover:bg-stone-50 transition"
            >
              <h3 className="text-stone-500 text-sm mb-2">
                Start Analytics
              </h3>

              <p className="text-lg font-semibold text-amber-600">
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