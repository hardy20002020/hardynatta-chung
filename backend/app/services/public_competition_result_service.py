from sqlalchemy.orm import (
    Session,
    joinedload,
)

from app.models.competition_result_publication import (
    CompetitionResultPublication,
)
from app.models.competition_round import (
    CompetitionRound,
)
from app.models.competition_round_entry import (
    CompetitionRoundEntry,
)
from app.models.competition_result import (
    CompetitionResult,
)
from app.models.competition_registration import (
    CompetitionRegistration,
)
from app.models.participant import (
    Participant,
)

from app.schemas.public_competition_result import (
    PublicCompetitionResultItem,
    PublicCompetitionRoundResultResponse,
)


class PublicCompetitionResultService:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # ======================================================
    # PUBLIC ROUND RESULT
    # ======================================================

    def get_published_round_result(
        self,
        competition_round_id: int,
    ) -> PublicCompetitionRoundResultResponse | None:

        publication = (
            self.db
            .query(CompetitionResultPublication)
            .options(
                joinedload(
                    CompetitionResultPublication
                    .competition_round
                ).joinedload(
                    CompetitionRound.competition
                )
            )
            .filter(
                CompetitionResultPublication
                .competition_round_id
                == competition_round_id,
                CompetitionResultPublication.status
                == "published",
            )
            .first()
        )

        if publication is None:
            return None

        competition_round = (
            publication.competition_round
        )

        competition = (
            competition_round.competition
        )

        results = (
            self.db
            .query(CompetitionResult)
            .join(
                CompetitionRoundEntry,
                CompetitionRoundEntry.id
                == CompetitionResult
                .competition_round_entry_id,
            )
            .options(
                joinedload(
                    CompetitionResult
                    .competition_round_entry
                )
                .joinedload(
                    CompetitionRoundEntry
                    .competition_registration
                )
                .joinedload(
                    CompetitionRegistration
                    .participant
                )
                .joinedload(
                    Participant.user
                ),

                joinedload(
                    CompetitionResult
                    .competition_round_entry
                )
                .joinedload(
                    CompetitionRoundEntry
                    .competition_registration
                )
                .joinedload(
                    CompetitionRegistration
                    .competition_group
                ),

                joinedload(
                    CompetitionResult
                    .competition_round_entry
                )
                .joinedload(
                    CompetitionRoundEntry
                    .competition_registration
                )
                .joinedload(
                    CompetitionRegistration
                    .competition_category
                ),
            )
            .filter(
                CompetitionRoundEntry
                .competition_round_id
                == competition_round_id,
                CompetitionResult.status
                == "finalized",
            )
            .order_by(
                CompetitionResult.rank,
                CompetitionResult.id,
            )
            .all()
        )

        public_results = []

        for result in results:

            entry = (
                result.competition_round_entry
            )

            registration = (
                entry.competition_registration
            )

            participant = (
                registration.participant
            )

            public_results.append(
                PublicCompetitionResultItem(
                    rank=result.rank,
                    final_score=result.final_score,
                    registration_number=(
                        registration
                        .registration_number
                    ),
                    participant_name=(
                        participant.user.name
                    ),
                    chinese_name=(
                        participant.chinese_name
                    ),
                    group_name=(
                        registration
                        .competition_group
                        .name
                    ),
                    category_name=(
                        registration
                        .competition_category
                        .name
                    ),
                )
            )

        return (
            PublicCompetitionRoundResultResponse(
                competition_id=competition.id,
                competition_name=competition.name,
                competition_code=competition.code,
                competition_year=competition.year,
                round_id=competition_round.id,
                round_code=competition_round.code,
                round_name=competition_round.name,
                published_at=publication.published_at,
                results=public_results,
            )
        )
