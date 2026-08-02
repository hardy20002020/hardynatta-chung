import { useEffect, useState } from "react";

import {
  getPermissions,
  getPermission,
  createPermission,
  updatePermission,
  deletePermission,
} from "../api/permissionService";

import { useAuth } from "../auth/AuthContext";
import { hasPermission } from "../auth/permissionHelper";

import PermissionTable from "../components/PermissionTable";
import PermissionForm from "../components/PermissionForm";


export default function PermissionManagement() {

  const { user } = useAuth();


  const canCreate =
    hasPermission(
      user,
      "permission.create"
    );

  const canEdit =
    hasPermission(
      user,
      "permission.update"
    );

  const canDelete =
    hasPermission(
      user,
      "permission.delete"
    );


  const [permissions, setPermissions] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [saving, setSaving] =
    useState(false);

  const [error, setError] =
    useState("");


  const [
    showForm,
    setShowForm,
  ] = useState(false);

  const [
    selectedPermission,
    setSelectedPermission,
  ] = useState(null);



  useEffect(() => {

    document.title =
      "MAJE - Permission Management";

    loadPermissions();

  }, []);



  async function loadPermissions() {

    try {

      setLoading(true);

      setError("");


      const data =
        await getPermissions();


      if (Array.isArray(data)) {

        setPermissions(data);

      } else {

        setPermissions([]);

        setError(
          "Invalid permission data."
        );

      }

    } catch (err) {

      console.error(
        "Load Permissions Error:",
        err
      );


      setPermissions([]);

      setError(
        "Failed to load permissions."
      );

    } finally {

      setLoading(false);

    }

  }



  async function handleSave(data) {

    const isCreate =
      !selectedPermission;


    if (
      isCreate &&
      !canCreate
    ) {

      alert(
        "You do not have permission to create permissions."
      );

      return;

    }


    if (
      !isCreate &&
      !canEdit
    ) {

      alert(
        "You do not have permission to update permissions."
      );

      return;

    }


    try {

      setSaving(true);


      if (selectedPermission) {

        await updatePermission(
          selectedPermission.id,
          data
        );

      } else {

        await createPermission(
          data
        );

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



  async function handleEdit(
    permission
  ) {

    if (!canEdit) {

      alert(
        "You do not have permission to update permissions."
      );

      return;

    }


    try {

      const data =
        await getPermission(
          permission.id
        );


      setSelectedPermission(data);

      setShowForm(true);

    } catch (err) {

      console.error(
        "Load Permission Error:",
        err
      );


      alert(
        "Failed to load permission."
      );

    }

  }



  async function handleDelete(
    permission
  ) {

    if (!canDelete) {

      alert(
        "You do not have permission to delete permissions."
      );

      return;

    }


    const confirmed =
      window.confirm(
        `Delete permission "${permission.name}"?`
      );


    if (!confirmed) {

      return;

    }


    try {

      await deletePermission(
        permission.id
      );


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



  function handleAdd() {

    if (!canCreate) {

      return;

    }


    setSelectedPermission(null);

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
          Permission Management
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
            + Add Permission
          </button>

        )}


      </div>



      {showForm &&
        (
          (
            selectedPermission &&
            canEdit
          ) ||
          (
            !selectedPermission &&
            canCreate
          )
        ) && (

          <PermissionForm
            initialData={
              selectedPermission
            }
            loading={saving}
            onSave={handleSave}
            onCancel={() => {

              setShowForm(false);

              setSelectedPermission(
                null
              );

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
        canEdit={canEdit}
        canDelete={canDelete}
      />


    </div>

  );

}