import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { login as loginService } from "../api/authService";
import { useAuth } from "../auth/AuthContext";

export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");

    try {
      const data = await loginService(email, password);

      login(data);

      navigate("/dashboard");
    } catch (err) {
      console.error("===== LOGIN ERROR =====");
      console.error(err);

      if (err.response) {
        console.error("Status:", err.response.status);
        console.error("Data:", err.response.data);
      } else {
        console.error("Message:", err.message);
      }

      setError(
        err.response?.data?.detail ||
        err.message ||
        "Login gagal"
      );
    }
  };

  return (
    <div>
      <h1>MAJE Login</h1>

      {error && <p>{error}</p>}

      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit">
          Login
        </button>
      </form>
    </div>
  );
}