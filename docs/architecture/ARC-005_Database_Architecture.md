# ARC-005 — Database Architecture

**Document ID:** ARC-005
**Project:** MAJE Platform
**Category:** Architecture
**Status:** Approved
**Version:** 1.0
**Owner:** Engineering Team
**Last Updated:** 2026-07-20

---

# 1. Purpose

Dokumen ini mendefinisikan arsitektur database MAJE Platform.

Database menjadi sumber data utama (System of Record) yang mendukung seluruh layanan aplikasi.

---

# 2. Objectives

Tujuan arsitektur database:

- menjaga integritas data
- mendukung performa tinggi
- memudahkan pengembangan
- mendukung skalabilitas
- menjaga keamanan data

---

# 3. Technology Stack

| Component | Technology |
|-----------|------------|
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migration | Alembic |
| Driver | psycopg |

---

# 4. Database Principles

MAJE menerapkan prinsip:

- Normalize First
- Secure by Default
- ACID Compliance
- Explicit Relationships
- Versioned Migration

---

# 5. High-Level Structure

```
Application
      │
      ▼
Repository Layer
      │
      ▼
SQLAlchemy ORM
      │
      ▼
PostgreSQL
```

---

# 6. Core Domains

Database dibagi menjadi beberapa domain utama:

- Authentication
- User Management
- Organization
- AI
- Audit
- Configuration
- Master Data

---

# 7. Naming Convention

## Table

snake_case

Contoh:

users

roles

permissions

audit_logs

---

## Column

snake_case

Contoh:

created_at

updated_at

is_active

---

## Primary Key

id

---

## Foreign Key

<nama_tabel>_id

Contoh:

user_id

role_id

---

# 8. Common Columns

Seluruh tabel memiliki:

id

created_at

updated_at

created_by

updated_by

is_active

---

# 9. Relationship Rules

Relationship menggunakan:

- One-to-One
- One-to-Many
- Many-to-Many

Foreign key wajib memiliki constraint yang jelas.

---

# 10. Migration

Perubahan database wajib melalui Alembic.

Migration tidak boleh dilakukan secara manual di Production.

---

# 11. Indexing

Index dibuat untuk:

- Primary Key
- Foreign Key
- Frequently Queried Columns
- Unique Constraints

---

# 12. Security

Database menerapkan:

- Least Privilege
- Role-Based Access
- Connection Encryption
- Audit Trail

---

# 13. Backup Strategy

Backup terdiri dari:

- Daily Backup
- Weekly Full Backup
- Restore Testing

---

# 14. Data Lifecycle

Tahapan data:

Create

↓

Read

↓

Update

↓

Archive / Delete

---

# 15. Audit

Perubahan data penting harus dicatat:

- user
- waktu
- perubahan
- sumber perubahan

---

# 16. Future Roadmap

Tahap berikutnya:

- Read Replica
- Partitioning
- Data Warehouse
- Vector Database untuk AI
- Data Retention Policy

---

# 17. Document History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-20 | Initial Database Architecture |