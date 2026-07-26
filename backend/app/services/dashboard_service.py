from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.province import Province
from app.models.city import City


class DashboardService:

    @staticmethod
    def get_dashboard(db: Session):
        return {
            "total_users": db.query(func.count(User.id)).scalar(),
            "total_provinces": db.query(func.count(Province.id)).scalar(),
            "total_cities": db.query(func.count(City.id)).scalar(),
        }
