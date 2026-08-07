from app.models.user import User
from app.models.province import Province
from app.models.city import City
from app.models.role import Role
from app.models.permission import Permission
from app.models.role_permission import RolePermission
from app.models.audit_log import AuditLog
from app.models.user_session import UserSession

from app.models.competition import Competition
from app.models.competition_group import CompetitionGroup
from app.models.competition_category import (
    CompetitionCategory,
)
from app.models.competition_round import (
    CompetitionRound,
)
from app.models.competition_round_entry import (
    CompetitionRoundEntry,
)
from app.models.competition_round_judge import (
    CompetitionRoundJudge,
)
from app.models.competition_judge_score import (
    CompetitionJudgeScore,
)
from app.models.competition_scoring_criterion import (
    CompetitionScoringCriterion,
)
from app.models.competition_judge_score_detail import (
    CompetitionJudgeScoreDetail,
)
from app.models.competition_result import (
    CompetitionResult,
)
from app.models.competition_result_publication import (
    CompetitionResultPublication,
)
from app.models.competition_registration import (
    CompetitionRegistration,
)

from app.models.chinese_surname import ChineseSurname
from app.models.chinese_surname_alias import (
    ChineseSurnameAlias,
)
from app.models.ethnicity import Ethnicity
from app.models.participant import Participant


__all__ = [
    "User",
    "Province",
    "City",
    "Role",
    "Permission",
    "RolePermission",
    "AuditLog",
    "UserSession",

    "Competition",
    "CompetitionGroup",
    "CompetitionCategory",
    "CompetitionRound",
    "CompetitionRoundEntry",
    "CompetitionRoundJudge",
    "CompetitionJudgeScore",
    "CompetitionScoringCriterion",
    "CompetitionJudgeScoreDetail",
    "CompetitionResult",
    "CompetitionResultPublication",
    "CompetitionRegistration",

    "ChineseSurname",
    "ChineseSurnameAlias",
    "Ethnicity",
    "Participant",
]