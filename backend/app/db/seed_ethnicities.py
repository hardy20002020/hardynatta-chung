from sqlalchemy.orm import Session

from app.models.ethnicity import Ethnicity


ETHNICITIES = [
    {
        "code": "HAKKA",
        "name": "Hakka",
        "chinese_name": "客家",
        "sort_order": 1,
        "is_other": False,
    },
    {
        "code": "TEOCHEW",
        "name": "Teochew",
        "chinese_name": "潮州",
        "sort_order": 2,
        "is_other": False,
    },
    {
        "code": "CANTONESE",
        "name": "Cantonese / Konghu",
        "chinese_name": "广府",
        "sort_order": 3,
        "is_other": False,
    },
    {
        "code": "HAINAN",
        "name": "Hainan",
        "chinese_name": "海南",
        "sort_order": 4,
        "is_other": False,
    },
    {
        "code": "HOKKIEN",
        "name": "Hokkien",
        "chinese_name": "福建",
        "sort_order": 5,
        "is_other": False,
    },
    {
        "code": "OTHER",
        "name": "Lainnya",
        "chinese_name": None,
        "sort_order": 99,
        "is_other": True,
    },
]


def seed_ethnicities(
    db: Session,
) -> None:
    """
    Seed MAJE participant ethnicity master data.

    This operation is idempotent.

    Existing records are synchronized using
    the stable ethnicity code.
    """

    for data in ETHNICITIES:
        ethnicity = (
            db.query(Ethnicity)
            .filter(
                Ethnicity.code == data["code"]
            )
            .first()
        )

        if ethnicity is None:
            ethnicity = Ethnicity(
                code=data["code"],
                name=data["name"],
                chinese_name=(
                    data["chinese_name"]
                ),
                sort_order=data["sort_order"],
                is_other=data["is_other"],
                is_active=True,
            )

            db.add(ethnicity)

        else:
            ethnicity.name = data["name"]
            ethnicity.chinese_name = (
                data["chinese_name"]
            )
            ethnicity.sort_order = (
                data["sort_order"]
            )
            ethnicity.is_other = (
                data["is_other"]
            )

    db.commit()