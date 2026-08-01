import { useEffect, useState } from "react";

import { useAuth } from "../auth/AuthContext";

import dashboardService from "../api/dashboardService";

import {
  getRecentAuditLogs,
} from "../api/auditLogService";

import AuditSummary from "../components/dashboard/AuditSummary";


export default function Dashboard() {

  const { user } = useAuth();


  const [stats, setStats] = useState({

    total_users: 0,

    total_provinces: 0,

    total_cities: 0,

    total_audit_logs: 0,

    today_login: 0,

    today_user_changes: 0,

  });



  const [recentLogs, setRecentLogs] = useState([]);


  const [loading, setLoading] = useState(true);



  useEffect(() => {

    loadDashboard();

  }, []);




  async function loadDashboard() {

    try {

      const data =
        await dashboardService.getDashboard();


      setStats(data);



      const logs =
        await getRecentAuditLogs();


      setRecentLogs(
        logs.items || []
      );


    } catch (error) {

      console.error(
        "Dashboard Error:",
        error
      );

    } finally {

      setLoading(false);

    }

  }




  return (

    <div>


      <h1>
        MAJE Dashboard
      </h1>




      {user && (

        <div className="card">

          <h2>
            Welcome back 👋
          </h2>


          <p>
            <strong>
              {user.name}
            </strong>
          </p>


          <p>
            {user.email}
          </p>


          <p>

            <strong>
              Role:
            </strong>{" "}

            {user.role}

          </p>


        </div>

      )}






      <h2 className="mt-3">
        Dashboard Statistics
      </h2>




      {loading ? (

        <p>
          Loading...
        </p>


      ) : (

        <div className="dashboard-grid">


          <div className="stat-card">

            <div className="stat-icon">
              👥
            </div>

            <div className="stat-title">
              Total Users
            </div>

            <div className="stat-value">
              {stats.total_users}
            </div>

          </div>




          <div className="stat-card">

            <div className="stat-icon">
              🗺️
            </div>

            <div className="stat-title">
              Total Provinces
            </div>

            <div className="stat-value">
              {stats.total_provinces}
            </div>

          </div>




          <div className="stat-card">

            <div className="stat-icon">
              🏙️
            </div>

            <div className="stat-title">
              Total Cities
            </div>

            <div className="stat-value">
              {stats.total_cities}
            </div>

          </div>




          <div className="stat-card">

            <div className="stat-icon">
              📋
            </div>

            <div className="stat-title">
              Total Audit Logs
            </div>

            <div className="stat-value">
              {stats.total_audit_logs}
            </div>

          </div>




          <div className="stat-card">

            <div className="stat-icon">
              🔐
            </div>

            <div className="stat-title">
              Login Today
            </div>

            <div className="stat-value">
              {stats.today_login}
            </div>

          </div>




          <div className="stat-card">

            <div className="stat-icon">
              ✏️
            </div>

            <div className="stat-title">
              User Changes Today
            </div>

            <div className="stat-value">
              {stats.today_user_changes}
            </div>

          </div>


        </div>

      )}






      <h2 className="mt-3">
        Analytics
      </h2>


      <AuditSummary />






      <h2 className="mt-3">
        Recent Activity
      </h2>



      <div className="card">


        {recentLogs.length === 0 ? (

          <p>
            No activity found.
          </p>


        ) : (


          recentLogs.map((log) => (

            <div
              key={log.id}
              style={{

                padding: "12px 0",

                borderBottom:
                  "1px solid #eee",

              }}
            >

              <strong>
                {log.action}
              </strong>


              <p>
                {log.description}
              </p>


              <small>

                {log.resource}

                {" | "}

                {new Date(
                  log.created_at
                ).toLocaleString()}

              </small>


            </div>

          ))

        )}


      </div>



    </div>

  );

}