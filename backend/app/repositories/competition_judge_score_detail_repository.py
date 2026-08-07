from sqlalchemy.orm import Session

from app.models.competition_judge_score_detail import (
    CompetitionJudgeScoreDetail,
)


class CompetitionJudgeScoreDetailRepository:

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
            .query(CompetitionJudgeScoreDetail)
            .order_by(
                CompetitionJudgeScoreDetail.id
            )
            .all()
        )

    def get_by_id(
        self,
        detail_id: int,
    ):
        return (
            self.db
            .query(CompetitionJudgeScoreDetail)
            .filter(
                CompetitionJudgeScoreDetail.id
                == detail_id
            )
            .first()
        )

    def get_by_judge_score(
        self,
        competition_judge_score_id: int,
    ):
        return (
            self.db
            .query(CompetitionJudgeScoreDetail)
            .filter(
                CompetitionJudgeScoreDetail
                .competition_judge_score_id
                == competition_judge_score_id
            )
            .order_by(
                CompetitionJudgeScoreDetail.id
            )
            .all()
        )

    def get_by_criterion(
        self,
        competition_scoring_criterion_id: int,
    ):
        return (
            self.db
            .query(CompetitionJudgeScoreDetail)
            .filter(
                CompetitionJudgeScoreDetail
                .competition_scoring_criterion_id
                == competition_scoring_criterion_id
            )
            .order_by(
                CompetitionJudgeScoreDetail.id
            )
            .all()
        )

    def get_by_score_criterion(
        self,
        competition_judge_score_id: int,
        competition_scoring_criterion_id: int,
    ):
        return (
            self.db
            .query(CompetitionJudgeScoreDetail)
            .filter(
                CompetitionJudgeScoreDetail
                .competition_judge_score_id
                == competition_judge_score_id,
                CompetitionJudgeScoreDetail
                .competition_scoring_criterion_id
                == competition_scoring_criterion_id,
            )
            .first()
        )

    # ======================================================
    # CREATE
    # ======================================================

    def create(
        self,
        detail: CompetitionJudgeScoreDetail,
    ):
        self.db.add(detail)

        self.db.commit()
        self.db.refresh(detail)

        return detail

    # ======================================================
    # UPDATE
    # ======================================================

    def update(
        self,
        detail: CompetitionJudgeScoreDetail,
        *,
        score,
        weighted_score,
        source,
        notes,
    ):
        detail.score = score
        detail.weighted_score = weighted_score
        detail.source = source
        detail.notes = notes

        self.db.commit()
        self.db.refresh(detail)

        return detail

    # ======================================================
    # DELETE
    # ======================================================

    def delete(
        self,
        detail: CompetitionJudgeScoreDetail,
    ):
        self.db.delete(detail)

        self.db.commit()

        return True