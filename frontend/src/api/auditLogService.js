import api from "./axios";


// ==========================================================
// GET AUDIT LOGS
// ==========================================================

export const getAuditLogs = async (
    skip = 0,
    limit = 100
) => {
    const response = await api.get(
        "/audit-logs/",
        {
            params: {
                skip,
                limit,
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
        `/audit-logs/user/${userId}`
    );

    return response.data;
};