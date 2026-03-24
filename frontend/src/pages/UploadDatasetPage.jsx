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

      <div className="p-8 max-w-5xl mx-auto">

        <h1 className="text-3xl font-semibold mb-8">
          Upload Dataset
        </h1>

        {/* FORM CARD */}
        <div className="bg-white border border-stone-200 rounded-xl p-6 shadow-sm mb-10">

          <form onSubmit={handleSubmit} className="space-y-4">

            <input
              type="text"
              placeholder="Dataset Name"
              className="w-full border border-stone-300 p-3 rounded-lg focus:ring-2 focus:ring-amber-500 outline-none"
              value={datasetName}
              onChange={(e) => setDatasetName(e.target.value)}
            />

            <input
              type="file"
              accept=".csv,.xlsx,.xls"
              className="w-full border border-stone-300 p-3 rounded-lg bg-white"
              onChange={(e) => setFile(e.target.files[0])}
            />

            <button
              type="submit"
              className="w-full bg-amber-600 text-white py-3 rounded-lg hover:bg-amber-700 transition"
            >
              Upload Dataset
            </button>

            {message && (
              <p className="text-sm text-stone-600">{message}</p>
            )}

          </form>

        </div>

        {/* DATASETS LIST */}
        <div>

          <h2 className="text-xl font-semibold mb-4">
            Previously Uploaded Datasets
          </h2>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">

            {datasets.map((dataset) => (

              <div
                key={dataset.id}
                className="bg-white border border-stone-200 rounded-xl p-5 shadow-sm"
              >
                <h3 className="font-semibold text-lg">
                  {dataset.name}
                </h3>

                <p className="text-sm text-gray-500 mt-2">
                  {dataset.file_type} • {dataset.rows} rows
                </p>

              </div>

            ))}

          </div>

        </div>

      </div>

    </div>

  </div>
);
}

export default UploadDatasetPage;