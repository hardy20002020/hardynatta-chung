from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog



class AuditLogRepository:


    # ==================================================
    # CREATE AUDIT LOG
    # ==================================================

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



    # ==================================================
    # GET ALL (LEGACY)
    # ==================================================

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[AuditLog]:


        return (
            db.query(AuditLog)
            .order_by(
                AuditLog.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )



    # ==================================================
    # GET BY USER
    # ==================================================

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



    # ==================================================
    # ENTERPRISE FILTER QUERY
    # ==================================================

    def get_filtered(
        self,
        db: Session,
        *,
        page: int = 1,
        size: int = 10,
        user_id: int | None = None,
        action: str | None = None,
    ):


        query = db.query(AuditLog)


        if user_id is not None:

            query = query.filter(
                AuditLog.user_id == user_id
            )


        if action is not None:

            query = query.filter(
                AuditLog.action == action
            )


        total = query.count()


        items = (
            query
            .order_by(
                AuditLog.created_at.desc()
            )
            .offset(
                (page - 1) * size
            )
            .limit(size)
            .all()
        )


        return {
            "items": items,
            "total": total,
            "page": page,
            "size": size,
        }