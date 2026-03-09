import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

function DashboardHome() {
  return (
    <div className="flex">

      <Sidebar />

      <div className="flex-1">

        <Navbar />

        <div className="p-8">
          <h1 className="text-2xl font-bold">
            Dashboard Connected Successfully 🚀
          </h1>
        </div>

      </div>

    </div>
  );
}

export default DashboardHome;