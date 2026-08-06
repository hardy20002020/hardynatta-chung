from sqlalchemy.orm import Session

from app.models.competition_round_judge import (
    CompetitionRoundJudge,
)


class CompetitionRoundJudgeRepository:

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
            self.db.query(
                CompetitionRoundJudge
            )
            .order_by(
                CompetitionRoundJudge.id
            )
            .all()
        )

    def get_by_id(
        self,
        judge_id: int,
    ):
        return (
            self.db.query(
                CompetitionRoundJudge
            )
            .filter(
                CompetitionRoundJudge.id
                == judge_id
            )
            .first()
        )

    def get_by_round(
        self,
        competition_round_id: int,
    ):
        return (
            self.db.query(
                CompetitionRoundJudge
            )
            .filter(
                CompetitionRoundJudge.competition_round_id
                == competition_round_id
            )
            .order_by(
                CompetitionRoundJudge.judge_order,
                CompetitionRoundJudge.id,
            )
            .all()
        )

    def get_by_user(
        self,
        user_id: int,
    ):
        return (
            self.db.query(
                CompetitionRoundJudge
            )
            .filter(
                CompetitionRoundJudge.user_id
                == user_id
            )
            .order_by(
                CompetitionRoundJudge.id
            )
            .all()
        )

    def get_by_round_user(
        self,
        competition_round_id: int,
        user_id: int,
    ):
        return (
            self.db.query(
                CompetitionRoundJudge
            )
            .filter(
                CompetitionRoundJudge.competition_round_id
                == competition_round_id,
                CompetitionRoundJudge.user_id
                == user_id,
            )
            .first()
        )

    # ======================================================
    # CREATE
    # ======================================================

    def create(
        self,
        judge: CompetitionRoundJudge,
    ):
        self.db.add(
            judge
        )

        self.db.commit()
        self.db.refresh(
            judge
        )

        return judge

    # ======================================================
    # UPDATE
    # ======================================================

    def update(
        self,
        judge: CompetitionRoundJudge,
        *,
        judge_order: int | None,
        status: str,
    ):
        judge.judge_order = judge_order
        judge.status = status

        self.db.commit()
        self.db.refresh(
            judge
        )

        return judge

    # ======================================================
    # DELETE
    # ======================================================

    def delete(
        self,
        judge: CompetitionRoundJudge,
    ):
        self.db.delete(
            judge
        )

        self.db.commit()

        return True