import { Navigate } from "react-router-dom";

import { useAuth } from "./AuthContext";
import { hasPermission } from "./permissionHelper";

export default function PermissionRoute({
  permission,
  children,
}) {
  const { user } = useAuth();

  if (!user) {
    return (
      <Navigate
        to="/login"
        replace
      />
    );
  }

  if (
    !hasPermission(
      user,
      permission
    )
  ) {
    return (
      <Navigate
        to="/403"
        replace
      />
    );
  }

  return children;
}