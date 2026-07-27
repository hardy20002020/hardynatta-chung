from app.db.database import SessionLocal

from app.db.seed_roles import seed_roles
from app.db.seed_permissions import (
    seed_permissions,
    seed_role_permissions,
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

        print("Done.")

    finally:
        db.close()


if __name__ == "__main__":
    main()