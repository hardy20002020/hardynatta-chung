import { useEffect, useState } from "react";
import PropTypes from "prop-types";

import { getPermissions } from "../api/permissionService";

import {
  getRolePermissions,
  assignRolePermission,
  revokeRolePermission,
} from "../api/rolePermissionService";


export default function RolePermissionManager({
  role,
  canAssign = false,
  canRevoke = false,
  onClose,
}) {

  const [permissions, setPermissions] =
    useState([]);

  const [assignedIds, setAssignedIds] =
    useState(new Set());

  const [loading, setLoading] =
    useState(true);

  const [savingId, setSavingId] =
    useState(null);

  const [error, setError] =
    useState("");


  useEffect(() => {

    loadData();

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [role.id]);


  async function loadData() {

    try {

      setLoading(true);

      setError("");


      const [
        allPermissions,
        rolePermissions,
      ] = await Promise.all([

        getPermissions(),

        getRolePermissions(role.id),

      ]);


      setPermissions(
        Array.isArray(allPermissions)
          ? allPermissions
          : []
      );


      setAssignedIds(
        new Set(
          Array.isArray(rolePermissions)
            ? rolePermissions.map(
                (permission) =>
                  permission.id
              )
            : []
        )
      );

    } catch (err) {

      console.error(
        "Load Role Permissions Error:",
        err
      );


      setError(
        "Failed to load role permissions."
      );

    } finally {

      setLoading(false);

    }

  }


  async function handleToggle(permission) {

    const isAssigned =
      assignedIds.has(permission.id);


    if (
      isAssigned &&
      !canRevoke
    ) {

      return;

    }


    if (
      !isAssigned &&
      !canAssign
    ) {

      return;

    }


    try {

      setSavingId(
        permission.id
      );


      if (isAssigned) {

        await revokeRolePermission(
          role.id,
          permission.id
        );

      } else {

        await assignRolePermission(
          role.id,
          permission.id
        );

      }


      setAssignedIds((current) => {

        const next =
          new Set(current);


        if (isAssigned) {

          next.delete(
            permission.id
          );

        } else {

          next.add(
            permission.id
          );

        }


        return next;

      });

    } catch (err) {

      console.error(
        "Update Role Permission Error:",
        err
      );


      const message =
        err.response?.data?.detail ||
        "Failed to update role permission.";


      alert(message);

    } finally {

      setSavingId(null);

    }

  }


  return (

    <div className="card mb-3">


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


        <div>

          <h2
            style={{
              margin: 0,
            }}
          >
            Manage Permissions
          </h2>


          <p
            style={{
              marginTop: "6px",
              color: "#6b7280",
            }}
          >

            Role:{" "}

            <strong>

              {
                role.name
                  .charAt(0)
                  .toUpperCase() +
                role.name.slice(1)
              }

            </strong>

          </p>

        </div>


        <button
          type="button"
          className="btn"
          onClick={onClose}
          style={{
            color: "#374151",
          }}
        >
          Close
        </button>


      </div>


      {error && (

        <p className="error">
          {error}
        </p>

      )}


      {!canAssign &&
        !canRevoke && (

          <p
            style={{
              color: "#6b7280",
            }}
          >
            Read-only permission access.
          </p>

        )}


      {loading ? (

        <p>
          Loading permissions...
        </p>

      ) : (

        <div className="permission-grid">


          {permissions.map(
            (permission) => {

              const checked =
                assignedIds.has(
                  permission.id
                );


              const saving =
                savingId ===
                permission.id;


              const canToggle =
                checked
                  ? canRevoke
                  : canAssign;


              return (

                <label
                  key={permission.id}
                  className="permission-item"
                >

                  <input
                    type="checkbox"
                    checked={checked}
                    disabled={
                      saving ||
                      !canToggle
                    }
                    onChange={() =>
                      handleToggle(
                        permission
                      )
                    }
                  />


                  <span>
                    {permission.name}
                  </span>


                  {saving && (

                    <small>
                      Saving...
                    </small>

                  )}


                </label>

              );

            }
          )}


        </div>

      )}


    </div>

  );

}


RolePermissionManager.propTypes = {

  role: PropTypes.shape({

    id: PropTypes.number.isRequired,

    name: PropTypes.string.isRequired,

  }).isRequired,


  canAssign: PropTypes.bool,

  canRevoke: PropTypes.bool,


  onClose: PropTypes.func.isRequired,

};


RolePermissionManager.defaultProps = {

  canAssign: false,

  canRevoke: false,

};