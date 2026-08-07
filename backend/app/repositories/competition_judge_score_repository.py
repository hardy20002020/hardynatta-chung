from sqlalchemy.orm import Session
from sqlalchemy import func


from app.models.competition_judge_score import (
    CompetitionJudgeScore,
)


from app.models.competition_judge_score_detail import (
    CompetitionJudgeScoreDetail,
)



class CompetitionJudgeScoreRepository:


    def __init__(
        self,
        db: Session,
    ):
        self.db = db



    # ======================================================
    # READ
    # ======================================================

    def get_all(
        self,
    ):

        return (
            self.db
            .query(
                CompetitionJudgeScore
            )
            .order_by(
                CompetitionJudgeScore.id
            )
            .all()
        )



    def get_by_id(
        self,
        score_id: int,
    ):

        return (
            self.db
            .query(
                CompetitionJudgeScore
            )
            .filter(
                CompetitionJudgeScore.id
                ==
                score_id
            )
            .first()
        )



    def get_by_entry(
        self,
        competition_round_entry_id: int,
    ):

        return (
            self.db
            .query(
                CompetitionJudgeScore
            )
            .filter(
                CompetitionJudgeScore
                .competition_round_entry_id
                ==
                competition_round_entry_id
            )
            .order_by(
                CompetitionJudgeScore.id
            )
            .all()
        )



    def get_by_judge(
        self,
        competition_round_judge_id: int,
    ):

        return (
            self.db
            .query(
                CompetitionJudgeScore
            )
            .filter(
                CompetitionJudgeScore
                .competition_round_judge_id
                ==
                competition_round_judge_id
            )
            .order_by(
                CompetitionJudgeScore.id
            )
            .all()
        )



    def get_by_entry_judge(
        self,
        competition_round_entry_id: int,
        competition_round_judge_id: int,
    ):

        return (
            self.db
            .query(
                CompetitionJudgeScore
            )
            .filter(
                CompetitionJudgeScore
                .competition_round_entry_id
                ==
                competition_round_entry_id,

                CompetitionJudgeScore
                .competition_round_judge_id
                ==
                competition_round_judge_id,
            )
            .first()
        )



    # ======================================================
    # CREATE
    # ======================================================

    def create(
        self,
        score: CompetitionJudgeScore,
    ):

        self.db.add(
            score
        )

        self.db.commit()

        self.db.refresh(
            score
        )

        return score



    # ======================================================
    # AGGREGATION ENGINE
    # ======================================================

    def calculate_total_score(
        self,
        competition_judge_score_id: int,
    ):

        result = (
            self.db
            .query(
                func.sum(
                    CompetitionJudgeScoreDetail
                    .weighted_score
                )
            )
            .filter(
                CompetitionJudgeScoreDetail
                .competition_judge_score_id
                ==
                competition_judge_score_id
            )
            .scalar()
        )


        if result is None:

            return 0


        return result



    # ======================================================
    # UPDATE
    # ======================================================

    def update(
        self,
        score: CompetitionJudgeScore,
        *,
        total_score,
        status,
        notes,
        submitted_at,
    ):

        score.total_score = total_score

        score.status = status

        score.notes = notes

        score.submitted_at = submitted_at


        self.db.commit()

        self.db.refresh(
            score
        )

        return score



    # ======================================================
    # DELETE
    # ======================================================

    def delete(
        self,
        score: CompetitionJudgeScore,
    ):

        self.db.delete(
            score
        )

        self.db.commit()

        return True