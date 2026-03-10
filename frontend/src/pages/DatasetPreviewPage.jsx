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
      <div className="flex items-center justify-center h-screen text-stone-600">
        Loading Dataset Preview...
      </div>
    );
  }

  if (!preview) {
    return (
      <div className="p-10 text-stone-600">
        Failed to load dataset preview.
      </div>
    );
  }


  return (
    <div className="flex bg-stone-100 min-h-screen text-stone-800">

      <Sidebar />

      <div className="flex-1">

        <Navbar />

        <div className="p-8">

          <h1 className="text-3xl font-semibold mb-8">
            Dataset Preview
          </h1>


          {/* DATASET SUMMARY */}

          <div className="grid grid-cols-2 gap-6 mb-10">

            <div className="bg-white border border-stone-200 p-6 rounded-xl">
              <p className="text-sm text-stone-500">Rows</p>
              <p className="text-2xl font-semibold">
                {preview.rows.length}
              </p>
            </div>

            <div className="bg-white border border-stone-200 p-6 rounded-xl">
              <p className="text-sm text-stone-500">Columns</p>
              <p className="text-2xl font-semibold">
                {preview.columns.length}
              </p>
            </div>

          </div>


          {/* COLUMN INFO */}

          <div className="bg-white border border-stone-200 rounded-xl p-6 mb-10">

            <h2 className="text-xl font-semibold mb-6">
              Column Information
            </h2>

            <table className="w-full text-sm">

              <thead className="bg-stone-50">

                <tr>
                  <th className="p-3 text-left border-b">Column</th>
                  <th className="p-3 text-left border-b">Data Type</th>
                </tr>

              </thead>

              <tbody>

                {preview.columns.map(col => (

                  <tr key={col} className="border-b">

                    <td className="p-3">
                      {col}
                    </td>

                    <td className="p-3 text-stone-600">
                      {preview.dtypes[col]}
                    </td>

                  </tr>

                ))}

              </tbody>

            </table>

          </div>


          {/* DATA PREVIEW */}

          <div className="bg-white border border-stone-200 rounded-xl p-6">

            <h2 className="text-xl font-semibold mb-6">
              Data Preview
            </h2>

            <div className="overflow-auto max-h-96 border border-stone-200 rounded-lg">

              <table className="min-w-full text-sm">

                <thead className="bg-stone-50">

                  <tr>

                    {preview.columns.map(col => (
                      <th key={col} className="p-3 border-b text-left">
                        {col}
                      </th>
                    ))}

                  </tr>

                </thead>

                <tbody>

                  {preview.rows.slice(0, 20).map((row, index) => (

                    <tr key={index} className="border-b">

                      {preview.columns.map(col => (

                        <td key={col} className="p-3 text-stone-700">
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

          <div className="mt-10 flex gap-4">

            <button
              onClick={cleanDataset}
              className="bg-amber-600 text-white px-6 py-3 rounded-lg hover:bg-amber-700 transition"
            >
              {cleaning ? "Cleaning..." : "Clean Dataset"}
            </button>

            <button
              onClick={() => navigate(`/analytics/${dataset_id}`)}
              className="bg-stone-800 text-white px-6 py-3 rounded-lg hover:bg-stone-900 transition"
            >
              Analyze Dataset
            </button> 

            <button
              onClick={() => navigate(`/analytics/${dataset_id}/profile`)}
              className="border border-stone-300 px-6 py-3 rounded-lg hover:bg-stone-50 transition"
            >
              View Profile
            </button>

          </div>


          {/* CLEANING REPORT */}

          {cleanReport && (

            <div className="mt-10 bg-white border border-stone-200 rounded-xl p-6">

              <h2 className="text-lg font-semibold mb-4">
                Cleaning Report
              </h2>

              <ul className="space-y-2 text-stone-700">

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