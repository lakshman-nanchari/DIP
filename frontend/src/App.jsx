import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import DashboardHome from "./pages/DashboardHome";
import DatasetsPage from "./pages/DatasetsPage";
import UploadDatasetPage from "./pages/UploadDatasetPage";
import AnalyticsDashboardPage from "./pages/AnalyticsDashboardPage"; 
import DatasetPreviewPage from "./pages/DatasetPreviewPage";
import ProtectedRoute from "./routes/ProtectedRoute";
import DatasetProfilePage from "./pages/DatasetProfilePage"

function App() {
  return (
    <BrowserRouter>

      <Routes>

        {/* PUBLIC */}
        <Route path="/" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />

        {/* 🔥 ALL PROTECTED ROUTES */}
        <Route element={<ProtectedRoute />}>

          <Route path="/dashboard" element={<DashboardHome />} />

          <Route path="/datasets" element={<DatasetsPage />} />

          <Route path="/upload-dataset" element={<UploadDatasetPage />} />

          <Route
            path="/analytics/:dataset_id"
            element={<AnalyticsDashboardPage />}
          />

          <Route
            path="/datasets/:dataset_id/preview"
            element={<DatasetPreviewPage />}
          />

          <Route
            path="/analytics/:dataset_id/profile"
            element={<DatasetProfilePage />}
          />

        </Route>

        {/* fallback */}
        <Route path="*" element={<Navigate to="/" />} />

      </Routes>

    </BrowserRouter>
  );
}

export default App;