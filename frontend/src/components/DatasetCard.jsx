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
    <div className="bg-white border border-stone-200 rounded-xl p-5 shadow-sm hover:shadow-md transition">

      <h3 className="text-lg font-semibold">
        {dataset.name}
      </h3>

      <p className="text-sm text-gray-500 mt-2">
        {dataset.file_type} • {dataset.rows} rows
      </p>

      <p className="text-sm text-gray-400 mt-2">
        Uploaded: {new Date(dataset.created_at).toLocaleString()}
      </p>
      <div className="flex flex-col gap-3 mt-4">

        <button
          onClick={() => navigate(`/datasets/${dataset.id}/preview`)}
          className="bg-amber-600 text-white py-2 rounded-lg hover:bg-amber-700 transition"
        >
          Preview Dataset
        </button>

        <button
          onClick={() => navigate(`/analytics/${dataset.id}`)}
          className="bg-stone-800 text-white py-2 rounded-lg hover:bg-stone-900 transition"
        >
          Analyze Dataset
        </button>

        <button
          onClick={deleteDataset}
          className="border border-red-400 text-red-600 py-2 rounded-lg hover:bg-red-50 transition"
        >
          Delete Dataset
        </button>

      </div>

    </div>
  );
}

export default DatasetCard;