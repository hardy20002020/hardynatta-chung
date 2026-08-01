import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import { AuthProvider } from "./auth/AuthContext";
import ProtectedRoute from "./auth/ProtectedRoute";
import PermissionRoute from "./auth/PermissionRoute";

import MainLayout from "./layouts/MainLayout";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import UserManagement from "./pages/UserManagement";
import RoleManagement from "./pages/RoleManagement";
import PermissionManagement from "./pages/PermissionManagement";
import Profile from "./pages/Profile";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>

          {/* Login */}
          <Route
            path="/login"
            element={<Login />}
          />

          {/* Root */}
          <Route
            path="/"
            element={
              <Navigate
                to="/dashboard"
                replace
              />
            }
          />

          {/* Dashboard */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <MainLayout>
                  <Dashboard />
                </MainLayout>
              </ProtectedRoute>
            }
          />

          {/* User Management */}
          <Route
            path="/users"
            element={
              <ProtectedRoute>
                <PermissionRoute permission="user.read">
                  <MainLayout>
                    <UserManagement />
                  </MainLayout>
                </PermissionRoute>
              </ProtectedRoute>
            }
          />

          {/* Role Management */}
          <Route
            path="/roles"
            element={
              <ProtectedRoute>
                <PermissionRoute permission="role.read">
                  <MainLayout>
                    <RoleManagement />
                  </MainLayout>
                </PermissionRoute>
              </ProtectedRoute>
            }
          />

          {/* Permission Management */}
          <Route
            path="/permissions"
            element={
              <ProtectedRoute>
                <PermissionRoute permission="permission.read">
                  <MainLayout>
                    <PermissionManagement />
                  </MainLayout>
                </PermissionRoute>
              </ProtectedRoute>
            }
          />

          {/* Profile */}
          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <MainLayout>
                  <Profile />
                </MainLayout>
              </ProtectedRoute>
            }
          />

          {/* 403 Forbidden */}
          <Route
            path="/403"
            element={
              <div
                style={{
                  padding: "50px",
                  textAlign: "center",
                }}
              >
                <h1>403</h1>

                <h2>Forbidden</h2>

                <p>
                  You do not have permission to access this page.
                </p>
              </div>
            }
          />

          {/* Fallback */}
          <Route
            path="*"
            element={
              <Navigate
                to="/dashboard"
                replace
              />
            }
          />

        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}