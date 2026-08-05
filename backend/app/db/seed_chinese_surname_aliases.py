from sqlalchemy.orm import Session

from app.models.chinese_surname import (
    ChineseSurname,
)
from app.models.chinese_surname_alias import (
    ChineseSurnameAlias,
)


SURNAME_ALIASES = {
    "鍾": [
        {
            "character": "鍾",
            "variant_type": "TRADITIONAL",
            "is_primary": True,
        },
        {
            "character": "锺",
            "variant_type": "SIMPLIFIED_VARIANT",
            "is_primary": False,
        },
        {
            "character": "钟",
            "variant_type": "SIMPLIFIED",
            "is_primary": False,
        },
    ],
}


def seed_chinese_surname_aliases(
    db: Session,
) -> None:
    """
    Seed Chinese surname character aliases.

    Multiple written character variants can
    reference one canonical Chinese surname.

    This operation is idempotent.
    """

    for (
        canonical_character,
        aliases,
    ) in SURNAME_ALIASES.items():

        surname = (
            db.query(ChineseSurname)
            .filter(
                ChineseSurname.chinese_character
                == canonical_character
            )
            .first()
        )

        # --------------------------------------------------
        # Zhong / Chung migration compatibility
        # --------------------------------------------------

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
                surname.pinyin = "Zhong"
                surname.local_name = (
                    "Chung / Tjung"
                )

                db.flush()

        if surname is None:
            raise RuntimeError(
                "Canonical Chinese surname "
                f"'{canonical_character}' "
                "does not exist"
            )

        for data in aliases:
            alias = (
                db.query(ChineseSurnameAlias)
                .filter(
                    ChineseSurnameAlias.character
                    == data["character"]
                )
                .first()
            )

            if alias is None:
                alias = ChineseSurnameAlias(
                    chinese_surname_id=surname.id,
                    character=data["character"],
                    variant_type=(
                        data["variant_type"]
                    ),
                    is_primary=(
                        data["is_primary"]
                    ),
                    is_active=True,
                )

                db.add(alias)

            else:
                alias.chinese_surname_id = (
                    surname.id
                )
                alias.variant_type = (
                    data["variant_type"]
                )
                alias.is_primary = (
                    data["is_primary"]
                )
                alias.is_active = True

    db.commit()