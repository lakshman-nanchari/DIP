import { useState } from "react";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import API from "../api/axios";

function UploadDatasetPage() {
  const [datasetName, setDatasetName] = useState("");
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      setMessage("Please select a dataset file");
      return;
    }

    try {
      const formData = new FormData();
      formData.append("dataset_name", datasetName);
      formData.append("file", file);

      await API.post("/datasets/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setMessage("Dataset uploaded successfully 🚀");
      setDatasetName("");
      setFile(null);

    } catch (err) {
      console.error(err);
      setMessage("Upload failed ❌");
    }
  };

  return (
    <div className="flex">

      <Sidebar />

      <div className="flex-1">

        <Navbar />

        <div className="p-8">

          <h1 className="text-2xl font-bold mb-6">
            Upload Dataset
          </h1>

          <form
            onSubmit={handleSubmit}
            className="bg-white p-6 rounded shadow w-96"
          >

            {/* Dataset Name */}
            <input
              type="text"
              placeholder="Dataset Name"
              className="w-full border p-3 rounded mb-4"
              value={datasetName}
              onChange={(e) => setDatasetName(e.target.value)}
            />

            {/* File Upload */}
            <label className="block mb-4">
              <span className="text-sm text-gray-600">
                Select Dataset File
              </span>

              <input
                type="file"
                accept=".csv,.xlsx"
                className="block w-full mt-2 border p-2 rounded bg-white"
                onChange={(e) => setFile(e.target.files[0])}
              />
            </label>

            {/* Upload Button */}
            <button
              type="submit"
              className="w-full bg-indigo-600 text-white p-3 rounded hover:bg-indigo-700"
            >
              Upload Dataset
            </button>

            {/* Message */}
            {message && (
              <p className="mt-4 text-sm text-gray-700">
                {message}
              </p>
            )}

          </form>

        </div>

      </div>

    </div>
  );
}

export default UploadDatasetPage;