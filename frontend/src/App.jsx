import { BrowserRouter, Routes, Route } from "react-router-dom";

import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import DashboardHome from "./pages/DashboardHome";
import DatasetsPage from "./pages/DatasetsPage";
import UploadDatasetPage from "./pages/UploadDatasetPage";
import AnalyticsDashboardPage from "./pages/AnalyticsDashboardPage";

import ProtectedRoute from "./routes/ProtectedRoute";

function App() {
  return (
    <BrowserRouter>

      <Routes>

        <Route path="/" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardHome />
            </ProtectedRoute>
          }
        />

        <Route path="/datasets" element={<DatasetsPage />} />

        <Route path="/upload-dataset" element={<UploadDatasetPage />} />

        <Route
          path="/analytics/:dataset_id"
          element={<AnalyticsDashboardPage />}
        />


      </Routes>

    </BrowserRouter>
  );
}

export default App;