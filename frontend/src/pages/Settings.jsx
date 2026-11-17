
import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import {
  User,
  Mail,
  ShieldCheck,
  LogOut,
  LockKeyhole,
  CircleUserRound,
} from "lucide-react";

import { AuthContext } from "../context/AuthContext";

function Settings() {
  const { user, isAuthenticated, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  const displayName =
    user?.full_name ||
    user?.name ||
    user?.username ||
    user?.email?.split("@")[0] ||
    "User";

  return (
    <div className="settings-page">
      <div className="settings-header">
        <div>
          <span className="settings-eyebrow">ACCOUNT MANAGEMENT</span>
          <h1>Settings</h1>
          <p>Manage your account and security preferences.</p>
        </div>

        <div className="settings-header-icon">
          <LockKeyhole size={27} />
        </div>
      </div>

      {/* Profile */}
      <section className="settings-card">
        <div className="settings-card-heading">
          <CircleUserRound size={21} />
          <div>
            <h2>Profile Information</h2>
            <p>Your account details</p>
          </div>
        </div>

        <div className="settings-profile">
          <div className="settings-avatar">
            <User size={32} />
          </div>

          <div>
            <h3>{displayName}</h3>
            <p>{user?.email || "Email not available"}</p>
          </div>
        </div>

        <div className="settings-info-grid">
          <div className="settings-info-item">
            <span>Full Name / Username</span>
            <strong>{displayName}</strong>
          </div>

          <div className="settings-info-item">
            <span>Email Address</span>
            <strong>{user?.email || "Not available"}</strong>
          </div>

          <div className="settings-info-item">
            <span>User ID</span>
            <strong>{user?.id ?? "Not available"}</strong>
          </div>

          <div className="settings-info-item">
            <span>Account Status</span>
            <strong className={isAuthenticated ? "settings-active" : ""}>
              {isAuthenticated ? "Authenticated" : "Not authenticated"}
            </strong>
          </div>
        </div>
      </section>

      {/* Security */}
      <section className="settings-card">
        <div className="settings-card-heading">
          <ShieldCheck size={21} />
          <div>
            <h2>Security</h2>
            <p>Authentication and account security</p>
          </div>
        </div>

        <div className="settings-security-row">
          <div className="settings-security-icon">
            <LockKeyhole size={20} />
          </div>

          <div>
            <h3>JWT Authentication</h3>
            <p>Your account is protected using token-based authentication.</p>
          </div>

          <span className="settings-active">Active</span>
        </div>

        <div className="settings-security-row">
          <div className="settings-security-icon">
            <Mail size={20} />
          </div>

          <div>
            <h3>Email Account</h3>
            <p>{user?.email || "Email not available"}</p>
          </div>
        </div>
      </section>

      {/* Application */}
      <section className="settings-card">
        <div className="settings-card-heading">
          <CircleUserRound size={21} />
          <div>
            <h2>Application Information</h2>
            <p>About FinSight AI</p>
          </div>
        </div>

        <div className="settings-info-grid">
          <div className="settings-info-item">
            <span>Application</span>
            <strong>FinSight AI</strong>
          </div>

          <div className="settings-info-item">
            <span>Platform</span>
            <strong>Stock Analytics & Prediction</strong>
          </div>

          <div className="settings-info-item">
            <span>Frontend</span>
            <strong>React.js</strong>
          </div>

          <div className="settings-info-item">
            <span>Backend</span>
            <strong>FastAPI</strong>
          </div>
        </div>
      </section>

      {/* Logout */}
      <section className="settings-logout-card">
        <div>
          <h3>Sign Out</h3>
          <p>Logout from your FinSight AI account.</p>
        </div>

        <button onClick={handleLogout}>
          <LogOut size={17} />
          Logout
        </button>
      </section>
    </div>
  );
}

export default Settings;
