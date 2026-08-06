from sqlalchemy.orm import Session

from app.models.competition_scoring_criterion import (
    CompetitionScoringCriterion,
)


class CompetitionScoringCriterionRepository:

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
            .query(CompetitionScoringCriterion)
            .order_by(
                CompetitionScoringCriterion.competition_round_id,
                CompetitionScoringCriterion.sort_order,
                CompetitionScoringCriterion.id,
            )
            .all()
        )

    def get_by_id(
        self,
        criterion_id: int,
    ):
        return (
            self.db
            .query(CompetitionScoringCriterion)
            .filter(
                CompetitionScoringCriterion.id
                == criterion_id
            )
            .first()
        )

    def get_by_round(
        self,
        competition_round_id: int,
    ):
        return (
            self.db
            .query(CompetitionScoringCriterion)
            .filter(
                CompetitionScoringCriterion.competition_round_id
                == competition_round_id
            )
            .order_by(
                CompetitionScoringCriterion.sort_order,
                CompetitionScoringCriterion.id,
            )
            .all()
        )

    def get_by_round_code(
        self,
        competition_round_id: int,
        code: str,
    ):
        return (
            self.db
            .query(CompetitionScoringCriterion)
            .filter(
                CompetitionScoringCriterion.competition_round_id
                == competition_round_id,
                CompetitionScoringCriterion.code
                == code,
            )
            .first()
        )

    # ======================================================
    # CREATE
    # ======================================================

    def create(
        self,
        criterion: CompetitionScoringCriterion,
    ):
        self.db.add(
            criterion
        )

        self.db.commit()
        self.db.refresh(
            criterion
        )

        return criterion

    # ======================================================
    # UPDATE
    # ======================================================

    def update(
        self,
        criterion: CompetitionScoringCriterion,
        *,
        code: str,
        name: str,
        description: str | None,
        weight,
        min_score,
        max_score,
        sort_order: int,
        is_active: bool,
    ):
        criterion.code = code
        criterion.name = name
        criterion.description = description
        criterion.weight = weight
        criterion.min_score = min_score
        criterion.max_score = max_score
        criterion.sort_order = sort_order
        criterion.is_active = is_active

        self.db.commit()
        self.db.refresh(
            criterion
        )

        return criterion

    # ======================================================
    # DELETE
    # ======================================================

    def delete(
        self,
        criterion: CompetitionScoringCriterion,
    ):
        self.db.delete(
            criterion
        )

        self.db.commit()

        return True