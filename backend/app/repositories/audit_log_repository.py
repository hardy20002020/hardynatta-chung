from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


class AuditLogRepository:

    def create(
        self,
        db: Session,
        *,
        user_id: int | None,
        action: str,
        resource: str,
        description: str | None = None,
    ) -> AuditLog:

        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            resource=resource,
            description=description,
        )

        db.add(audit_log)
        db.commit()
        db.refresh(audit_log)

        return audit_log


    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[AuditLog]:

        return (
            db.query(AuditLog)
            .offset(skip)
            .limit(limit)
            .all()
        )


    def get_by_user(
        self,
        db: Session,
        user_id: int,
    ) -> list[AuditLog]:

        return (
            db.query(AuditLog)
            .filter(
                AuditLog.user_id == user_id
            )
            .order_by(
                AuditLog.created_at.desc()
            )
            .all()
        )