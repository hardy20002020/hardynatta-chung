import PropTypes from "prop-types";

export default function PermissionTable({
  permissions,
  loading,
  onEdit,
  onDelete,
}) {
  if (loading) {
    return <p>Loading permissions...</p>;
  }

  return (
    <div className="table-container">
      <table className="user-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Permission Name</th>
            <th width="180">Action</th>
          </tr>
        </thead>

        <tbody>
          {permissions.length === 0 ? (
            <tr>
              <td
                colSpan={3}
                className="empty-row"
              >
                No permissions found.
              </td>
            </tr>
          ) : (
            permissions.map((permission) => (
              <tr key={permission.id}>
                <td>{permission.id}</td>

                <td>
                  <span className="permission-badge">
                    {permission.name}
                  </span>
                </td>

                <td className="action-column">
                  <button
                    type="button"
                    className="btn btn-warning"
                    onClick={() =>
                      onEdit(permission)
                    }
                  >
                    ✏ Edit
                  </button>

                  <button
                    type="button"
                    className="btn btn-danger"
                    onClick={() =>
                      onDelete(permission)
                    }
                  >
                    🗑 Delete
                  </button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

PermissionTable.propTypes = {
  permissions: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      name: PropTypes.string.isRequired,
    })
  ).isRequired,

  loading: PropTypes.bool,
  onEdit: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired,
};

PermissionTable.defaultProps = {
  loading: false,
};
