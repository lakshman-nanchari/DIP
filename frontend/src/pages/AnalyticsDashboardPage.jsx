import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import KpiCard from "../components/KpiCard";
import InsightsPanel from "../components/InsightsPanel";
import API from "../api/axios";

function AnalyticsDashboardPage() {

  const { dataset_id } = useParams();
  const navigate = useNavigate();

  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {

    if (!dataset_id) {
      navigate("/datasets");
      return;
    }

    fetchDashboard();

  }, [dataset_id]);


  const fetchDashboard = async () => {

    try {

      const res = await API.get(`/analytics/${dataset_id}/dashboard`);

      console.log("Dashboard data:", res.data);

      setDashboard(res.data.dashboard);

    } catch (err) {

      console.error("Failed to load dashboard", err);

    } finally {

      setLoading(false);

    }

  };


  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <p className="text-lg font-semibold">
          Loading Analytics Dashboard...
        </p>
      </div>
    );
  }


  return (
    <div className="flex">

      <Sidebar />

      <div className="flex-1">

        <Navbar />

        <div className="p-8">

          <h1 className="text-2xl font-bold mb-6">
            Analytics Dashboard
          </h1>


          {/* KPI SECTION */}

          <div className="grid grid-cols-4 gap-6 mb-8">

            <KpiCard
              title="Average Amount"
              value={dashboard?.kpis?.average_Amount ?? "N/A"}
            />

            <KpiCard
              title="Average Boxes"
              value={dashboard?.kpis?.average_Boxes ?? "N/A"}
            />

            <KpiCard
              title="Total Rows"
              value={dashboard?.kpis?.total_rows ?? "N/A"}
            />

            <KpiCard
              title="Total Columns"
              value={dashboard?.kpis?.total_columns ?? "N/A"}
            />

          </div>


          {/* INSIGHTS */}

          <InsightsPanel
            insights={dashboard?.insights?.insights || []}
          />

        </div>

      </div>

    </div>
  );
}

export default AnalyticsDashboardPage;