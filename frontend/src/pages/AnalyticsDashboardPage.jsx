import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import KpiCard from "../components/KpiCard";
import InsightsPanel from "../components/InsightsPanel";
import ChartComponent from "../components/ChartComponent";
import AnomalyTable from "../components/AnomalyTable";

import API from "../api/axios";

function AnalyticsDashboardPage() {

  const { dataset_id } = useParams();
  const [datasetName, setDatasetName] = useState("");
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

      setDashboard(res.data.dashboard);
      setDatasetName(res.data.dataset_name);

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

          <div className="mb-6">

            <h1 className="text-2xl font-bold">
            Analytics Dashboard
            </h1>

            <p className="text-gray-500">
            Dataset: {datasetName}
            </p>

            </div>

            {/* KPI SECTION */}

            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-8">

            {Object.entries(dashboard?.kpis || {}).map(([key, value]) => (

            <KpiCard
              key={key}
              title={key.replaceAll("_", " ")}
              value={value}
            />

            ))}

            </div>

          {/* INSIGHTS */}

          <InsightsPanel
            insights={dashboard?.insights}
          />

        {/* HISTOGRAM CHARTS */}

        <h2 className="text-xl font-semibold mt-10 mb-4">
          Charts
        </h2>

        <div className="grid grid-cols-2 gap-6">

          {Object.entries(dashboard?.charts?.histograms || {}).map(([column, data]) => (

            <ChartComponent
              key={column}
              title={`Histogram: ${column}`}
              type="bar"
              data={data.values.slice(0,500).map((v,i)=>({
                index:i,
                value:v
              }))}
            />

          ))}

        </div>  


        {/* CATEGORY DISTRIBUTION */}

          <h2 className="text-xl font-semibold mt-10 mb-4">
          Category Distribution
          </h2>

          <div className="grid grid-cols-2 gap-6">

          {Object.entries(dashboard?.charts?.bars || {}).map(([column, data]) => (

            <ChartComponent
              key={column}
              title={`Category: ${column}`}
              data={data.labels.map((label,i)=>({
                index: label,
                value: data.values[i]
              }))}
            />

          ))}

          </div>

          {/* TREND */}

          <h2 className="text-xl font-semibold mt-10 mb-4">
            Trend
          </h2>

          <ChartComponent
            type="line"
            title={`Trend: ${dashboard?.charts?.trend?.column}`}
            data={dashboard?.charts?.trend?.values
              ?.slice(0,500)
              .map((v,i)=>({
                index:i,
                value:v
              }))}
          />


            {/* FORECAST */}

            <h2 className="text-xl font-semibold mt-10 mb-4">
              Forecast
            </h2>

            <ChartComponent
              type="line"
              title="Forecast"
              data={dashboard?.forecast?.forecast?.map(item => ({
                index: item.step,
                value: item.predicted_value
              }))}
            />


          {/* ANOMALY DETECTION */}

          <h2 className="text-xl font-semibold mt-10 mb-4">
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