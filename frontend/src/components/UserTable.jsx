import PropTypes from "prop-types";

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
            <th>Nama</th>
            <th>Email</th>
            <th>Role ID</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          {users.length === 0 ? (
            <tr>
              <td colSpan={5} className="empty-row">
                Tidak ada data.
              </td>
            </tr>
          ) : (
            users.map((user) => (
              <tr key={user.id}>
                <td>{user.id}</td>
                <td>{user.name}</td>
                <td>{user.email}</td>
                <td>{user.role_id}</td>

                <td className="action-column">
                  <button
                    className="btn btn-warning"
                    onClick={() => onEdit(user)}
                  >
                    Edit
                  </button>

                  <button
                    className="btn btn-danger"
                    onClick={() => onDelete(user)}
                  >
                    Delete
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
      role_id: PropTypes.number.isRequired,
    })
  ).isRequired,

  loading: PropTypes.bool,

  onEdit: PropTypes.func.isRequired,

  onDelete: PropTypes.func.isRequired,
};

UserTable.defaultProps = {
  loading: false,
};