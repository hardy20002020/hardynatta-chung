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
          ========================== */}

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




          {/* =========================
              USER MANAGEMENT
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
          ========================== */}

          <Route

            path="/users/:userId/activity"

            element={

              <ProtectedRoute>

                <MainLayout>

                  <UserActivity />

                </MainLayout>

              </ProtectedRoute>

            }

          />




          {/* =========================
              ROLE MANAGEMENT
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
              403
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