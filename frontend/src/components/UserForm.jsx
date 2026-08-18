import { useEffect, useState } from "react";

export default function UserForm({
  initialData = null,
  onSave,
  onCancel,
  loading = false,
}) {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    province_id: null,
    city_id: null,
  });

  useEffect(() => {
    if (initialData) {
      setFormData({
        name: initialData.name ?? "",
        email: initialData.email ?? "",
        password: "",
        province_id: initialData.province_id ?? null,
        city_id: initialData.city_id ?? null,
      });
    } else {
      setFormData({
        name: "",
        email: "",
        password: "",
        province_id: null,
        city_id: null,
      });
    }
  }, [initialData]);

  function handleChange(e) {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]:
        name === "province_id" || name === "city_id"
          ? value === "" ? null : Number(value)
          : value,
    }));
  }

  function handleSubmit(e) {
    e.preventDefault();

    const payload = {
      ...formData,
    };

    // Saat Edit, jangan kirim password jika kosong
    if (initialData && payload.password.trim() === "") {
      delete payload.password;
    }

    onSave(payload);
  }

  return (
    <div
      style={{
        border: "1px solid #ddd",
        borderRadius: 8,
        padding: 20,
        marginBottom: 20,
        backgroundColor: "#fff",
      }}
    >
      <h2>
        {initialData ? "Edit User" : "Create User"}
      </h2>

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: 15 }}>
          <label>Name</label>

          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            style={{
              width: "100%",
              padding: 8,
              marginTop: 5,
            }}
          />
        </div>

        <div style={{ marginBottom: 15 }}>
          <label>Email</label>

          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            style={{
              width: "100%",
              padding: 8,
              marginTop: 5,
            }}
          />
        </div>

        <div style={{ marginBottom: 15 }}>
          <label>Password</label>

          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder={
              initialData
                ? "Kosongkan jika tidak ingin mengubah password"
                : "Masukkan password"
            }
            required={!initialData}
            style={{
              width: "100%",
              padding: 8,
              marginTop: 5,
            }}
          />
        </div>

        <div style={{ marginBottom: 15 }}>
          <label>Province ID</label>

          <input
            type="number"
            name="province_id"
            value={formData.province_id}
            onChange={handleChange}
            min={1}
            style={{
              width: "100%",
              padding: 8,
              marginTop: 5,
            }}
          />
        </div>

        <div style={{ marginBottom: 15 }}>
          <label>City ID</label>

          <input
            type="number"
            name="city_id"
            value={formData.city_id}
            onChange={handleChange}
            min={1}
            style={{
              width: "100%",
              padding: 8,
              marginTop: 5,
            }}
          />
        </div>

        <div
          style={{
            display: "flex",
            gap: 10,
          }}
        >
          <button
            type="submit"
            disabled={loading}
          >
            {loading ? "Saving..." : "Save"}
          </button>

          <button
            type="button"
            onClick={onCancel}
            disabled={loading}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}