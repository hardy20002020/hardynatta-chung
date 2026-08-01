import { NavLink } from "react-router-dom";

import { useAuth } from "../auth/AuthContext";
import { hasPermission } from "../auth/permissionHelper";

export default function Sidebar() {
  const { user } = useAuth();

  return (
    <aside className="sidebar">
      <h2 className="sidebar-title">
        MAJE
      </h2>

      <nav>
        <ul className="sidebar-menu">

          <li>
            <NavLink to="/dashboard">
              📊 Dashboard
            </NavLink>
          </li>

          {hasPermission(user, "user.read") && (
            <li>
              <NavLink to="/users">
                👥 User Management
              </NavLink>
            </li>
          )}

          {hasPermission(user, "role.read") && (
            <li>
              <NavLink to="/roles">
                🛡 Role Management
              </NavLink>
            </li>
          )}

          {hasPermission(user, "permission.read") && (
            <li>
              <NavLink to="/permissions">
                🔑 Permission Management
              </NavLink>
            </li>
          )}

          <li>
            <NavLink to="/profile">
              👤 Profile
            </NavLink>
          </li>

        </ul>
      </nav>
    </aside>
  );
}