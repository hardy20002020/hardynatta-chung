import api from "./axios";

export async function getUsers(page = 1, size = 10) {
  const response = await api.get("/users/", {
    params: {
      page,
      size,
    },
  });

  return response.data;
}