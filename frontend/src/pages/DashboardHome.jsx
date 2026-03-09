import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import KpiCard from "../components/KpiCard";

function DashboardHome() {
  return (
    <div className="flex">

      <Sidebar />

      <div className="flex-1">

        <Navbar />

        <div className="p-8">

          <h1 className="text-2xl font-bold mb-6">
            Dashboard
          </h1>

          <div className="grid grid-cols-4 gap-6">

            <KpiCard title="Total Revenue" value="$120K" />

            <KpiCard title="Total Orders" value="3,200" />

            <KpiCard title="Customers" value="1,050" />

            <KpiCard title="Growth" value="18%" />

          </div>

        </div>

      </div>

    </div>
  );
}

export default DashboardHome;