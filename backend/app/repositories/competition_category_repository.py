from sqlalchemy.orm import Session

from app.models.competition_category import (
    CompetitionCategory,
)


class CompetitionCategoryRepository:

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
            .query(CompetitionCategory)
            .order_by(
                CompetitionCategory.competition_id,
                CompetitionCategory.sort_order,
                CompetitionCategory.id,
            )
            .all()
        )

    def get_by_competition(
        self,
        competition_id: int,
    ):
        return (
            self.db
            .query(CompetitionCategory)
            .filter(
                CompetitionCategory.competition_id
                == competition_id
            )
            .order_by(
                CompetitionCategory.sort_order,
                CompetitionCategory.id,
            )
            .all()
        )

    def get_by_id(
        self,
        category_id: int,
    ):
        return (
            self.db
            .query(CompetitionCategory)
            .filter(
                CompetitionCategory.id
                == category_id
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
            .query(CompetitionCategory)
            .filter(
                CompetitionCategory.competition_id
                == competition_id,
                CompetitionCategory.code
                == code,
            )
            .first()
        )

    # ======================================================
    # CREATE
    # ======================================================

    def create(
        self,
        category: CompetitionCategory,
    ):
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)

        return category

    # ======================================================
    # UPDATE
    # ======================================================

    def update(
        self,
        category: CompetitionCategory,
        code: str,
        name: str,
        description: str | None,
        sort_order: int,
        is_active: bool,
    ):
        category.code = code
        category.name = name
        category.description = description
        category.sort_order = sort_order
        category.is_active = is_active

        self.db.commit()
        self.db.refresh(category)

        return category

    # ======================================================
    # DELETE
    # ======================================================

    def delete(
        self,
        category: CompetitionCategory,
    ):
        self.db.delete(category)
        self.db.commit()

        return True