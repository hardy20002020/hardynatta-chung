import api from "./axios";


// ==========================================================
// GET AUDIT LOGS (ENTERPRISE PAGINATION + FILTER)
// ==========================================================

export const getAuditLogs = async (
    page = 1,
    size = 10,
    action = null,
    userId = null
) => {

    const response = await api.get(
        "/audit-logs/",
        {
            params: {

                page,

                size,

                ...(action && {
                    action,
                }),

                ...(userId && {
                    user_id: userId,
                }),

            },
        }
    );


    return response.data;
};



// ==========================================================
// GET AUDIT LOGS BY USER
// ==========================================================

export const getUserAuditLogs = async (
    userId
) => {

    const response = await api.get(
        "/audit-logs/",
        {
            params: {
                user_id: userId,
            },
        }
    );


    return response.data;
};