import api from "./axios";

/**
 * Get User List
 */
export async function getUsers(
  page = 1,
  size = 10,
  search = ""
) {
  const response = await api.get("/users/", {
    params: {
      page,
      size,
      search,
    },
  });

  return response.data;
}

/**
 * Get User By ID
 */
export async function getUser(userId) {
  const response = await api.get(`/users/${userId}`);

  return response.data;
}

/**
 * Create User
 */
export async function createUser(userData) {
  const response = await api.post("/users/", userData);

  return response.data;
}

/**
 * Update User
 */
export async function updateUser(userId, userData) {
  const response = await api.put(
    `/users/${userId}`,
    userData
  );

  return response.data;
}

/**
 * Delete User
 */
export async function deleteUser(userId) {
  const response = await api.delete(
    `/users/${userId}`
  );

  return response.data;
}