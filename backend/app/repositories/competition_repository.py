from datetime import date

from sqlalchemy.orm import Session

from app.models.competition import Competition


class CompetitionRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # ======================================================
    # READ
    # ======================================================

    def get_all(self):
        return (
            self.db
            .query(Competition)
            .order_by(
                Competition.year.desc(),
                Competition.id.desc(),
            )
            .all()
        )

    def get_by_id(
        self,
        competition_id: int,
    ):
        return (
            self.db
            .query(Competition)
            .filter(
                Competition.id
                == competition_id
            )
            .first()
        )

    def get_by_code(
        self,
        code: str,
    ):
        return (
            self.db
            .query(Competition)
            .filter(
                Competition.code
                == code
            )
            .first()
        )

    # ======================================================
    # CREATE
    # ======================================================

    def create(
        self,
        competition: Competition,
    ):
        self.db.add(competition)
        self.db.commit()
        self.db.refresh(competition)

        return competition

    # ======================================================
    # UPDATE
    # ======================================================

    def update(
        self,
        competition: Competition,
        name: str,
        code: str,
        year: int,
        age_reference_date: date | None,
        is_active: bool,
    ):
        competition.name = name
        competition.code = code
        competition.year = year

        competition.age_reference_date = (
            age_reference_date
        )

        competition.is_active = is_active

        self.db.commit()
        self.db.refresh(competition)

        return competition

    # ======================================================
    # DELETE
    # ======================================================

    def delete(
        self,
        competition: Competition,
    ):
        self.db.delete(competition)
        self.db.commit()

        return True