
import { Outlet } from "react-router-dom";
import {
  LayoutDashboard,
  TrendingUp,
  BriefcaseBusiness,
  BrainCircuit,
  Settings,
  LogOut,
} from "lucide-react";

import Navbar from "../components/Navbar";

const menuItems = [
  { name: "Overview", icon: LayoutDashboard, path: "/" },
  { name: "Stock Market", icon: TrendingUp, path: "/stocks" },
  { name: "Portfolio", icon: BriefcaseBusiness, path: "/portfolio" },
  { name: "AI Predictions", icon: BrainCircuit, path: "/predictions" },
  { name: "Settings", icon: Settings, path: "/settings" },
];

function DashboardLayout() {
  return (
    <div className="dashboard-layout">
      <aside className="sidebar">
        <h2 className="logo">FinSight AI</h2>

        <p className="menu-label">MENU</p>

        <nav className="sidebar-menu">
          {menuItems.map((item) => {
            const Icon = item.icon;

            return (
              <a href={item.path} className="menu-item" key={item.name}>
                <Icon size={19} />
                <span>{item.name}</span>
              </a>
            );
          })}
        </nav>
      </aside>

      <div className="dashboard-main">
        <Navbar />

        <main className="dashboard-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

export default DashboardLayout;
