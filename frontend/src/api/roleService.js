import api from "./axios";

/**
 * Get All Roles
 */
export async function getRoles() {
  const response = await api.get("/roles/");
  return response.data;
}

/**
 * Get Role By ID
 */
export async function getRole(roleId) {
  const response = await api.get(`/roles/${roleId}`);
  return response.data;
}

/**
 * Create Role
 */
export async function createRole(roleData) {
  const response = await api.post(
    "/roles/",
    roleData
  );

  return response.data;
}

/**
 * Update Role
 */
export async function updateRole(
  roleId,
  roleData
) {
  const response = await api.put(
    `/roles/${roleId}`,
    roleData
  );

  return response.data;
}

/**
 * Delete Role
 */
export async function deleteRole(roleId) {
  const response = await api.delete(
    `/roles/${roleId}`
  );

  return response.data;
}
