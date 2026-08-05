from sqlalchemy.orm import Session

from app.models.competition_group import (
    CompetitionGroup,
)
from app.repositories.competition_group_repository import (
    CompetitionGroupRepository,
)
from app.repositories.competition_repository import (
    CompetitionRepository,
)
from app.schemas.competition_group import (
    CompetitionGroupCreate,
    CompetitionGroupUpdate,
)


class CompetitionGroupService:

    def __init__(
        self,
        db: Session,
    ):
        self.repository = (
            CompetitionGroupRepository(db)
        )

        self.competition_repository = (
            CompetitionRepository(db)
        )

    # ======================================================
    # READ
    # ======================================================

    def get_groups(self):
        return self.repository.get_all()

    def get_groups_by_competition(
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

    def get_group_by_id(
        self,
        group_id: int,
    ):
        return self.repository.get_by_id(
            group_id
        )

    # ======================================================
    # AGE RANGE VALIDATION
    # ======================================================

    def _validate_age_range(
        self,
        min_age: int | None,
        max_age: int | None,
    ):
        if (
            min_age is not None
            and min_age < 0
        ):
            raise ValueError(
                "Minimum age cannot be negative"
            )

        if (
            max_age is not None
            and max_age < 0
        ):
            raise ValueError(
                "Maximum age cannot be negative"
            )

        if (
            min_age is not None
            and max_age is not None
            and min_age > max_age
        ):
            raise ValueError(
                "Minimum age cannot be greater "
                "than maximum age"
            )

    # ======================================================
    # CREATE
    # ======================================================

    def create_group(
        self,
        data: CompetitionGroupCreate,
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

        existing = self.repository.get_by_code(
            data.competition_id,
            data.code,
        )

        if existing:
            raise ValueError(
                "Competition group code "
                "already exists"
            )

        self._validate_age_range(
            data.min_age,
            data.max_age,
        )

        group = CompetitionGroup(
            competition_id=data.competition_id,
            code=data.code,
            name=data.name,
            min_age=data.min_age,
            max_age=data.max_age,
            sort_order=data.sort_order,
        )

        return self.repository.create(
            group
        )

    # ======================================================
    # UPDATE
    # ======================================================

    def update_group(
        self,
        group_id: int,
        data: CompetitionGroupUpdate,
    ):
        group = self.repository.get_by_id(
            group_id
        )

        if group is None:
            return None

        existing = self.repository.get_by_code(
            group.competition_id,
            data.code,
        )

        if (
            existing
            and existing.id != group_id
        ):
            raise ValueError(
                "Competition group code "
                "already exists"
            )

        self._validate_age_range(
            data.min_age,
            data.max_age,
        )

        return self.repository.update(
            group=group,
            code=data.code,
            name=data.name,
            min_age=data.min_age,
            max_age=data.max_age,
            sort_order=data.sort_order,
            is_active=data.is_active,
        )

    # ======================================================
    # DELETE
    # ======================================================

    def delete_group(
        self,
        group_id: int,
    ):
        group = self.repository.get_by_id(
            group_id
        )

        if group is None:
            return False

        return self.repository.delete(
            group
        )