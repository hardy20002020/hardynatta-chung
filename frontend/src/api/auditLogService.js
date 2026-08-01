import api from "./axios";


// ==========================================================
// GET AUDIT LOGS
// ENTERPRISE PAGINATION + FILTER
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
// GET RECENT AUDIT LOGS
// DASHBOARD RECENT ACTIVITY WIDGET
// ==========================================================

export const getRecentAuditLogs = async () => {

    const response = await api.get(
        "/audit-logs/",
        {
            params: {

                page: 1,

                size: 5,

            },
        }
    );


    return response.data;
};




// ==========================================================
// GET AUDIT SUMMARY
// DASHBOARD ANALYTICS
// ==========================================================

export const getAuditSummary = async () => {

    const response = await api.get(
        "/audit-logs/",
        {
            params: {

                page: 1,

                size: 100,

            },
        }
    );


    return response.data.items;
};




// ==========================================================
// GET AUDIT LOGS BY USER
// USER ACTIVITY TIMELINE
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