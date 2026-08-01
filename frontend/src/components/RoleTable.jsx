import PropTypes from "prop-types";

const SYSTEM_ROLES = ["admin", "user"];

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
}) {
  if (loading) {
    return <p>Loading roles...</p>;
  }

  return (
    <div className="table-container">
      <table className="user-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Role Name</th>
            <th width="320">Action</th>
          </tr>
        </thead>

        <tbody>
          {roles.length === 0 ? (
            <tr>
              <td
                colSpan={3}
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
                  <td>{role.id}</td>

                  <td>
                    <span
                      className={
                        role.name.toLowerCase() === "admin"
                          ? "role-badge role-admin"
                          : "role-badge role-user"
                      }
                    >
                      {role.name.charAt(0).toUpperCase() +
                        role.name.slice(1)}
                    </span>
                  </td>

                  <td className="action-column">
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

                    <button
                      type="button"
                      className="btn btn-warning"
                      onClick={() => onEdit(role)}
                      disabled={systemRole}
                      title={
                        systemRole
                          ? "System role cannot be modified"
                          : "Edit role"
                      }
                    >
                      ✏ Edit
                    </button>

                    <button
                      type="button"
                      className="btn btn-danger"
                      onClick={() => onDelete(role)}
                      disabled={systemRole}
                      title={
                        systemRole
                          ? "System role cannot be deleted"
                          : "Delete role"
                      }
                    >
                      🗑 Delete
                    </button>
                  </td>
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
  onEdit: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired,
  onPermissions: PropTypes.func.isRequired,
};

RoleTable.defaultProps = {
  loading: false,
};