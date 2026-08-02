import PropTypes from "prop-types";


function getRoleLabel(user) {

  if (user.role) {

    return (
      user.role.charAt(0).toUpperCase() +
      user.role.slice(1)
    );

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

  canEdit = false,

  canDelete = false,

}) {


  if (loading) {

    return (
      <p>
        Loading users...
      </p>
    );

  }



  const showActions =
    canEdit || canDelete;



  return (

    <div className="table-container">

      <table className="user-table">


        <thead>

          <tr>

            <th>
              ID
            </th>

            <th>
              Name
            </th>

            <th>
              Email
            </th>

            <th>
              Role
            </th>


            {showActions && (

              <th width="180">
                Action
              </th>

            )}

          </tr>

        </thead>



        <tbody>


          {users.length === 0 ? (

            <tr>

              <td
                colSpan={
                  showActions
                    ? 5
                    : 4
                }
                className="empty-row"
              >

                No users found.

              </td>

            </tr>

          ) : (

            users.map((user) => (

              <tr key={user.id}>


                <td>
                  {user.id}
                </td>


                <td>
                  {user.name}
                </td>


                <td>
                  {user.email}
                </td>


                <td>

                  <span
                    className={
                      getRoleBadgeClass(user)
                    }
                  >

                    {getRoleLabel(user)}

                  </span>

                </td>



                {showActions && (

                  <td className="action-column">


                    {canEdit && (

                      <button
                        className="btn btn-warning"
                        onClick={() =>
                          onEdit(user)
                        }
                      >

                        ✏ Edit

                      </button>

                    )}



                    {canDelete && (

                      <button
                        className="btn btn-danger"
                        onClick={() =>
                          onDelete(user)
                        }
                      >

                        🗑 Delete

                      </button>

                    )}


                  </td>

                )}


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


  onEdit: PropTypes.func,

  onDelete: PropTypes.func,


  canEdit: PropTypes.bool,

  canDelete: PropTypes.bool,

};



UserTable.defaultProps = {

  loading: false,

  onEdit: undefined,

  onDelete: undefined,

  canEdit: false,

  canDelete: false,

};