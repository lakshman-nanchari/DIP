import { Link, useLocation } from "react-router-dom";

const routeNameMap = {
  dashboard: "Dashboard",
  datasets: "Datasets",
  "upload-dataset": "Upload",
  analytics: "Analytics",
  preview: "Preview",
  profile: "Profile"
};

function Breadcrumbs() {
  const location = useLocation();

  const pathnames = location.pathname.split("/").filter(Boolean);

  return (
    <div className="mb-6 text-sm text-stone-500 flex flex-wrap items-center gap-2">

      <Link to="/dashboard" className="hover:text-stone-800">
        Dashboard
      </Link>

      {pathnames.map((value, index) => {
        const to = "/" + pathnames.slice(0, index + 1).join("/");
        const isLast = index === pathnames.length - 1;

        // ignore dynamic ids
        if (!isNaN(value)) return null;

        return (
          <span key={to} className="flex items-center gap-2">

            <span>›</span>

            {isLast ? (
              <span className="text-stone-800 font-medium">
                {routeNameMap[value] || value}
              </span>
            ) : (
              <Link to={to} className="hover:text-stone-800">
                {routeNameMap[value] || value}
              </Link>
            )}

          </span>
        );
      })}

    </div>
  );
}

export default Breadcrumbs;