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

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        Loading Dataset Preview...
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


          {/* COLUMN INFO */}

          <div className="bg-white shadow rounded p-6 mb-8">

            <h2 className="text-xl font-semibold mb-4">
              Columns
            </h2>

            <table className="w-full border">

              <thead className="bg-gray-100">
                <tr>
                  <th className="p-2 border">Column</th>
                  <th className="p-2 border">Data Type</th>
                </tr>
              </thead>

              <tbody>

                {preview.columns.map(col => (

                  <tr key={col}>

                    <td className="border p-2">{col}</td>

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
              First {preview.rows.length} Rows
            </h2>

            <div className="overflow-auto">

              <table className="w-full border">

                <thead className="bg-gray-100">

                  <tr>

                    {preview.columns.map(col => (
                      <th key={col} className="p-2 border">
                        {col}
                      </th>
                    ))}

                  </tr>

                </thead>

                <tbody>

                  {preview.rows.map((row, index) => (

                    <tr key={index}>

                      {preview.columns.map(col => (

                        <td key={col} className="border p-2">
                          {String(row[col])}
                        </td>

                      ))}

                    </tr>

                  ))}

                </tbody>

              </table>

            </div>

          </div>


          {/* ANALYZE BUTTON */}

          <div className="mt-8">

            <button
              onClick={() => navigate(`/analytics/${dataset_id}`)}
              className="bg-indigo-600 text-white px-6 py-3 rounded hover:bg-indigo-700"
            >
              Analyze Dataset
            </button>

          </div>

        </div>

      </div>

    </div>
  );
}

export default DatasetPreviewPage;