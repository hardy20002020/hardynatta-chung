import PropTypes from "prop-types";


const SYSTEM_ROLES = [
  "admin",
  "user",
];


function isSystemRole(role) {

  return SYSTEM_ROLES.includes(
    role.name.toLowerCase()
  );

}


export default function RoleTable({

  roles,

  loading,

  onEdit,

  onDelete,

  onPermissions,

  canEdit = false,

  canDelete = false,

  canManagePermissions = false,

}) {


  if (loading) {

    return (
      <p>
        Loading roles...
      </p>
    );

  }


  const showActions =
    canEdit ||
    canDelete ||
    canManagePermissions;


  return (

    <div className="table-container">

      <table className="user-table">


        <thead>

          <tr>

            <th>
              ID
            </th>

            <th>
              Role Name
            </th>


            {showActions && (

              <th width="320">
                Action
              </th>

            )}

          </tr>

        </thead>


        <tbody>

          {roles.length === 0 ? (

            <tr>

              <td
                colSpan={
                  showActions
                    ? 3
                    : 2
                }
                className="empty-row"
              >
                No roles found.
              </td>

            </tr>

          ) : (

            roles.map((role) => {

              const systemRole =
                isSystemRole(role);


              return (

                <tr key={role.id}>

                  <td>
                    {role.id}
                  </td>


                  <td>

                    <span
                      className={
                        role.name.toLowerCase() ===
                        "admin"
                          ? "role-badge role-admin"
                          : "role-badge role-user"
                      }
                    >

                      {
                        role.name
                          .charAt(0)
                          .toUpperCase() +
                        role.name.slice(1)
                      }

                    </span>

                  </td>


                  {showActions && (

                    <td className="action-column">


                      {canManagePermissions && (

                        <button
                          type="button"
                          className="btn btn-primary"
                          onClick={() =>
                            onPermissions(role)
                          }
                          title="Manage role permissions"
                        >
                          🔑 Permissions
                        </button>

                      )}


                      {canEdit && (

                        <button
                          type="button"
                          className="btn btn-warning"
                          onClick={() =>
                            onEdit(role)
                          }
                          disabled={systemRole}
                          title={
                            systemRole
                              ? "System role cannot be modified"
                              : "Edit role"
                          }
                        >
                          ✏ Edit
                        </button>

                      )}


                      {canDelete && (

                        <button
                          type="button"
                          className="btn btn-danger"
                          onClick={() =>
                            onDelete(role)
                          }
                          disabled={systemRole}
                          title={
                            systemRole
                              ? "System role cannot be deleted"
                              : "Delete role"
                          }
                        >
                          🗑 Delete
                        </button>

                      )}


                    </td>

                  )}

                </tr>

              );

            })

          )}

        </tbody>


      </table>

    </div>

  );

}


RoleTable.propTypes = {

  roles: PropTypes.arrayOf(

    PropTypes.shape({

      id: PropTypes.number.isRequired,

      name: PropTypes.string.isRequired,

    })

  ).isRequired,


  loading: PropTypes.bool,


  onEdit: PropTypes.func,

  onDelete: PropTypes.func,

  onPermissions: PropTypes.func,


  canEdit: PropTypes.bool,

  canDelete: PropTypes.bool,

  canManagePermissions: PropTypes.bool,

};


RoleTable.defaultProps = {

  loading: false,


  onEdit: undefined,

  onDelete: undefined,

  onPermissions: undefined,


  canEdit: false,

  canDelete: false,

  canManagePermissions: false,

};