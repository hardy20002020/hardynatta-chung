import api from "./axios";

/**
 * Get All Permissions
 */
export async function getPermissions() {
  const response = await api.get("/permissions/");
  return response.data;
}

/**
 * Get Permission By ID
 */
export async function getPermission(permissionId) {
  const response = await api.get(
    `/permissions/${permissionId}`
  );

  return response.data;
}

/**
 * Create Permission
 */
export async function createPermission(
  permissionData
) {
  const response = await api.post(
    "/permissions/",
    permissionData
  );

  return response.data;
}

/**
 * Update Permission
 */
export async function updatePermission(
  permissionId,
  permissionData
) {
  const response = await api.put(
    `/permissions/${permissionId}`,
    permissionData
  );

  return response.data;
}

/**
 * Delete Permission
 */
export async function deletePermission(
  permissionId
) {
  const response = await api.delete(
    `/permissions/${permissionId}`
  );

  return response.data;
}
