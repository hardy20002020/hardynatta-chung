from app.db.database import SessionLocal

from app.db.seed_roles import seed_roles
from app.db.seed_permissions import (
    seed_permissions,
    seed_role_permissions,
)
from app.db.seed_ethnicities import (
    seed_ethnicities,
)
from app.db.seed_chinese_surnames import (
    seed_chinese_surnames,
)
from app.db.seed_chinese_surname_aliases import (
    seed_chinese_surname_aliases,
)


def main():
    db = SessionLocal()

    try:
        print("Seeding roles...")
        seed_roles(db)

        print("Seeding permissions...")
        seed_permissions(db)

        print("Seeding role permissions...")
        seed_role_permissions(db)

        print("Seeding ethnicities...")
        seed_ethnicities(db)

        print("Seeding Chinese surnames...")
        seed_chinese_surnames(db)

        print("Seeding Chinese surname aliases...")
        seed_chinese_surname_aliases(db)

        print("Done.")

    finally:
        db.close()


if __name__ == "__main__":
    main()