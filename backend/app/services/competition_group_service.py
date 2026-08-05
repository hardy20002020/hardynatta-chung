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

        group = CompetitionGroup(
            competition_id=data.competition_id,
            code=data.code,
            name=data.name,
            sort_order=data.sort_order,
        )

        return self.repository.create(
            group
        )


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

        return self.repository.update(
            group,
            data.code,
            data.name,
            data.sort_order,
            data.is_active,
        )


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