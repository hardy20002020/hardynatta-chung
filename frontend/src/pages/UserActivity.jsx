import { useEffect, useState } from "react";

import { useParams, useNavigate } from "react-router-dom";

import { getUserAuditLogs } from "../api/auditLogService";


export default function UserActivity() {


    const {
        userId,
    } = useParams();


    const navigate = useNavigate();


    const [logs, setLogs] = useState([]);

    const [loading, setLoading] = useState(true);



    useEffect(() => {

        loadActivity();

    }, []);




    async function loadActivity() {

        try {

            setLoading(true);


            const response = await getUserAuditLogs(
                userId
            );


            setLogs(
                response.items || []
            );


        } catch (error) {

            console.error(
                "Failed loading user activity",
                error
            );


        } finally {

            setLoading(false);

        }

    }





    if (loading) {

        return (
            <div>
                Loading User Activity...
            </div>
        );

    }





    return (

        <div>


            <button
                onClick={() => navigate(-1)}
            >

                ← Back

            </button>



            <h1>
                User Activity Timeline
            </h1>



            <h3>
                User ID: {userId}
            </h3>




            <div>


                {logs.map((log) => (

                    <div

                        key={log.id}

                        style={{
                            padding: "15px",
                            marginBottom: "10px",
                            borderLeft:
                                "4px solid #2563eb",
                            background:
                                "#f8fafc",
                        }}

                    >


                        <h3>
                            {log.action}
                        </h3>


                        <p>
                            {log.description}
                        </p>


                        <small>

                            {log.resource}
                            {" | "}

                            {
                                new Date(
                                    log.created_at
                                ).toLocaleString()
                            }

                        </small>


                    </div>

                ))}


            </div>



        </div>

    );

}