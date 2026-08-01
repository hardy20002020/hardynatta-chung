import { useEffect, useState } from "react";

import { useAuth } from "../auth/AuthContext";
import dashboardService from "../api/dashboardService";

export default function Dashboard() {
  const { user } = useAuth();

  const [stats, setStats] = useState({
    total_users: 0,
    total_provinces: 0,
    total_cities: 0,
  });

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, []);

  async function loadDashboard() {
    try {
      const data = await dashboardService.getDashboard();
      setStats(data);
    } catch (error) {
      console.error("Dashboard Error:", error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h1>MAJE Dashboard</h1>

      {user && (
        <div className="card">
          <h2>Welcome back 👋</h2>

          <p>
            <strong>{user.name}</strong>
          </p>

          <p>{user.email}</p>

          <p>
            <strong>Role:</strong> {user.role}
          </p>
        </div>
      )}

      <h2 className="mt-3">
        Dashboard Statistics
      </h2>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <div className="dashboard-grid">

          <div className="stat-card">
            <div className="stat-icon">
              👥
            </div>

            <div className="stat-title">
              Total Users
            </div>

            <div className="stat-value">
              {stats.total_users}
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">
              🗺️
            </div>

            <div className="stat-title">
              Total Provinces
            </div>

            <div className="stat-value">
              {stats.total_provinces}
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">
              🏙️
            </div>

            <div className="stat-title">
              Total Cities
            </div>

            <div className="stat-value">
              {stats.total_cities}
            </div>
          </div>

        </div>
      )}
    </div>
  );
}