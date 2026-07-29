import { useAuth } from "../auth/AuthContext";


export default function Dashboard() {
  const { user, logout } = useAuth();


  return (
    <div>
      <h1>MAJE Dashboard</h1>

      {user && (
        <div>
          <p>
            Welcome, {user.name}
          </p>

          <p>
            Role: {user.role}
          </p>

          <p>
            Email: {user.email}
          </p>
        </div>
      )}


      <button onClick={logout}>
        Logout
      </button>

    </div>
  );
}
