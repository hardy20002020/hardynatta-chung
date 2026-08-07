from sqlalchemy.orm import Session

from app.models.competition_judge_score_detail import (
    CompetitionJudgeScoreDetail,
)

from app.repositories.competition_judge_score_detail_repository import (
    CompetitionJudgeScoreDetailRepository,
)

from app.repositories.competition_judge_score_repository import (
    CompetitionJudgeScoreRepository,
)

from app.repositories.competition_scoring_criterion_repository import (
    CompetitionScoringCriterionRepository,
)

from app.schemas.competition_judge_score_detail import (
    CompetitionJudgeScoreDetailCreate,
    CompetitionJudgeScoreDetailUpdate,
)


class CompetitionJudgeScoreDetailService:

    def __init__(
        self,
        db: Session,
    ):

        self.repository = (
            CompetitionJudgeScoreDetailRepository(
                db
            )
        )

        self.score_repository = (
            CompetitionJudgeScoreRepository(
                db
            )
        )

        self.criterion_repository = (
            CompetitionScoringCriterionRepository(
                db
            )
        )

    # ======================================================
    # EDITABILITY
    # ======================================================

    def ensure_score_editable(
        self,
        judge_score,
    ):

        if judge_score.status != "draft":

            raise ValueError(
                "Submitted or locked score cannot be modified"
            )

    # ======================================================
    # READ
    # ======================================================

    def get_details(
        self,
        competition_judge_score_id: int | None = None,
        competition_scoring_criterion_id: int | None = None,
    ):

        if (
            competition_judge_score_id is not None
            and competition_scoring_criterion_id is not None
        ):
            detail = (
                self.repository.get_by_score_criterion(
                    competition_judge_score_id,
                    competition_scoring_criterion_id,
                )
            )

            if detail is None:
                return []

            return [detail]

        if competition_judge_score_id is not None:
            return self.repository.get_by_judge_score(
                competition_judge_score_id
            )

        if competition_scoring_criterion_id is not None:
            return self.repository.get_by_criterion(
                competition_scoring_criterion_id
            )

        return self.repository.get_all()

    def get_detail_by_id(
        self,
        detail_id: int,
    ):

        return self.repository.get_by_id(
            detail_id
        )

    # ======================================================
    # CALCULATION
    # ======================================================

    def calculate_weighted_score(
        self,
        score,
        weight,
    ):

        return score * weight

    def refresh_total_score(
        self,
        competition_judge_score_id: int,
    ):

        judge_score = (
            self.score_repository.get_by_id(
                competition_judge_score_id
            )
        )

        if judge_score is None:

            return None

        total_score = (
            self.score_repository.calculate_total_score(
                competition_judge_score_id
            )
        )

        self.score_repository.update(
            judge_score,
            total_score=total_score,
            status=judge_score.status,
            notes=judge_score.notes,
            submitted_at=judge_score.submitted_at,
        )

        return total_score

    # ======================================================
    # CREATE
    # ======================================================

    def create_detail(
        self,
        data: CompetitionJudgeScoreDetailCreate,
    ):

        judge_score = (
            self.score_repository.get_by_id(
                data.competition_judge_score_id
            )
        )

        if judge_score is None:

            raise ValueError(
                "Competition judge score not found"
            )

        self.ensure_score_editable(
            judge_score
        )

        criterion = (
            self.criterion_repository.get_by_id(
                data.competition_scoring_criterion_id
            )
        )

        if criterion is None:

            raise ValueError(
                "Competition scoring criterion not found"
            )

        existing = (
            self.repository.get_by_score_criterion(
                data.competition_judge_score_id,
                data.competition_scoring_criterion_id,
            )
        )

        if existing:

            raise ValueError(
                "Score detail already exists"
            )

        weighted_score = (
            self.calculate_weighted_score(
                data.score,
                criterion.weight,
            )
        )

        detail = CompetitionJudgeScoreDetail(

            competition_judge_score_id=(
                data.competition_judge_score_id
            ),

            competition_scoring_criterion_id=(
                data.competition_scoring_criterion_id
            ),

            score=data.score,

            weighted_score=weighted_score,

            source=data.source,

            notes=data.notes,

        )

        result = (
            self.repository.create(
                detail
            )
        )

        # ==================================================
        # AUTO AGGREGATE PARENT SCORE
        # ==================================================

        self.refresh_total_score(
            data.competition_judge_score_id
        )

        return result

    # ======================================================
    # UPDATE
    # ======================================================

    def update_detail(
        self,
        detail_id: int,
        data: CompetitionJudgeScoreDetailUpdate,
    ):

        detail = (
            self.repository.get_by_id(
                detail_id
            )
        )

        if detail is None:

            return None

        judge_score = (
            self.score_repository.get_by_id(
                detail.competition_judge_score_id
            )
        )

        if judge_score is None:

            raise ValueError(
                "Competition judge score not found"
            )

        self.ensure_score_editable(
            judge_score
        )

        if data.score is not None:

            criterion = (
                self.criterion_repository.get_by_id(
                    detail.competition_scoring_criterion_id
                )
            )

            if criterion is None:

                raise ValueError(
                    "Competition scoring criterion not found"
                )

            detail.score = data.score

            detail.weighted_score = (
                self.calculate_weighted_score(
                    data.score,
                    criterion.weight,
                )
            )

        if data.source is not None:

            detail.source = data.source

        if data.notes is not None:

            detail.notes = data.notes

        self.repository.db.commit()

        self.repository.db.refresh(
            detail
        )

        self.refresh_total_score(
            detail.competition_judge_score_id
        )

        return detail

    # ======================================================
    # DELETE
    # ======================================================

    def delete_detail(
        self,
        detail_id: int,
    ):

        detail = (
            self.repository.get_by_id(
                detail_id
            )
        )

        if detail is None:

            return False

        score_id = (
            detail.competition_judge_score_id
        )

        judge_score = (
            self.score_repository.get_by_id(
                score_id
            )
        )

        if judge_score is None:

            raise ValueError(
                "Competition judge score not found"
            )

        self.ensure_score_editable(
            judge_score
        )

        result = (
            self.repository.delete(
                detail
            )
        )

        self.refresh_total_score(
            score_id
        )

        return result
