# HC-005 — Database Governance

**Document ID:** HC-005  
**Project:** MAJE Platform  
**Category:** Engineering Documentation  
**Status:** Approved  
**Version:** 1.0  

---

# 1. Purpose

Dokumen ini mendefinisikan standar pengelolaan database MAJE Platform.

Database Governance memastikan:

- struktur data konsisten
- keamanan data terjaga
- perubahan schema terkendali
- performa database optimal

---

# 2. Database Principle

MAJE menggunakan prinsip:

- Data Integrity First
- Consistent Schema Design
- Migration Controlled
- Security by Default

---

# 3. Database Technology

Database utama:


PostgreSQL


ORM:


SQLAlchemy


Migration:


Alembic


---

# 4. Schema Organization

Struktur database:


Database

├── Core Schema
├── Application Schema
├── Audit Schema
└── Reference Schema


---

# 5. Table Naming Convention

Gunakan:


snake_case


dan bentuk plural.

Contoh:

Benar:


users
roles
transactions
payments


Tidak:


User
tbl_user
paymentData


---

# 6. Column Naming Convention

Gunakan:


snake_case


Contoh:

```sql
user_id
created_at
updated_at
is_active
7. Primary Key Standard

Setiap tabel wajib memiliki:

id

Format:

BIGSERIAL / UUID

Contoh:

id UUID PRIMARY KEY
8. Foreign Key Standard

Relasi menggunakan:

<table>_id

Contoh:

user_id
role_id
organization_id
9. Timestamp Standard

Setiap tabel utama wajib memiliki:

created_at
updated_at

Contoh:

created_at TIMESTAMP
updated_at TIMESTAMP
10. Migration Policy

Semua perubahan database wajib melalui migration.

Tidak diperbolehkan:

perubahan manual production database
menghapus migration lama
bypass migration process

Flow:

Create Migration
        ↓
Review
        ↓
Testing
        ↓
Deploy
11. Indexing Strategy

Index digunakan untuk:

kolom pencarian
foreign key
query dengan frekuensi tinggi

Contoh:

CREATE INDEX idx_users_email
ON users(email);
12. Data Integrity

Database wajib menggunakan:

primary key
foreign key
unique constraint
validation constraint
13. Soft Delete Policy

Untuk data penting gunakan:

deleted_at

Contoh:

deleted_at TIMESTAMP NULL

Data tidak langsung dihapus.

14. Transaction Handling

Operasi penting wajib menggunakan transaction.

Contoh:

pembayaran
transaksi keuangan
perubahan permission
15. Database Security

Wajib:

credential management
access control
encrypted connection
backup protection

Tidak diperbolehkan:

menyimpan password plaintext
expose database langsung ke publik
16. Backup & Recovery

Database wajib memiliki:

automated backup
recovery procedure
backup testing
17. Document History
Version	Date	Change
1.0	2026-07-18	Initial Database Governance

Setelah selesai:

```bash
git add docs/hc/HC-005_Database_Governance.md

cek:

git status

commit:

git commit -m "docs: add HC-005 Database Governance"