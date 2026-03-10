import { NavLink, useNavigate } from "react-router-dom";
import {
  FiHome,
  FiDatabase,
  FiUpload,
  FiLogOut
} from "react-icons/fi";

function Sidebar() {

  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <div className="w-64 bg-stone-800 text-stone-200 backdrop-blur-xl border-r border-stone-800 min-h-screen flex flex-col">

      {/* Logo */}
      <div className="p-6 border-b border-gray-800">
        <h2 className="text-xl font-bold tracking-wide">
          Data Intelligence
        </h2>
      </div>

      {/* Navigation */}
      <nav className="flex flex-col gap-2 p-4 flex-1">

        <NavLink
          to="/dashboard"
          className={({ isActive }) =>
            `flex items-center gap-3 p-3 rounded transition ${
              isActive
                ? "bg-violet-600/20"
                : "hover:bg-slate-800"
            }`
          }
        >
          <FiHome size={18} />
          Dashboard
        </NavLink>

        <NavLink
          to="/datasets"
          className={({ isActive }) =>
            `flex items-center gap-3 p-3 rounded transition ${
              isActive
                ? "bg-violet-600/20"
                : "hover:bg-slate-800"
            }`
          }
        >
          <FiDatabase size={18} />
          Datasets
        </NavLink>

        <NavLink
          to="/upload-dataset"
          className={({ isActive }) =>
            `flex items-center gap-3 p-3 rounded transition ${
              isActive
                ? "bg-indigo-600/20"
                : "hover:bg-slate-800"
            }`
          }
        >
          <FiUpload size={18} />
          Upload Dataset
        </NavLink>

      </nav>

      {/* Logout */}
      <div className="p-4 border-t border-gray-800">

        <button
          onClick={handleLogout}
          className="flex items-center gap-3 w-full p-3 rounded hover:bg-red-600 transition"
        >
          <FiLogOut size={18} />
          Logout
        </button>

      </div>

    </div>
  );
}

export default Sidebar;