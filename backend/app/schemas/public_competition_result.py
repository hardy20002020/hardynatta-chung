from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class PublicCompetitionResultItem(
    BaseModel
):
    rank: int

    final_score: Decimal

    registration_number: str

    participant_name: str

    chinese_name: str | None

    group_name: str

    category_name: str


class PublicCompetitionRoundResultResponse(
    BaseModel
):
    competition_id: int

    competition_name: str

    competition_code: str

    competition_year: int

    round_id: int

    round_code: str

    round_name: str

    published_at: datetime

    results: list[
        PublicCompetitionResultItem
    ]
