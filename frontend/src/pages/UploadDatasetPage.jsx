import { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import API from "../api/axios";

function UploadDatasetPage() {

  const [datasetName, setDatasetName] = useState("");
  const [file, setFile] = useState(null);
  const [datasets, setDatasets] = useState([]);
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetchDatasets();
  }, []);

  const fetchDatasets = async () => {
    try {
      const res = await API.get("/datasets");
      setDatasets(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      setMessage("Please select a file");
      return;
    }

    try {

      const formData = new FormData();
      formData.append("dataset_name", datasetName);
      formData.append("file", file);

      await API.post("/datasets/upload", formData);

      setMessage("Dataset uploaded successfully 🚀");

      setDatasetName("");
      setFile(null);

      // Reset file input element
      const fileInput = document.querySelector('input[type="file"]');
      if (fileInput) {
        fileInput.value = "";
      }

      fetchDatasets();

    } catch (err) {
      console.error(err);
      setMessage("Upload failed");
    }
  };

  return (
    <div className="flex bg-stone-100 min-h-screen text-stone-800">

      <Sidebar />

      <div className="flex-1">

        <Navbar />

        <div className="p-8">

          <h1 className="text-2xl font-bold mb-6">
            Upload Dataset
          </h1>

          <form
            onSubmit={handleSubmit}
            className="bg-white p-6 rounded shadow w-96 mb-10"
          >

            <input
              type="text"
              placeholder="Dataset Name"
              className="w-full border p-3 rounded mb-4"
              value={datasetName}
              onChange={(e) => setDatasetName(e.target.value)}
            />

            <label className="block mb-4">
              <span className="text-sm text-gray-600">
                Select Dataset File
              </span>

              <input
                type="file"
                accept=".csv,.xlsx,.xls"
                className="block w-full mt-2 border p-2 rounded bg-white"
                onChange={(e) => setFile(e.target.files[0])}
              />
            </label>

            <button
              type="submit"
              className="w-full bg-indigo-600 text-white p-3 rounded hover:bg-indigo-700"
            >
              Upload Dataset
            </button>

            {message && (
              <p className="mt-4 text-sm">{message}</p>
            )}

          </form>

          {/* Previous Datasets */}

          <h2 className="text-xl font-semibold mb-4">
            Previously Uploaded Datasets
          </h2>

          <div className="grid grid-cols-3 gap-4">

            {datasets.map((dataset) => (

              <div
                key={dataset.id}
                className="bg-white shadow p-4 rounded"
              >

                <h3 className="font-semibold">
                  {dataset.name}
                </h3>

                <p className="text-sm text-gray-500">
                  {dataset.file_type} • {dataset.rows} rows
                </p>

              </div>

            ))}

          </div>

        </div>

      </div>

    </div>
  );
}

export default UploadDatasetPage;