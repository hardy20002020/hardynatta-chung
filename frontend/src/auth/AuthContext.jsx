import {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";

import {
  getCurrentUser,
} from "../api/authService";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    restoreSession();
  }, []);

  const restoreSession = async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      setLoading(false);
      return;
    }

    try {
      const response = await getCurrentUser();

      // Backend MAJE mengembalikan { success, message, user }
      const currentUser = response.user;

      localStorage.setItem(
        "user",
        JSON.stringify(currentUser)
      );

      setUser(currentUser);
    } catch (err) {
      console.error("Restore session failed:", err);

      localStorage.removeItem("access_token");
      localStorage.removeItem("user");

      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const login = (data) => {
    localStorage.setItem(
      "access_token",
      data.access_token
    );

    localStorage.setItem(
      "user",
      JSON.stringify(data.user)
    );

    setUser(data.user);
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");

    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        logout,
        restoreSession,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}