from sqlalchemy.orm import Session

from app.models.city import City


class CityService:

    @staticmethod
    def get_all(db: Session):
        return db.query(City).all()

    @staticmethod
    def get_by_id(
        db: Session,
        city_id: int,
    ):
        return (
            db.query(City)
            .filter(City.id == city_id)
            .first()
        )

    @staticmethod
    def create(
        db: Session,
        name: str,
        province_id: int,
    ):
        city = City(
            name=name,
            province_id=province_id,
        )

        db.add(city)
        db.commit()
        db.refresh(city)

        return city

    @staticmethod
    def update(
        db: Session,
        city_id: int,
        name: str,
        province_id: int,
    ):
        city = (
            db.query(City)
            .filter(City.id == city_id)
            .first()
        )

        if city:
            city.name = name
            city.province_id = province_id

            db.commit()
            db.refresh(city)

        return city

    @staticmethod
    def delete(
        db: Session,
        city_id: int,
    ):
        city = (
            db.query(City)
            .filter(City.id == city_id)
            .first()
        )

        if city:
            db.delete(city)
            db.commit()

        return city