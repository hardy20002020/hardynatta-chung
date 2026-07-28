from sqlalchemy.orm import Session

from app.models.province import Province


class ProvinceService:

    @staticmethod
    def get_all(db: Session):
        return db.query(Province).all()

    @staticmethod
    def get_by_id(
        db: Session,
        province_id: int,
    ):
        return (
            db.query(Province)
            .filter(Province.id == province_id)
            .first()
        )

    @staticmethod
    def create(
        db: Session,
        name: str,
    ):
        province = Province(name=name)

        db.add(province)
        db.commit()
        db.refresh(province)

        return province

    @staticmethod
    def update(
        db: Session,
        province_id: int,
        name: str,
    ):
        province = (
            db.query(Province)
            .filter(Province.id == province_id)
            .first()
        )

        if not province:
            return None

        province.name = name

        db.commit()
        db.refresh(province)

        return province

    @staticmethod
    def delete(
        db: Session,
        province_id: int,
    ):
        province = (
            db.query(Province)
            .filter(Province.id == province_id)
            .first()
        )

        if not province:
            return None

        db.delete(province)
        db.commit()

        return province