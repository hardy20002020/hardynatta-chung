import { Link } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";


export default function Sidebar() {
  const { user } = useAuth();


  return (
    <aside>
      <h2>MAJE</h2>

      <nav>
        <ul>
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
