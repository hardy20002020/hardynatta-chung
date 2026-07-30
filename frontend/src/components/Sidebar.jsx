import { Link } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

export default function Sidebar() {
  const { user } = useAuth();

  return (
    <aside className="sidebar">
      <h2 className="sidebar-title">MAJE</h2>

      <nav>
        <ul className="sidebar-menu">
          <li>
            <Link to="/dashboard">
              Dashboard
            </Link>
          </li>

          {user?.role === "admin" && (
            <li>
              <Link to="/users">
                User Management
              </Link>
            </li>
          )}

          <li>
            <Link to="/profile">
              Profile
            </Link>
          </li>
        </ul>
      </nav>
    </aside>
  );
}