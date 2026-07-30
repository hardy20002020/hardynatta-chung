import api from "./axios";

/**
 * Get Province List
 */
export async function getProvinces() {
  const response = await api.get("/provinces/");

  return response.data;
}

/**
 * Get Province By ID
 */
export async function getProvince(provinceId) {
  const response = await api.get(`/provinces/${provinceId}`);

  return response.data;
}