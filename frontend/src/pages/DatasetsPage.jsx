import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import DatasetCard from "../components/DatasetCard";
import Breadcrumbs from "../components/Breadcrumbs";
import API from "../api/axios";

function DatasetsPage() {

  const [datasets, setDatasets] = useState([]);

  useEffect(() => {

    fetchDatasets();

  }, []);

  const fetchDatasets = async () => {

    try {

      const res = await API.get("/datasets");

      setDatasets(res.data || []);

    } catch (err) {

      console.error("Failed to fetch datasets", err);

      setDatasets([]);

    }

  };

  return (
    <div className="flex min-h-screen text-stone-800 bg-linear-to-br
      from-stone-100
      via-stone-50
      to-stone-200">

      <Sidebar />

      <div className="flex-1">

        <Navbar />

        <div className="p-8 max-w-7xl mx-auto">

          <Breadcrumbs />

          <h1 className="text-3xl font-semibold mb-6">
            Datasets
          </h1>

          {datasets.length === 0 ? (

            <div className="bg-white border border-stone-200 rounded-xl p-6 text-center text-stone-500">
              No datasets uploaded yet.
            </div>

          ) : (

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">

              {datasets.map((dataset) => (

                <DatasetCard
                  key={dataset.id}
                  dataset={dataset}
                  refreshDatasets={fetchDatasets}   
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