import { useEffect, useState } from "react";

import {
  getRoles,
  getRole,
  createRole,
  updateRole,
  deleteRole,
} from "../api/roleService";

import { useAuth } from "../auth/AuthContext";
import { hasPermission } from "../auth/permissionHelper";

import RoleTable from "../components/RoleTable";
import RoleForm from "../components/RoleForm";
import RolePermissionManager from "../components/RolePermissionManager";


export default function RoleManagement() {

  const { user } = useAuth();


  const canCreate =
    hasPermission(user, "role.create");

  const canEdit =
    hasPermission(user, "role.update");

  const canDelete =
    hasPermission(user, "role.delete");

  const canReadPermissions =
    hasPermission(user, "permission.read");

  const canAssignPermissions =
    hasPermission(
      user,
      "role.permission.assign"
    );

  const canRevokePermissions =
    hasPermission(
      user,
      "role.permission.revoke"
    );


  const canManagePermissions =
    canReadPermissions;


  const [roles, setRoles] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [saving, setSaving] =
    useState(false);

  const [error, setError] =
    useState("");


  const [showForm, setShowForm] =
    useState(false);

  const [selectedRole, setSelectedRole] =
    useState(null);


  const [
    permissionRole,
    setPermissionRole,
  ] = useState(null);



  useEffect(() => {

    document.title =
      "MAJE - Role Management";

    loadRoles();

  }, []);



  async function loadRoles() {

    try {

      setLoading(true);

      setError("");


      const data =
        await getRoles();


      if (Array.isArray(data)) {

        setRoles(data);

      } else {

        setRoles([]);

        setError(
          "Invalid role data."
        );

      }

    } catch (err) {

      console.error(
        "Load Roles Error:",
        err
      );


      setRoles([]);

      setError(
        "Failed to load roles."
      );

    } finally {

      setLoading(false);

    }

  }



  async function handleSave(data) {

    const isCreate =
      !selectedRole;


    if (
      isCreate &&
      !canCreate
    ) {

      alert(
        "You do not have permission to create roles."
      );

      return;

    }


    if (
      !isCreate &&
      !canEdit
    ) {

      alert(
        "You do not have permission to update roles."
      );

      return;

    }


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

      console.error(
        "Save Role Error:",
        err
      );


      const message =
        err.response?.data?.detail ||
        "Failed to save role.";


      alert(message);

    } finally {

      setSaving(false);

    }

  }



  async function handleEdit(role) {

    if (!canEdit) {

      alert(
        "You do not have permission to update roles."
      );

      return;

    }


    try {

      setPermissionRole(null);


      const data =
        await getRole(role.id);


      setSelectedRole(data);

      setShowForm(true);

    } catch (err) {

      console.error(
        "Load Role Error:",
        err
      );


      alert(
        "Failed to load role."
      );

    }

  }



  async function handleDelete(role) {

    if (!canDelete) {

      alert(
        "You do not have permission to delete roles."
      );

      return;

    }


    const confirmed =
      window.confirm(
        `Delete role "${role.name}"?`
      );


    if (!confirmed) {

      return;

    }


    try {

      await deleteRole(role.id);


      if (
        permissionRole?.id ===
        role.id
      ) {

        setPermissionRole(null);

      }


      await loadRoles();

    } catch (err) {

      console.error(
        "Delete Role Error:",
        err
      );


      const message =
        err.response?.data?.detail ||
        "Failed to delete role.";


      alert(message);

    }

  }



  function handlePermissions(role) {

    if (!canManagePermissions) {

      return;

    }


    setShowForm(false);

    setSelectedRole(null);

    setPermissionRole(role);

  }



  function handleAdd() {

    if (!canCreate) {

      return;

    }


    setPermissionRole(null);

    setSelectedRole(null);

    setShowForm(true);

  }



  return (

    <div>


      <div
        style={{
          display: "flex",
          justifyContent:
            "space-between",
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


        {canCreate && (

          <button
            type="button"
            className="btn btn-success"
            onClick={handleAdd}
            disabled={
              loading ||
              saving
            }
          >
            + Add Role
          </button>

        )}


      </div>



      {showForm &&
        (
          (selectedRole && canEdit) ||
          (!selectedRole && canCreate)
        ) && (

          <RoleForm
            initialData={
              selectedRole
            }
            loading={saving}
            onSave={handleSave}
            onCancel={() => {

              setShowForm(false);

              setSelectedRole(null);

            }}
          />

        )}



      {permissionRole &&
        canManagePermissions && (

          <RolePermissionManager
            role={permissionRole}
            canAssign={
              canAssignPermissions
            }
            canRevoke={
              canRevokePermissions
            }
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
        onPermissions={
          handlePermissions
        }
        canEdit={canEdit}
        canDelete={canDelete}
        canManagePermissions={
          canManagePermissions
        }
      />


    </div>

  );

}