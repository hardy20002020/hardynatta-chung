from sqlalchemy.orm import Session

from app.models.chinese_surname import (
    ChineseSurname,
)


CHINESE_SURNAMES = [
    {
        "chinese_character": "陈",
        "pinyin": "Chen",
        "local_name": "Tan",
        "sort_order": 1,
    },
    {
        "chinese_character": "林",
        "pinyin": "Lin",
        "local_name": "Lim",
        "sort_order": 2,
    },
    {
        "chinese_character": "黄",
        "pinyin": "Huang",
        "local_name": "Oei / Ng",
        "sort_order": 3,
    },
    {
        "chinese_character": "李",
        "pinyin": "Li",
        "local_name": "Lie / Lee",
        "sort_order": 4,
    },
    {
        "chinese_character": "王",
        "pinyin": "Wang",
        "local_name": "Ong",
        "sort_order": 5,
    },
    {
        "chinese_character": "张",
        "pinyin": "Zhang",
        "local_name": "Tjong / Chang",
        "sort_order": 6,
    },
    {
        "chinese_character": "刘",
        "pinyin": "Liu",
        "local_name": "Lauw / Lioe",
        "sort_order": 7,
    },
    {
        "chinese_character": "吴",
        "pinyin": "Wu",
        "local_name": "Go / Goh",
        "sort_order": 8,
    },
    {
        "chinese_character": "郑",
        "pinyin": "Zheng",
        "local_name": "Tay / Tee",
        "sort_order": 9,
    },
    {
        "chinese_character": "鍾",
        "pinyin": "Zhong",
        "local_name": "Chung / Tjung",
        "sort_order": 10,
    },
]


def seed_chinese_surnames(
    db: Session,
) -> None:
    """
    Seed MAJE Chinese surname master data.

    This operation is idempotent.

    Chinese surnames use a canonical character
    as the master record.

    Character variants are stored separately
    in chinese_surname_aliases.
    """

    for data in CHINESE_SURNAMES:
        canonical_character = (
            data["chinese_character"]
        )

        surname = (
            db.query(ChineseSurname)
            .filter(
                ChineseSurname.chinese_character
                == canonical_character
            )
            .first()
        )

        # ==================================================
        # LEGACY ZHONG / CHUNG COMPATIBILITY
        # ==================================================
        #
        # Older MAJE data used 钟 as the canonical
        # character for Zhong / Chung.
        #
        # Preserve the existing database record and ID,
        # but migrate its canonical character to 鍾.
        #
        # This prevents duplicate Zhong surname records.
        # ==================================================

        if (
            surname is None
            and canonical_character == "鍾"
        ):
            surname = (
                db.query(ChineseSurname)
                .filter(
                    ChineseSurname.chinese_character
                    == "钟"
                )
                .first()
            )

            if surname is not None:
                surname.chinese_character = "鍾"

        if surname is None:
            surname = ChineseSurname(
                chinese_character=(
                    canonical_character
                ),
                pinyin=data["pinyin"],
                local_name=data["local_name"],
                sort_order=data["sort_order"],
                is_active=True,
            )

            db.add(surname)

        else:
            surname.pinyin = data["pinyin"]
            surname.local_name = (
                data["local_name"]
            )
            surname.sort_order = (
                data["sort_order"]
            )
            surname.is_active = True

    db.commit()