from app.core.dependencies import require_permission


#
# User Permissions
#

require_user_read = require_permission(
    "user.read"
)

require_user_create = require_permission(
    "user.create"
)

require_user_update = require_permission(
    "user.update"
)

require_user_delete = require_permission(
    "user.delete"
)


#
# Admin Aliases
#

require_admin_create = require_user_create

require_admin_update = require_user_update

require_admin_delete = require_user_delete