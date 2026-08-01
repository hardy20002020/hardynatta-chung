import { useEffect, useState } from "react";

import { getAuditLogs } from "../api/auditLogService";


export default function AuditLogs() {

    const [logs, setLogs] = useState([]);
    const [loading, setLoading] = useState(true);


    useEffect(() => {

        loadLogs();

    }, []);


    const loadLogs = async () => {

        try {

            const data = await getAuditLogs();

            setLogs(data);

        } catch (error) {

            console.error(
                "Failed loading audit logs",
                error
            );

        } finally {

            setLoading(false);

        }

    };


    if (loading) {

        return (
            <div>
                Loading Audit Logs...
            </div>
        );

    }


    return (

        <div>

            <h1>
                Audit Logs
            </h1>


            <table
                style={{
                    width: "100%",
                    marginTop: "20px",
                    borderCollapse: "collapse",
                }}
            >

                <thead>

                    <tr>

                        <th>ID</th>
                        <th>User</th>
                        <th>Action</th>
                        <th>Resource</th>
                        <th>Description</th>
                        <th>Time</th>

                    </tr>

                </thead>


                <tbody>

                    {logs.map((log) => (

                        <tr key={log.id}>

                            <td>{log.id}</td>

                            <td>{log.user_id}</td>

                            <td>{log.action}</td>

                            <td>{log.resource}</td>

                            <td>{log.description}</td>

                            <td>
                                {new Date(
                                    log.created_at
                                ).toLocaleString()}
                            </td>

                        </tr>

                    ))}

                </tbody>

            </table>

        </div>

    );

}