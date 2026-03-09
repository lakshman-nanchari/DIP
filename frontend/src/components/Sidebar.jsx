import { Link } from "react-router-dom";

function Sidebar() {
  return (
    <div className="w-64 bg-gray-900 text-white min-h-screen p-6">

      <h2 className="text-xl font-bold mb-8">
        Data Intelligence
      </h2>

      <nav className="flex flex-col gap-4">

        <Link to="/dashboard">Dashboard</Link>

        <Link to="/datasets">Datasets</Link>

        <Link to="/upload-dataset">Upload Dataset</Link>

        <Link to="/analytics">Analytics</Link>

        <Link to="/">Logout</Link>

      </nav>

    </div>
  );
}

export default Sidebar;