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


          {/* ==================================================
              DASHBOARD
          ================================================== */}

          {hasPermission(
            user,
            "dashboard.read"
          ) && (

            <li>

              <NavLink to="/dashboard">

                📊 Dashboard

              </NavLink>

            </li>

          )}




          {/* ==================================================
              USER MANAGEMENT
          ================================================== */}

          {hasPermission(
            user,
            "user.read"
          ) && (

            <li>

              <NavLink to="/users">

                👥 User Management

              </NavLink>

            </li>

          )}




          {/* ==================================================
              ROLE MANAGEMENT
          ================================================== */}

          {hasPermission(
            user,
            "role.read"
          ) && (

            <li>

              <NavLink to="/roles">

                🛡 Role Management

              </NavLink>

            </li>

          )}




          {/* ==================================================
              PERMISSION MANAGEMENT
          ================================================== */}

          {hasPermission(
            user,
            "permission.read"
          ) && (

            <li>

              <NavLink to="/permissions">

                🔑 Permission Management

              </NavLink>

            </li>

          )}




          {/* ==================================================
              AUDIT LOGS
          ================================================== */}

          {hasPermission(
            user,
            "audit.read"
          ) && (

            <li>

              <NavLink to="/audit-logs">

                📋 Audit Logs

              </NavLink>

            </li>

          )}




          {/* ==================================================
              PROFILE
          ================================================== */}

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