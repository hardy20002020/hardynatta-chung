import PropTypes from "prop-types";

function getRoleLabel(user) {
  if (user.role) {
    return user.role.charAt(0).toUpperCase() + user.role.slice(1);
  }

  if (user.role_id === 1) {
    return "Administrator";
  }

  return "User";
}

function getRoleBadgeClass(user) {
  if (
    user.role === "admin" ||
    user.role_id === 1
  ) {
    return "role-badge role-admin";
  }

  return "role-badge role-user";
}

export default function UserTable({
  users,
  loading,
  onEdit,
  onDelete,
}) {
  if (loading) {
    return <p>Loading users...</p>;
  }

  return (
    <div className="table-container">
      <table className="user-table">

        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
            <th width="180">
              Action
            </th>
          </tr>
        </thead>

        <tbody>

          {users.length === 0 ? (
            <tr>
              <td
                colSpan={5}
                className="empty-row"
              >
                No users found.
              </td>
            </tr>
          ) : (
            users.map((user) => (
              <tr key={user.id}>

                <td>{user.id}</td>

                <td>{user.name}</td>

                <td>{user.email}</td>

                <td>
                  <span
                    className={getRoleBadgeClass(user)}
                  >
                    {getRoleLabel(user)}
                  </span>
                </td>

                <td className="action-column">

                  <button
                    className="btn btn-warning"
                    onClick={() => onEdit(user)}
                  >
                    ✏ Edit
                  </button>

                  <button
                    className="btn btn-danger"
                    onClick={() => onDelete(user)}
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

UserTable.propTypes = {
  users: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      name: PropTypes.string.isRequired,
      email: PropTypes.string.isRequired,
      role: PropTypes.string,
      role_id: PropTypes.number,
    })
  ).isRequired,

  loading: PropTypes.bool,

  onEdit: PropTypes.func.isRequired,

  onDelete: PropTypes.func.isRequired,
};

UserTable.defaultProps = {
  loading: false,
};