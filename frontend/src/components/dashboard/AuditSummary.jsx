import { useEffect, useState } from "react";

import { getAuditSummary } from "../../api/auditLogService";


export default function AuditSummary() {

    const [summary, setSummary] = useState({});


    useEffect(() => {

        loadSummary();

    }, []);



    async function loadSummary() {

        try {

            const logs = await getAuditSummary();


            const result = {};


            logs.forEach((log) => {

                if (result[log.action]) {

                    result[log.action] += 1;

                } else {

                    result[log.action] = 1;

                }

            });


            setSummary(result);


        } catch (error) {

            console.error(
                "Audit Summary Error:",
                error
            );

        }

    }



    return (

        <div className="card">

            <h2>
                Audit Summary
            </h2>


            {Object.keys(summary).length === 0 ? (

                <p>
                    No audit data.
                </p>


            ) : (

                Object.entries(summary).map(
                    ([action, total]) => (

                        <div
                            key={action}
                            style={{
                                display: "flex",
                                justifyContent: "space-between",
                                padding: "10px 0",
                                borderBottom:
                                  "1px solid #eee",
                            }}
                        >

                            <strong>
                                {action}
                            </strong>


                            <span>
                                {total}
                            </span>

                        </div>

                    )
                )

            )}

        </div>

    );

}
