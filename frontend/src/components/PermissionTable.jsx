import PropTypes from "prop-types";


export default function PermissionTable({

  permissions,

  loading,

  onEdit,

  onDelete,

  canEdit = false,

  canDelete = false,

}) {


  if (loading) {

    return (
      <p>
        Loading permissions...
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
              Permission Name
            </th>


            {showActions && (

              <th width="180">
                Action
              </th>

            )}

          </tr>

        </thead>


        <tbody>


          {permissions.length === 0 ? (

            <tr>

              <td
                colSpan={
                  showActions
                    ? 3
                    : 2
                }
                className="empty-row"
              >
                No permissions found.
              </td>

            </tr>

          ) : (

            permissions.map(
              (permission) => (

                <tr key={permission.id}>

                  <td>
                    {permission.id}
                  </td>


                  <td>

                    <span className="permission-badge">
                      {permission.name}
                    </span>

                  </td>


                  {showActions && (

                    <td className="action-column">


                      {canEdit && (

                        <button
                          type="button"
                          className="btn btn-warning"
                          onClick={() =>
                            onEdit(permission)
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
                            onDelete(permission)
                          }
                        >
                          🗑 Delete
                        </button>

                      )}


                    </td>

                  )}


                </tr>

              )
            )

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


  onEdit: PropTypes.func,

  onDelete: PropTypes.func,


  canEdit: PropTypes.bool,

  canDelete: PropTypes.bool,

};


PermissionTable.defaultProps = {

  loading: false,


  onEdit: undefined,

  onDelete: undefined,


  canEdit: false,

  canDelete: false,

};