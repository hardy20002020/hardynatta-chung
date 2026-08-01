import { useEffect, useState } from "react";

import {
  getPermissions,
  getPermission,
  createPermission,
  updatePermission,
  deletePermission,
} from "../api/permissionService";

import PermissionTable from "../components/PermissionTable";
import PermissionForm from "../components/PermissionForm";

export default function PermissionManagement() {
  const [permissions, setPermissions] = useState([]);

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const [showForm, setShowForm] = useState(false);
  const [selectedPermission, setSelectedPermission] =
    useState(null);

  useEffect(() => {
    document.title = "MAJE - Permission Management";
    loadPermissions();
  }, []);

  async function loadPermissions() {
    try {
      setLoading(true);
      setError("");

      const data = await getPermissions();

      if (Array.isArray(data)) {
        setPermissions(data);
      } else {
        setPermissions([]);
        setError("Invalid permission data.");
      }
    } catch (err) {
      console.error(
        "Load Permissions Error:",
        err
      );

      setPermissions([]);
      setError("Failed to load permissions.");
    } finally {
      setLoading(false);
    }
  }

  async function handleSave(data) {
    try {
      setSaving(true);

      if (selectedPermission) {
        await updatePermission(
          selectedPermission.id,
          data
        );
      } else {
        await createPermission(data);
      }

      setShowForm(false);
      setSelectedPermission(null);

      await loadPermissions();
    } catch (err) {
      console.error(
        "Save Permission Error:",
        err
      );

      const message =
        err.response?.data?.detail ||
        "Failed to save permission.";

      alert(message);
    } finally {
      setSaving(false);
    }
  }

  async function handleEdit(permission) {
    try {
      const data = await getPermission(
        permission.id
      );

      setSelectedPermission(data);
      setShowForm(true);
    } catch (err) {
      console.error(
        "Load Permission Error:",
        err
      );

      alert("Failed to load permission.");
    }
  }

  async function handleDelete(permission) {
    const confirmed = window.confirm(
      `Delete permission "${permission.name}"?`
    );

    if (!confirmed) {
      return;
    }

    try {
      await deletePermission(permission.id);
      await loadPermissions();
    } catch (err) {
      console.error(
        "Delete Permission Error:",
        err
      );

      const message =
        err.response?.data?.detail ||
        "Failed to delete permission.";

      alert(message);
    }
  }

  return (
    <div>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          gap: "16px",
          marginBottom: "20px",
        }}
      >
        <h1
          style={{
            margin: 0,
          }}
        >
          Permission Management
        </h1>

        <button
          type="button"
          className="btn btn-success"
          onClick={() => {
            setSelectedPermission(null);
            setShowForm(true);
          }}
          disabled={loading || saving}
        >
          + Add Permission
        </button>
      </div>

      {showForm && (
        <PermissionForm
          initialData={selectedPermission}
          loading={saving}
          onSave={handleSave}
          onCancel={() => {
            setShowForm(false);
            setSelectedPermission(null);
          }}
        />
      )}

      {error && (
        <p className="error">
          {error}
        </p>
      )}

      <PermissionTable
        permissions={permissions}
        loading={loading}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />
    </div>
  );
}
