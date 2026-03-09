import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import DatasetCard from "../components/DatasetCard";
import API from "../api/axios";

function DatasetsPage() {

  const [datasets, setDatasets] = useState([]);

  useEffect(() => {
    fetchDatasets();
  }, []);

  const fetchDatasets = async () => {
    try {

      const res = await API.get("/datasets");

      setDatasets(res.data);

    } catch (err) {
      console.error("Failed to fetch datasets", err);
    }
  };

  return (
    <div className="flex">

      <Sidebar />

      <div className="flex-1">

        <Navbar />

        <div className="p-8">

          <h1 className="text-2xl font-bold mb-6">
            Datasets
          </h1>

          {datasets.length === 0 ? (
            <p>No datasets uploaded yet.</p>
          ) : (

            <div className="grid grid-cols-3 gap-6">

              {datasets.map((dataset) => (
                <DatasetCard
                  key={dataset.id}
                  dataset={dataset}
                />
              ))}

            </div>

          )}

        </div>

      </div>

    </div>
  );
}

export default DatasetsPage;