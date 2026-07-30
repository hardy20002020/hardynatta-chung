import { useEffect, useState } from "react";
import { getUsers } from "../api/userService";

export default function UserManagement() {
  const [users, setUsers] = useState([]);
  const [meta, setMeta] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadUsers();
  }, []);

  async function loadUsers() {
    try {
      setLoading(true);
      setError("");

      const response = await getUsers();

      console.log("===== GET USERS RESPONSE =====");
      console.log(response);

      if (response.success) {
        setUsers(response.data?.items ?? []);
        setMeta(response.data?.meta ?? null);
      } else {
        setError(response.message || "Gagal mengambil data user.");
      }
    } catch (err) {
      console.error("===== GET USERS ERROR =====");
      console.error(err);

      if (err.response) {
        console.error("Status :", err.response.status);
        console.error("Response :", err.response.data);

        setError(
          err.response.data?.detail ||
          err.response.data?.message ||
          "Gagal mengambil data user."
        );
      } else {
        console.error("Message :", err.message);
        setError(err.message);
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h1>User Management</h1>

      {loading && <p>Loading...</p>}

      {error && (
        <p style={{ color: "red", fontWeight: "bold" }}>
          {error}
        </p>
      )}

      {!loading && !error && (
        <>
          <table border="1" cellPadding="8" style={{ borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th>ID</th>
                <th>Nama</th>
                <th>Email</th>
                <th>Role ID</th>
              </tr>
            </thead>

            <tbody>
              {users.length === 0 ? (
                <tr>
                  <td colSpan="4">Tidak ada data.</td>
                </tr>
              ) : (
                users.map((user) => (
                  <tr key={user.id}>
                    <td>{user.id}</td>
                    <td>{user.name}</td>
                    <td>{user.email}</td>
                    <td>{user.role_id}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>

          {meta && (
            <div style={{ marginTop: 20 }}>
              <strong>Pagination</strong>

              <p>Page : {meta.page}</p>
              <p>Size : {meta.size}</p>
              <p>Total : {meta.total}</p>
            </div>
          )}
        </>
      )}
    </div>
  );
}