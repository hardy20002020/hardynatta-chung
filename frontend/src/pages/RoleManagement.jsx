import { useEffect, useState } from "react";

import {
  getRoles,
  getRole,
  createRole,
  updateRole,
  deleteRole,
} from "../api/roleService";

import RoleTable from "../components/RoleTable";
import RoleForm from "../components/RoleForm";
import RolePermissionManager from "../components/RolePermissionManager";

export default function RoleManagement() {
  const [roles, setRoles] = useState([]);

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const [showForm, setShowForm] = useState(false);
  const [selectedRole, setSelectedRole] = useState(null);

  const [
    permissionRole,
    setPermissionRole,
  ] = useState(null);

  useEffect(() => {
    document.title = "MAJE - Role Management";
    loadRoles();
  }, []);

  async function loadRoles() {
    try {
      setLoading(true);
      setError("");

      const data = await getRoles();

      if (Array.isArray(data)) {
        setRoles(data);
      } else {
        setRoles([]);
        setError("Invalid role data.");
      }
    } catch (err) {
      console.error("Load Roles Error:", err);

      setRoles([]);
      setError("Failed to load roles.");
    } finally {
      setLoading(false);
    }
  }

  async function handleSave(data) {
    try {
      setSaving(true);

      if (selectedRole) {
        await updateRole(
          selectedRole.id,
          data
        );
      } else {
        await createRole(data);
      }

      setShowForm(false);
      setSelectedRole(null);

      await loadRoles();
    } catch (err) {
      console.error("Save Role Error:", err);

      const message =
        err.response?.data?.detail ||
        "Failed to save role.";

      alert(message);
    } finally {
      setSaving(false);
    }
  }

  async function handleEdit(role) {
    try {
      setPermissionRole(null);

      const data = await getRole(role.id);

      setSelectedRole(data);
      setShowForm(true);
    } catch (err) {
      console.error("Load Role Error:", err);

      alert("Failed to load role.");
    }
  }

  async function handleDelete(role) {
    const confirmed = window.confirm(
      `Delete role "${role.name}"?`
    );

    if (!confirmed) {
      return;
    }

    try {
      await deleteRole(role.id);

      if (permissionRole?.id === role.id) {
        setPermissionRole(null);
      }

      await loadRoles();
    } catch (err) {
      console.error("Delete Role Error:", err);

      const message =
        err.response?.data?.detail ||
        "Failed to delete role.";

      alert(message);
    }
  }

  function handlePermissions(role) {
    setShowForm(false);
    setSelectedRole(null);

    setPermissionRole(role);
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
          Role Management
        </h1>

        <button
          type="button"
          className="btn btn-success"
          onClick={() => {
            setPermissionRole(null);
            setSelectedRole(null);
            setShowForm(true);
          }}
          disabled={loading || saving}
        >
          + Add Role
        </button>
      </div>

      {showForm && (
        <RoleForm
          initialData={selectedRole}
          loading={saving}
          onSave={handleSave}
          onCancel={() => {
            setShowForm(false);
            setSelectedRole(null);
          }}
        />
      )}

      {permissionRole && (
        <RolePermissionManager
          role={permissionRole}
          onClose={() =>
            setPermissionRole(null)
          }
        />
      )}

      {error && (
        <p className="error">
          {error}
        </p>
      )}

      <RoleTable
        roles={roles}
        loading={loading}
        onEdit={handleEdit}
        onDelete={handleDelete}
        onPermissions={handlePermissions}
      />
    </div>
  );
}