import { useEffect, useState } from "react";

import { getAuditLogs } from "../api/auditLogService";


export default function AuditLogs() {


    const [logs, setLogs] = useState([]);

    const [total, setTotal] = useState(0);

    const [page, setPage] = useState(1);

    const size = 10;


    const [action, setAction] = useState("");

    const [userId, setUserId] = useState("");


    const [loading, setLoading] = useState(true);



    useEffect(() => {

        loadLogs();

    }, [
        page,
        action,
    ]);




    async function loadLogs() {

        try {

            setLoading(true);


            const data = await getAuditLogs(

                page,

                size,

                action || null,

                userId || null

            );


            setLogs(
                data.items
            );


            setTotal(
                data.total
            );


        } catch (error) {

            console.error(
                "Failed loading audit logs",
                error
            );


        } finally {

            setLoading(false);

        }

    }





    function handleSearch() {

        setPage(1);

        loadLogs();

    }





    function handlePrevious() {

        if (page > 1) {

            setPage(
                page - 1
            );

        }

    }





    function handleNext() {

        if (
            page * size < total
        ) {

            setPage(
                page + 1
            );

        }

    }





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



            {/* FILTER */}

            <div
                style={{
                    marginBottom: "20px",
                }}
            >


                <select

                    value={action}

                    onChange={(e) => {

                        setAction(
                            e.target.value
                        );

                        setPage(1);

                    }}

                >

                    <option value="">
                        All Actions
                    </option>


                    <option value="LOGIN">
                        LOGIN
                    </option>


                    <option value="CREATE_USER">
                        CREATE_USER
                    </option>


                    <option value="UPDATE_USER">
                        UPDATE_USER
                    </option>


                    <option value="DELETE_USER">
                        DELETE_USER
                    </option>


                </select>





                <input

                    type="number"

                    placeholder="User ID"

                    value={userId}

                    onChange={(e) =>
                        setUserId(
                            e.target.value
                        )
                    }

                    style={{
                        marginLeft: "10px",
                    }}

                />





                <button

                    onClick={handleSearch}

                    style={{
                        marginLeft: "10px",
                    }}

                >

                    Search

                </button>


            </div>





            <p>

                Total Records: {total}

            </p>





            <table

                style={{

                    width: "100%",

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

                        <tr
                            key={log.id}
                        >

                            <td>
                                {log.id}
                            </td>


                            <td>
                                {log.user_id}
                            </td>


                            <td>
                                {log.action}
                            </td>


                            <td>
                                {log.resource}
                            </td>


                            <td>
                                {log.description}
                            </td>


                            <td>

                                {new Date(
                                    log.created_at
                                ).toLocaleString()}

                            </td>


                        </tr>

                    ))}


                </tbody>


            </table>





            {/* PAGINATION */}


            <div

                style={{

                    marginTop: "20px",

                }}

            >


                <button

                    onClick={handlePrevious}

                    disabled={
                        page === 1
                    }

                >

                    Previous

                </button>




                <span

                    style={{

                        margin: "0 15px",

                    }}

                >

                    Page {page}

                </span>




                <button

                    onClick={handleNext}

                    disabled={
                        page * size >= total
                    }

                >

                    Next

                </button>


            </div>



        </div>

    );

}