import { useNavigate } from "react-router-dom";
import API from "../api/axios";

function DatasetCard({ dataset, refreshDatasets }) {

  const navigate = useNavigate();

  const deleteDataset = async () => {

    const confirmDelete = window.confirm(
      "Are you sure you want to delete this dataset?"
    );

    if (!confirmDelete) return;

    try {

      await API.delete(`/datasets/${dataset.id}`);

      refreshDatasets(); // refresh dataset list

    } catch (err) {

      console.error("Failed to delete dataset", err);

    }

  };

  return (
    <div className="bg-white shadow rounded p-4 hover:shadow-lg transition">

      <h3 className="text-lg font-semibold">
        {dataset.name}
      </h3>

      <p className="text-sm text-gray-500 mt-2">
        {dataset.file_type} • {dataset.rows} rows
      </p>

      <p className="text-sm text-gray-400 mt-2">
        Uploaded: {new Date(dataset.created_at).toLocaleString()}
      </p>

      <button
        onClick={() => navigate(`/datasets/${dataset.id}/preview`)}
        className="mt-4 w-full bg-indigo-600 text-white p-2 rounded hover:bg-indigo-700"
      >
        Preview Dataset
      </button>

      <button
        onClick={() => navigate(`/analytics/${dataset.id}`)}
        className="mt-2 w-full bg-green-600 text-white p-2 rounded hover:bg-green-700"
      >
        Analyze Dataset
      </button>

      <button
        onClick={deleteDataset}
        className="mt-2 w-full bg-red-600 text-white p-2 rounded hover:bg-red-700"
      >
        Delete Dataset
      </button>

    </div>
  );
}

export default DatasetCard;