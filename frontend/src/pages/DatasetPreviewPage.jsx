import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import API from "../api/axios";

function DatasetPreviewPage() {

  const { dataset_id } = useParams();
  const navigate = useNavigate();

  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(true);
  const [cleaning, setCleaning] = useState(false);
  const [cleanReport, setCleanReport] = useState(null);

  useEffect(() => {
    fetchPreview();
  }, []);

  const fetchPreview = async () => {

    try {

      const res = await API.get(`/datasets/${dataset_id}/preview`);

      setPreview(res.data);

    } catch (err) {

      console.error("Failed to load preview", err);

    } finally {

      setLoading(false);

    }

  };


  const cleanDataset = async () => {

    try {

      setCleaning(true);

      const res = await API.post(`/analytics/${dataset_id}/clean`);

      setCleanReport(res.data.cleaning_report || res.data.report);

    } catch (err) {

      console.error("Cleaning failed", err);

    } finally {

      setCleaning(false);

    }

  };


  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        Loading Dataset Preview...
      </div>
    );
  }

  if (!preview) {
    return (
      <div className="p-10">
        Failed to load dataset preview.
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
            Dataset Preview
          </h1>


          {/* DATASET SUMMARY */}

          <div className="grid grid-cols-2 gap-4 mb-8">

            <div className="bg-white shadow p-4 rounded">
              <p className="text-sm text-gray-500">Rows</p>
              <p className="text-xl font-semibold">
                {preview.rows.length}
              </p>
            </div>

            <div className="bg-white shadow p-4 rounded">
              <p className="text-sm text-gray-500">Columns</p>
              <p className="text-xl font-semibold">
                {preview.columns.length}
              </p>
            </div>

          </div>


          {/* COLUMN INFO */}

          <div className="bg-white shadow rounded p-6 mb-8">

            <h2 className="text-xl font-semibold mb-4">
              Column Information
            </h2>

            <table className="w-full border">

              <thead className="bg-gray-100">

                <tr>
                  <th className="p-2 border text-left">Column</th>
                  <th className="p-2 border text-left">Data Type</th>
                </tr>

              </thead>

              <tbody>

                {preview.columns.map(col => (

                  <tr key={col}>

                    <td className="border p-2">
                      {col}
                    </td>

                    <td className="border p-2">
                      {preview.dtypes[col]}
                    </td>

                  </tr>

                ))}

              </tbody>

            </table>

          </div>


          {/* DATA PREVIEW */}

          <div className="bg-white shadow rounded p-6">

            <h2 className="text-xl font-semibold mb-4">
              Data Preview
            </h2>

            <div className="overflow-auto max-h-100 border rounded">

              <table className="min-w-full text-sm">

                <thead className="bg-gray-100">

                  <tr>

                    {preview.columns.map(col => (
                      <th key={col} className="p-2 border text-left">
                        {col}
                      </th>
                    ))}

                  </tr>

                </thead>

                <tbody>

                  {preview.rows.slice(0, 20).map((row, index) => (

                    <tr key={index} className="border-b">

                      {preview.columns.map(col => (

                        <td key={col} className="p-2 border">
                          {String(row[col])}
                        </td>

                      ))}

                    </tr>

                  ))}

                </tbody>

              </table>

            </div>

          </div>


          {/* ACTION BUTTONS */}

          <div className="mt-8 flex gap-4">

            <button
              onClick={cleanDataset}
              className="bg-green-600 text-white px-6 py-3 rounded hover:bg-green-700"
            >
              {cleaning ? "Cleaning..." : "Clean Dataset"}
            </button>

            <button
              onClick={() => navigate(`/analytics/${dataset_id}`)}
              className="bg-indigo-600 text-white px-6 py-3 rounded hover:bg-indigo-700"
            >
              Analyze Dataset
            </button>

          </div>


          {/* CLEANING REPORT */}

          {cleanReport && (

            <div className="mt-6 bg-white shadow rounded p-6">

              <h2 className="text-lg font-semibold mb-3">
                Cleaning Report
              </h2>

              <ul className="space-y-2">

                <li>
                  Duplicates Removed: {cleanReport.duplicates_removed}
                </li>

                <li>
                  Missing Values Filled: {cleanReport.missing_values_filled}
                </li>

                <li>
                  Cleaned Rows: {cleanReport.cleaned_rows}
                </li>

              </ul>

            </div>

          )}

        </div>

      </div>

    </div>
  );
}

export default DatasetPreviewPage;