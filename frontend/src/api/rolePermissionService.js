import api from "./axios";

/**
 * Get Permissions Assigned To Role
 */
export async function getRolePermissions(roleId) {
  const response = await api.get(
    `/role-permissions/${roleId}`
  );

  return response.data;
}

/**
 * Assign Permission To Role
 */
export async function assignRolePermission(
  roleId,
  permissionId
) {
  const response = await api.post(
    `/role-permissions/${roleId}/${permissionId}`
  );

  return response.data;
}

/**
 * Revoke Permission From Role
 */
export async function revokeRolePermission(
  roleId,
  permissionId
) {
  const response = await api.delete(
    `/role-permissions/${roleId}/${permissionId}`
  );

  return response.data;
}
