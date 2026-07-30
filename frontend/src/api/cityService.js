import api from "./axios";

/**
 * Get All Cities
 */
export async function getCities() {
  const response = await api.get("/cities/");

  return response.data;
}

/**
 * Get City By ID
 */
export async function getCity(cityId) {
  const response = await api.get(`/cities/${cityId}`);

  return response.data;
}

/**
 * Create City
 */
export async function createCity(data) {
  const response = await api.post("/cities/", data);

  return response.data;
}

/**
 * Update City
 */
export async function updateCity(cityId, data) {
  const response = await api.put(
    `/cities/${cityId}`,
    data
  );

  return response.data;
}

/**
 * Delete City
 */
export async function deleteCity(cityId) {
  const response = await api.delete(
    `/cities/${cityId}`
  );

  return response.data;
}