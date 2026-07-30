import { useEffect, useState } from "react";
import api from "../api/axios";

export default function Profile() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const response = await api.get("/auth/me");
      setUser(response.data.user);
    } catch (error) {
      console.error(error);
      alert("Failed to load profile");
    }
  };

  if (!user) {
    return <p>Loading profile...</p>;
  }

  return (
    <div>
      <h1>My Profile</h1>

      <table>
        <tbody>
          <tr>
            <td><strong>Name</strong></td>
            <td>{user.name}</td>
          </tr>

          <tr>
            <td><strong>Email</strong></td>
            <td>{user.email}</td>
          </tr>

          <tr>
            <td><strong>Role</strong></td>
            <td>{user.role}</td>
          </tr>

          <tr>
            <td><strong>Province</strong></td>
            <td>{user.province_id}</td>
          </tr>

          <tr>
            <td><strong>City</strong></td>
            <td>{user.city_id}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}