from sqlalchemy.orm import Session

from app.models.competition_category import (
    CompetitionCategory,
)
from app.repositories.competition_category_repository import (
    CompetitionCategoryRepository,
)
from app.repositories.competition_repository import (
    CompetitionRepository,
)
from app.schemas.competition_category import (
    CompetitionCategoryCreate,
    CompetitionCategoryUpdate,
)


class CompetitionCategoryService:

    def __init__(
        self,
        db: Session,
    ):
        self.repository = (
            CompetitionCategoryRepository(db)
        )

        self.competition_repository = (
            CompetitionRepository(db)
        )

    # ======================================================
    # READ
    # ======================================================

    def get_categories(
        self,
    ):
        return self.repository.get_all()

    def get_categories_by_competition(
        self,
        competition_id: int,
    ):
        competition = (
            self.competition_repository
            .get_by_id(
                competition_id
            )
        )

        if competition is None:
            return None

        return (
            self.repository
            .get_by_competition(
                competition_id
            )
        )

    def get_category_by_id(
        self,
        category_id: int,
    ):
        return self.repository.get_by_id(
            category_id
        )

    # ======================================================
    # CREATE
    # ======================================================

    def create_category(
        self,
        data: CompetitionCategoryCreate,
    ):
        competition = (
            self.competition_repository
            .get_by_id(
                data.competition_id
            )
        )

        if competition is None:
            raise ValueError(
                "Competition not found"
            )

        existing = (
            self.repository
            .get_by_code(
                data.competition_id,
                data.code,
            )
        )

        if existing is not None:
            raise ValueError(
                "Competition category code "
                "already exists"
            )

        category = CompetitionCategory(
            competition_id=data.competition_id,
            code=data.code,
            name=data.name,
            description=data.description,
            sort_order=data.sort_order,
            is_active=data.is_active,
        )

        return self.repository.create(
            category
        )

    # ======================================================
    # UPDATE
    # ======================================================

    def update_category(
        self,
        category_id: int,
        data: CompetitionCategoryUpdate,
    ):
        category = (
            self.repository.get_by_id(
                category_id
            )
        )

        if category is None:
            return None

        existing = (
            self.repository
            .get_by_code(
                category.competition_id,
                data.code,
            )
        )

        if (
            existing is not None
            and existing.id != category.id
        ):
            raise ValueError(
                "Competition category code "
                "already exists"
            )

        return self.repository.update(
            category,
            data.code,
            data.name,
            data.description,
            data.sort_order,
            data.is_active,
        )

    # ======================================================
    # DELETE
    # ======================================================

    def delete_category(
        self,
        category_id: int,
    ):
        category = (
            self.repository.get_by_id(
                category_id
            )
        )

        if category is None:
            return False

        return self.repository.delete(
            category
        )