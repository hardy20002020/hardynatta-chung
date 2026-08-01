from sqlalchemy.orm import Session

from app.repositories.audit_log_repository import AuditLogRepository
from app.models.audit_log import AuditLog


class AuditLogService:

    def __init__(self):
        self.repository = AuditLogRepository()


    def create_log(
        self,
        db: Session,
        *,
        user_id: int | None,
        action: str,
        resource: str,
        description: str | None = None,
    ) -> AuditLog:

        return self.repository.create(
            db,
            user_id=user_id,
            action=action,
            resource=resource,
            description=description,
        )


    def get_logs(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[AuditLog]:

        return self.repository.get_all(
            db,
            skip=skip,
            limit=limit,
        )


    def get_user_logs(
        self,
        db: Session,
        user_id: int,
    ) -> list[AuditLog]:

        return self.repository.get_by_user(
            db,
            user_id=user_id,
        )