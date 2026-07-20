# ARC-002 — Backend Architecture

**Document ID:** ARC-002
**Project:** MAJE Platform
**Category:** Architecture
**Status:** Approved
**Version:** 1.0
**Owner:** Engineering Team
**Last Updated:** 2026-07-20

---

# 1. Purpose

Dokumen ini mendefinisikan arsitektur backend MAJE Platform.

Backend bertanggung jawab untuk:

- Business Logic
- REST API
- Authentication
- Authorization
- Database Access
- AI Integration
- Background Processing

---

# 2. Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.13+ |
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Migration | Alembic |
| Validation | Pydantic |
| Authentication | JWT |
| Database | PostgreSQL |
| Cache | Redis (planned) |
| Background Jobs | Celery (planned) |

---

# 3. Backend Architecture

```
                REST API
                    │
        ┌───────────▼───────────┐
        │       API Layer       │
        └───────────┬───────────┘
                    │
        ┌───────────▼───────────┐
        │     Service Layer     │
        └───────────┬───────────┘
                    │
        ┌───────────▼───────────┐
        │   Repository Layer    │
        └───────────┬───────────┘
                    │
        ┌───────────▼───────────┐
        │      PostgreSQL       │
        └───────────────────────┘
```

---

# 4. Project Structure

```
backend/

app/
├── api/
├── core/
├── db/
├── models/
├── repositories/
├── schemas/
├── services/
├── middleware/
├── exceptions/
├── utils/
├── dependencies/
└── main.py
```

---

# 5. Layer Responsibilities

## API Layer

- menerima request
- validasi input
- mengembalikan response

## Service Layer

- business logic
- workflow aplikasi

## Repository Layer

- akses database
- query
- transaksi

## Database Layer

- PostgreSQL
- migration
- indexing

---

# 6. Design Principles

- Single Responsibility
- Dependency Injection
- Loose Coupling
- High Cohesion
- Clean Architecture

---

# 7. API Versioning

Semua endpoint menggunakan format:

```
/api/v1/
```

Contoh:

```
/api/v1/auth
/api/v1/users
/api/v1/roles
```

---

# 8. Error Handling

Standar:

- exception terpusat
- response konsisten
- logging otomatis

---

# 9. Security

Backend wajib menerapkan:

- JWT Authentication
- RBAC
- Input Validation
- Rate Limiting (planned)
- Audit Logging

---

# 10. Integration

Backend berkomunikasi dengan:

- Frontend
- AI Service
- PostgreSQL
- Monitoring Service

---

# 11. Coding Standards

Seluruh implementasi backend wajib mengikuti:

- HC-003 Coding Standard
- HC-004 API Governance
- HC-005 Database Governance
- HC-006 Security Governance

---

# 12. Document History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-20 | Initial Backend Architecture |