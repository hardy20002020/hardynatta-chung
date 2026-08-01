import { useAuth } from "../auth/AuthContext";

export default function Dashboard() {
  const { user } = useAuth();

  return (
    <div>
      <h1>MAJE Dashboard</h1>

      {user && (
        <>
          <p>
            Role: <strong>{user.role}</strong>
          </p>

          <p>
            Email: <strong>{user.email}</strong>
          </p>
        </>
      )}

      <hr />

      <h2>Dashboard Statistics</h2>

      <p>Coming Soon...</p>
    </div>
  );
}