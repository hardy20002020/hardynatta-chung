import { useAuth } from "../auth/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <header
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "16px 24px",
        borderBottom: "1px solid #ddd",
        marginBottom: "24px",
      }}
    >
      <div>
        <h3
          style={{
            margin: 0,
          }}
        >
          {user?.name}
        </h3>

        <small
          style={{
            color: "#888",
          }}
        >
          {user?.email}
        </small>
      </div>

      <button onClick={logout}>
        Logout
      </button>
    </header>
  );
}