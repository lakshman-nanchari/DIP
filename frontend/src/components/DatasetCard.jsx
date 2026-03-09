import { useNavigate } from "react-router-dom";

function DatasetCard({ dataset }) {

  const navigate = useNavigate();

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

    </div>
  );
}

export default DatasetCard;