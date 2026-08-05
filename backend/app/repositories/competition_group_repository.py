from sqlalchemy.orm import Session

from app.models.competition_group import (
    CompetitionGroup,
)


class CompetitionGroupRepository:

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
            .query(CompetitionGroup)
            .order_by(
                CompetitionGroup.competition_id,
                CompetitionGroup.sort_order,
                CompetitionGroup.id,
            )
            .all()
        )

    def get_by_competition(
        self,
        competition_id: int,
    ):
        return (
            self.db
            .query(CompetitionGroup)
            .filter(
                CompetitionGroup.competition_id
                == competition_id
            )
            .order_by(
                CompetitionGroup.sort_order,
                CompetitionGroup.id,
            )
            .all()
        )

    def get_by_id(
        self,
        group_id: int,
    ):
        return (
            self.db
            .query(CompetitionGroup)
            .filter(
                CompetitionGroup.id
                == group_id
            )
            .first()
        )

    def get_by_code(
        self,
        competition_id: int,
        code: str,
    ):
        return (
            self.db
            .query(CompetitionGroup)
            .filter(
                CompetitionGroup.competition_id
                == competition_id,
                CompetitionGroup.code
                == code,
            )
            .first()
        )

    # ======================================================
    # CREATE
    # ======================================================

    def create(
        self,
        group: CompetitionGroup,
    ):
        self.db.add(group)
        self.db.commit()
        self.db.refresh(group)

        return group

    # ======================================================
    # UPDATE
    # ======================================================

    def update(
        self,
        group: CompetitionGroup,
        code: str,
        name: str,
        min_age: int | None,
        max_age: int | None,
        sort_order: int,
        is_active: bool,
    ):
        group.code = code
        group.name = name

        group.min_age = min_age
        group.max_age = max_age

        group.sort_order = sort_order
        group.is_active = is_active

        self.db.commit()
        self.db.refresh(group)

        return group

    # ======================================================
    # DELETE
    # ======================================================

    def delete(
        self,
        group: CompetitionGroup,
    ):
        self.db.delete(group)
        self.db.commit()

        return True