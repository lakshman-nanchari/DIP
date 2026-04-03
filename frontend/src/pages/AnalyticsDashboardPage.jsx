import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import KpiCard from "../components/KpiCard";
import InsightsPanel from "../components/InsightsPanel";
import ChartComponent from "../components/ChartComponent";
import AnomalyTable from "../components/AnomalyTable";
import Loader from "../components/Loader";
import Breadcrumbs from "../components/Breadcrumbs";
import API from "../api/axios";

function AnalyticsDashboardPage() {

  const { dataset_id } = useParams();
  const navigate = useNavigate();

  const [datasetName, setDatasetName] = useState("");
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {

    if (!dataset_id) return;

    fetchDashboard();

  }, [dataset_id]);

  const fetchDashboard = async () => {

    try {

      const res = await API.get(`/analytics/${dataset_id}/dashboard`);

      setDashboard(res.data.dashboard);
      setDatasetName(res.data.dataset_name);

    } catch (err) {

      console.error("Failed to load dashboard", err);

    } finally {

      setLoading(false);

    }

  };

  if (loading) {
    return <Loader />;
  }

  if (!dashboard) {
    return <div className="p-8">No dashboard data available</div>;
  }

  return (

    <div className="flex min-h-screen text-stone-800 bg-linear-to-br
  from-stone-100
  via-stone-50
  to-stone-200">

      <Sidebar />

      <div className="flex-1">

        <Navbar />

        <div className="p-8 max-w-7xl mx-auto">

          <Breadcrumbs />

          {/* HEADER */}

          <div className="mb-8">

            <h1 className="text-3xl font-semibold">
              Analytics Dashboard
            </h1>

            <p className="text-sm text-stone-500 mt-2">
              Dataset:
              <span className="ml-2 bg-stone-200 px-2 py-1 rounded text-xs">
                {datasetName}
              </span>
            </p>

          </div>


          {/* KPI SECTION */}

          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mb-10">

            {Object.entries(dashboard?.kpis || {}).map(([key, value]) => (

              <KpiCard
                key={key}
                title={key.replaceAll("_", " ")}
                value={value}
              />

            ))}

          </div>


          {/* INSIGHTS */}

          <InsightsPanel insights={dashboard?.insights} />


          {/* DISTRIBUTION CHARTS */}

          <h2 className="text-xl font-semibold mt-12 mb-4">
            Distribution
          </h2>

          <div className="grid md:grid-cols-2 gap-6">

            {Object.entries(dashboard?.charts?.histograms || {}).map(([column, data]) => {

              const values = data?.values || [];

              return (
                <ChartComponent
                  key={column}
                  title={`Histogram: ${column}`}
                  type="bar"
                  data={values.slice(0, 500).map((v, i) => ({
                    index: i,
                    value: v
                  }))}
                />
              );
            })}

          </div>


          {/* CATEGORY DISTRIBUTION */}

          <h2 className="text-xl font-semibold mt-12 mb-4">
            Category Distribution
          </h2>

          <div className="grid md:grid-cols-2 gap-6">

            {Object.entries(dashboard?.charts?.bars || {}).map(([column, data]) => {

              const labels = data?.labels || [];
              const values = data?.values || [];

              return (
                <ChartComponent
                  key={column}
                  title={`Category: ${column}`}
                  data={labels.map((label, i) => ({
                    index: label,
                    value: values[i] ?? 0
                  }))}
                />
              );
            })}

          </div>


          {/* TREND */}

          <h2 className="text-xl font-semibold mt-12 mb-4">
            Trend Analysis
          </h2>

          {(() => {
            const trendValues = dashboard?.charts?.trend?.values || [];

            return (
              <ChartComponent
                type="line"
                title={`Trend: ${dashboard?.charts?.trend?.column}`}
                data={trendValues.slice(0, 200).map((v, i) => ({
                  index: i,
                  value: v
                }))}
              />
            );
          })()}


          {/* FORECAST */}

          <h2 className="text-xl font-semibold mt-12 mb-4">
            Forecast
          </h2>

          {(() => {
            const forecastData = dashboard?.forecast?.forecast || [];

            return (
              <ChartComponent
                type="line"
                title="Forecast"
                data={forecastData.map(item => ({
                  index: item.step,
                  value: item.predicted_value
                }))}
              />
            );
          })()}


          {/* ANOMALY DETECTION */}

          <h2 className="text-xl font-semibold mt-12 mb-4">
            Anomaly Detection
          </h2>

          <AnomalyTable
            anomalies={dashboard?.anomalies?.anomalies || []}
          />

        </div>

      </div>

    </div>

  );
}

export default AnalyticsDashboardPage;