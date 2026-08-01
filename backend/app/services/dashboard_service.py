from datetime import datetime, date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.province import Province
from app.models.city import City
from app.models.audit_log import AuditLog



class DashboardService:


    @staticmethod
    def get_dashboard(db: Session):

        today = date.today()


        total_users = (
            db.query(func.count(User.id))
            .scalar()
        )


        total_provinces = (
            db.query(func.count(Province.id))
            .scalar()
        )


        total_cities = (
            db.query(func.count(City.id))
            .scalar()
        )


        total_audit_logs = (
            db.query(func.count(AuditLog.id))
            .scalar()
        )


        today_login = (
            db.query(func.count(AuditLog.id))
            .filter(
                AuditLog.action == "LOGIN",
                func.date(AuditLog.created_at) == today,
            )
            .scalar()
        )


        today_user_changes = (
            db.query(func.count(AuditLog.id))
            .filter(
                AuditLog.action.in_(
                    [
                        "CREATE_USER",
                        "UPDATE_USER",
                        "DELETE_USER",
                    ]
                ),
                func.date(AuditLog.created_at) == today,
            )
            .scalar()
        )


        return {

            # Basic Dashboard

            "total_users": total_users,

            "total_provinces": total_provinces,

            "total_cities": total_cities,


            # Audit Dashboard

            "total_audit_logs": total_audit_logs,

            "today_login": today_login,

            "today_user_changes": today_user_changes,

        }