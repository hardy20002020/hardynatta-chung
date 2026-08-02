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
import AuditLogs from "./pages/AuditLogs";
import UserActivity from "./pages/UserActivity";


export default function App() {

  return (

    <AuthProvider>

      <BrowserRouter>

        <Routes>


          {/* =========================
              LOGIN
          ========================== */}

          <Route
            path="/login"
            element={
              <Login />
            }
          />


          {/* =========================
              ROOT
          ========================== */}

          <Route
            path="/"
            element={
              <Navigate
                to="/dashboard"
                replace
              />
            }
          />


          {/* =========================
              DASHBOARD
              Permission: dashboard.read
          ========================== */}

          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>

                <PermissionRoute permission="dashboard.read">

                  <MainLayout>

                    <Dashboard />

                  </MainLayout>

                </PermissionRoute>

              </ProtectedRoute>
            }
          />


          {/* =========================
              USER MANAGEMENT
              Permission: user.read
          ========================== */}

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


          {/* =========================
              USER ACTIVITY TIMELINE
              Permission: audit.read
          ========================== */}

          <Route
            path="/users/:userId/activity"
            element={
              <ProtectedRoute>

                <PermissionRoute permission="audit.read">

                  <MainLayout>

                    <UserActivity />

                  </MainLayout>

                </PermissionRoute>

              </ProtectedRoute>
            }
          />


          {/* =========================
              ROLE MANAGEMENT
              Permission: role.read
          ========================== */}

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


          {/* =========================
              PERMISSION MANAGEMENT
              Permission: permission.read
          ========================== */}

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


          {/* =========================
              AUDIT LOGS
              Permission: audit.read
          ========================== */}

          <Route
            path="/audit-logs"
            element={
              <ProtectedRoute>

                <PermissionRoute permission="audit.read">

                  <MainLayout>

                    <AuditLogs />

                  </MainLayout>

                </PermissionRoute>

              </ProtectedRoute>
            }
          />


          {/* =========================
              PROFILE
          ========================== */}

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


          {/* =========================
              403 FORBIDDEN
          ========================== */}

          <Route
            path="/403"
            element={
              <div
                style={{
                  padding: "50px",
                  textAlign: "center",
                }}
              >

                <h1>
                  403
                </h1>

                <h2>
                  Forbidden
                </h2>

                <p>
                  You do not have permission to access this page.
                </p>

              </div>
            }
          />


          {/* =========================
              FALLBACK
          ========================== */}

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