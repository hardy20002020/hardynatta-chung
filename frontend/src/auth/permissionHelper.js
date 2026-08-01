export function hasPermission(user, permission) {
  if (!user) {
    return false;
  }

  const permissions = user.permissions || [];

  // Wildcard admin
  if (permissions.includes("*")) {
    return true;
  }

  return permissions.includes(permission);
}

export function hasAnyPermission(user, permissions) {
  if (!user) {
    return false;
  }

  return permissions.some((permission) =>
    hasPermission(user, permission)
  );
}

export function hasAllPermissions(user, permissions) {
  if (!user) {
    return false;
  }

  return permissions.every((permission) =>
    hasPermission(user, permission)
  );
}
