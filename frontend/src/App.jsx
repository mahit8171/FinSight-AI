
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import ProtectedRoute from "./components/ProtectedRoute";
import DashboardLayout from "./layouts/DashboardLayout";
import StockMarket from "./pages/StockMarket";
import StockDetails from "./pages/StockDetails";
import Portfolio from "./pages/Portfolio";
import AIPredictions from "./pages/AIPredictions";
import Settings from "./pages/Settings";
import Register from "./pages/Register";

import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route element={<ProtectedRoute />}>
          <Route element={<DashboardLayout />}>
            <Route path="/" element={<Dashboard />} />
            <Route path="/stocks" element={<StockMarket />} />
            <Route path="/stocks/:symbol" element={<StockDetails />} />
            <Route path="/portfolio" element={<Portfolio />} />
            <Route path="/predictions" element={<AIPredictions />} />
            <Route path="/settings" element={<Settings />} />
          </Route>
        </Route>

        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
