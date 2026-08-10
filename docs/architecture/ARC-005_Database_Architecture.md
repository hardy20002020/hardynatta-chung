# ARC-005 — Database Architecture

## HARDYNATTA CHUNG Enterprise Software Engineering Ecosystem

| Item | Value |
|---|---|
| Document ID | ARC-005 |
| Document Name | Database Architecture |
| Project | MAJE Platform |
| Category | Architecture |
| Version | 2.0 |
| Status | Approved |
| Owner | Engineering Team |
| Governance Authority | HC-000 Project Constitution |
| Parent Architecture | ARC-001 System Architecture |
| Foundation References | FDN-001, FDN-002, FDN-003, FDN-004, FDN-005 |
| Planning References | MASTER_DOCUMENT_BLUEPRINT, DOCUMENT_ROADMAP, DOCUMENT_DEPENDENCY, DOCUMENT_STATUS |
| Specialized Architecture Relationship | ARC-002, ARC-004, ARC-006, ARC-007, ARC-008, ARC-009 |
| Review Cycle | Every Major Release |

---

# 1. Purpose

ARC-005 mendefinisikan arsitektur database MAJE Platform sebagai specialized architecture di bawah ARC-001 System Architecture.

Dokumen ini menjadi acuan untuk persistence boundary, relational model, data integrity, migrations, indexing, security, backup, recovery, lifecycle, audit, performance, testing, deployment relationship, dan evolution.

---

# 2. Architecture Role

ARC-005 merupakan specialized architecture document.

ARC-001 menetapkan system-level architecture. ARC-005 menerjemahkan system architecture menjadi database architecture.

ARC-005 tidak menggantikan ARC-001 dan tidak mengambil alih backend application logic, security policy, deployment infrastructure, atau AI implementation.

---

# 3. Architectural Scope

Scope ARC-005 meliputi:

- PostgreSQL persistence;
- relational data model;
- schema organization;
- naming conventions;
- keys and relationships;
- constraints;
- indexes;
- transactions;
- migrations;
- database access boundary;
- security;
- audit;
- backup and recovery;
- lifecycle and retention;
- performance;
- testing;
- deployment relationship.

---

# 4. Architectural Authority

Database architecture harus konsisten dengan:

- HC-000 Project Constitution;
- HC-003 Coding Standard;
- HC-004 API Governance;
- HC-005 Database Governance;
- HC-006 Security Governance;
- HC-007 Testing Governance;
- HC-008 Deployment Governance;
- HC-009 Monitoring and Observability Governance;
- HC-011 Documentation Governance;
- HC-012 Engineering Quality Governance;
- ARC-001 System Architecture.

---

# 5. Database Architectural Principles

MAJE database mengikuti prinsip:

- Integrity First;
- Secure by Default;
- ACID Transactions;
- Explicit Relationships;
- Controlled Schema Evolution;
- Least Privilege;
- Predictable Naming;
- Measured Performance;
- Recoverability;
- Auditability;
- Data Minimization where applicable;
- Evolutionary Architecture.

---

# 6. System of Record

PostgreSQL menjadi primary relational system of record untuk transactional application data.

Database menjadi authoritative persistence layer untuk data yang memang berada dalam database domain.

Cache, vector index, search index, dan derived stores tidak otomatis menjadi source of truth.

---

# 7. Database Boundary

Database berada di belakang backend persistence boundary.

Application code mengakses database melalui controlled data-access mechanisms seperti SQLAlchemy repositories dan database sessions.

Frontend dan external clients tidak boleh mengakses database secara langsung.

---

# 8. High-Level Database Architecture

```text
Client
  |
  v
Backend API
  |
  v
Service Layer
  |
  v
Repository / Data Access
  |
  v
SQLAlchemy
  |
  v
PostgreSQL
  |
  +--> Backup / Recovery
  +--> Monitoring / Audit
```

---

# 9. Technology Stack

Baseline database technology:

- PostgreSQL 17 runtime baseline in the current development stack;
- SQLAlchemy 2.x for ORM/data access;
- Alembic for schema migration;
- psycopg for PostgreSQL connectivity.

Technology upgrades require compatibility validation and governance.

---

# 10. Database Domains

Conceptual database domains dapat meliputi:

- identity and authentication;
- users and authorization;
- organization and master data;
- application configuration;
- competition or business domain data;
- AI-related metadata where persistence is required;
- audit data;
- operational metadata.

Domain expansion harus mengikuti architecture governance.

---

# 11. Schema Organization

Schema organization harus menjaga separation of concerns dan ownership yang jelas.

Table grouping atau PostgreSQL schema separation dapat digunakan apabila complexity dan governance membutuhkannya.

---

# 12. Naming Convention

Database identifiers menggunakan snake_case sebagai baseline.

Nama harus deskriptif, konsisten, dan tidak bergantung pada reserved words.

---

# 13. Table Naming

Table names menggunakan plural nouns sebagai baseline, misalnya `users`, `roles`, `audit_logs`, dan `organizations`.

Konvensi existing project harus dipertahankan secara konsisten.

---

# 14. Column Naming

Column names menggunakan snake_case.

Contoh: `created_at`, `updated_at`, `is_active`, `user_id`.

---

# 15. Primary Key Strategy

Setiap persistent entity harus memiliki primary key yang jelas.

`id` dapat digunakan sebagai baseline conventional primary key apabila sesuai dengan domain model.

---

# 16. Foreign Key Strategy

Foreign key menggunakan pola `<referenced_table_singular>_id` atau convention project yang telah ditetapkan.

Foreign key harus memiliki target yang jelas dan constraint yang sesuai.

---

# 17. Relationship Architecture

Relationship database dapat berupa:

- one-to-one;
- one-to-many;
- many-to-many.

Relationship harus direpresentasikan secara eksplisit melalui keys dan constraints.

---

# 18. Nullability

Column nullability harus ditentukan berdasarkan domain semantics.

NULL tidak boleh digunakan sekadar untuk menghindari validasi business rules.

---

# 19. Common Audit Columns

Tabel yang membutuhkan lifecycle tracking dapat menggunakan:

- `created_at`;
- `updated_at`;
- `created_by` apabila applicable;
- `updated_by` apabila applicable;
- status atau `is_active` apabila sesuai domain.

Tidak semua tabel harus dipaksa memiliki kolom yang tidak relevan.

---

# 20. Timestamp Strategy

Timestamp harus memiliki timezone semantics yang konsisten.

Untuk distributed application, UTC menjadi baseline storage convention kecuali governance domain menentukan lain.

---

# 21. Data Integrity

Database integrity dijaga melalui combination of:

- primary keys;
- foreign keys;
- unique constraints;
- not-null constraints;
- check constraints;
- transaction boundaries.

---

# 22. Unique Constraints

Business identifiers yang harus unik wajib memiliki unique constraint di database.

Application validation tidak menggantikan database uniqueness enforcement.

---

# 23. Check Constraints

Check constraints digunakan untuk invariant yang tepat ditegakkan pada database.

Business workflows yang kompleks tetap berada pada application/service layer.

---

# 24. Referential Integrity

Foreign key constraints menjaga referential integrity.

Delete/update behavior harus dipilih secara eksplisit dan tidak boleh menyebabkan accidental cascade.

---

# 25. Transaction Architecture

Transactional operations menggunakan ACID transaction semantics PostgreSQL.

Transaction boundary harus dikendalikan secara konsisten oleh application service dan data-access architecture.

---

# 26. Isolation Strategy

Transaction isolation harus dipilih berdasarkan consistency requirements dan workload.

Default PostgreSQL behavior dapat digunakan apabila memenuhi kebutuhan; perubahan isolation memerlukan alasan teknis.

---

# 27. Concurrency Control

Database design harus aman terhadap concurrent transactions.

Optimistic atau pessimistic locking dapat digunakan sesuai contention pattern.

---

# 28. Connection Management

Database connections dikelola melalui SQLAlchemy engine dan connection pool.

Connection lifetime tidak boleh dikendalikan secara ad-hoc pada setiap query.

---

# 29. Session Management

Database session dikelola melalui controlled dependency mechanism.

Session harus memiliki scope yang jelas, ditutup setelah work selesai, dan tidak dibagikan antar-request secara unsafe.

---

# 30. Query Discipline

Queries harus explicit, parameterized, maintainable, dan testable.

Raw SQL hanya digunakan ketika terdapat technical justification yang jelas.

---

# 31. ORM Architecture

SQLAlchemy ORM menjadi abstraction layer untuk application persistence.

ORM models merepresentasikan persistence entities dan tidak boleh menjadi tempat utama business policy.

---

# 32. Repository Boundary

Repository layer menjadi controlled boundary untuk database operations.

Repository bertanggung jawab terhadap persistence concerns, bukan business orchestration.

---

# 33. N+1 Query Prevention

Application harus menghindari accidental N+1 queries.

Eager loading, explicit joins, batching, atau query restructuring digunakan berdasarkan measurement.

---

# 34. Pagination Strategy

Large collections harus menggunakan pagination.

Pagination strategy harus memiliki stable ordering dan batas page size yang terkontrol.

---

# 35. Filtering and Search

Filtering dan search harus menggunakan parameterized queries dan indexed paths apabila diperlukan.

Arbitrary SQL expressions dari external input tidak diperbolehkan.

---

# 36. Indexing Principles

Index dibuat berdasarkan access pattern dan measurement.

Index bukan default untuk setiap column karena menambah storage dan write overhead.

---

# 37. Foreign Key Indexes

Foreign key columns harus dievaluasi untuk indexing terutama pada join, lookup, dan referential operations yang frequent.

---

# 38. Composite Indexes

Composite indexes digunakan apabila query workload membutuhkan kombinasi column tertentu.

Column ordering harus mengikuti access patterns.

---

# 39. Migration Architecture

Seluruh schema changes harus melalui Alembic migrations yang version controlled.

Migration menjadi authoritative mechanism untuk controlled schema evolution.

---

# 40. Backward Compatibility

Breaking schema changes harus mempertimbangkan application compatibility.

Expand-and-contract strategy dapat digunakan untuk perubahan yang membutuhkan zero/minimal downtime.

---

# 41. Migration Safety

Migration tidak boleh mengandung destructive operation tanpa explicit impact assessment dan recovery plan.

---

# 42. Production Migration

Production migrations harus dijalankan melalui governed deployment process.

Manual ad-hoc schema changes tidak boleh menjadi normal operating procedure.

---

# 43. Environment Separation

Minimum conceptual environments:

- development;
- testing;
- staging;
- production.

Database instance dan credentials antar-environment harus dipisahkan.

---

# 44. Configuration Architecture

Database configuration mencakup connection target, credentials reference, pool settings, timeout, SSL/TLS policy, dan environment-specific parameters.

Configuration tidak boleh hard-coded.

---

# 45. Secrets Management

Database credentials harus berasal dari secure environment configuration atau secret management mechanism.

Credentials tidak boleh masuk repository.

---

# 46. Network Security

Database access harus dibatasi pada trusted application and infrastructure boundaries.

Public exposure tidak diperbolehkan tanpa explicit architecture and security approval.

---

# 47. Transport Encryption

Database connections pada environment yang memerlukan secure transport harus menggunakan TLS/SSL sesuai deployment security policy.

---

# 48. Least Privilege

Database users dan roles harus memiliki privilege minimum yang dibutuhkan.

Application runtime account tidak boleh otomatis memiliki unrestricted administrative privileges.

---

# 49. Administrative Access

Database administration harus menggunakan controlled administrative credentials dan auditable access path.

---

# 50. Data Classification

Data harus diklasifikasikan sesuai sensitivity dan governance requirements.

Classification memengaruhi access, logging, retention, backup, dan exposure.

---

# 51. Sensitive Data Handling

Sensitive data harus diminimalkan dan dilindungi.

Application logs dan audit records tidak boleh secara tidak sengaja menyalin sensitive database content.

---

# 52. Encryption at Rest

Encryption at rest mengikuti capability dan policy infrastructure/deployment environment.

ARC-005 mendefinisikan requirement relationship, sedangkan implementation detail berada pada deployment/security architecture.

---

# 53. Audit Architecture

Security-significant atau governance-significant database changes harus dapat diaudit.

Audit dapat berada pada application audit layer, database mechanism, atau kombinasi sesuai requirement.

---

# 54. Soft Delete

Soft deletion dapat digunakan untuk domain yang membutuhkan recoverability atau auditability.

Soft delete tidak boleh diterapkan secara otomatis pada semua tabel tanpa domain rationale.

---

# 55. Retention Policy

Retention harus ditentukan berdasarkan business need, legal requirement, operational need, dan storage cost.

Retention policy harus memiliki owner.

---

# 56. Archival Strategy

Data yang tidak lagi aktif tetapi masih diperlukan dapat dipindahkan ke archival storage atau status archival sesuai governance.

---

# 57. Deletion Strategy

Deletion harus mempertimbangkan referential integrity, audit requirements, retention policy, dan business ownership.

Destructive deletion harus controlled.

---

# 58. Backup Strategy

Database backup harus mendukung recovery objectives.

Baseline dapat mencakup automated backups, periodic full backups, dan tested restore procedures.

---

# 59. Backup Types

Backup strategy dapat menggunakan kombinasi full, incremental, differential, atau PostgreSQL-native recovery mechanisms sesuai deployment capability.

---

# 60. Point-in-Time Recovery

Untuk workload yang membutuhkan granular recovery, PostgreSQL WAL-based point-in-time recovery dapat digunakan apabila supported oleh deployment architecture.

---

# 61. Backup Encryption

Backup yang mengandung sensitive data harus dilindungi sesuai security policy, termasuk encryption dan access control.

---

# 62. Restore Testing

Backup tanpa restore verification tidak dianggap sufficient recovery assurance.

Restore test harus dilakukan secara berkala sesuai recovery governance.

---

# 63. Recovery Objectives

Database recovery harus memiliki target RPO dan RTO yang ditentukan berdasarkan business criticality.

Nilai target tidak boleh diasumsikan tanpa business requirement.

---

# 64. Disaster Recovery

Database disaster recovery strategy berada pada relationship dengan ARC-008 Deployment Architecture.

ARC-005 mendefinisikan data persistence and recoverability requirements.

---

# 65. High Availability

High availability dapat menggunakan PostgreSQL replication atau managed database capability apabila business requirement membutuhkannya.

Implementation topology berada pada deployment architecture.

---

# 66. Read Replica

Read replicas dapat digunakan untuk read scaling atau reporting workload setelah workload dan consistency requirements tervalidasi.

---

# 67. Partitioning

Partitioning dapat digunakan untuk large time-series atau high-volume tables apabila query dan lifecycle pattern mendukungnya.

---

# 68. Archival Performance

Archival harus mengurangi operational dataset size tanpa menghilangkan required traceability.

Archival queries harus tetap memiliki documented access path apabila dibutuhkan.

---

# 69. Performance Baseline

Database performance harus diukur menggunakan query latency, throughput, resource consumption, connection usage, dan workload-specific indicators.

---

# 70. Query Optimization

Query optimization dilakukan berdasarkan execution plan dan measurement.

Premature optimization harus dihindari.

---

# 71. EXPLAIN Discipline

PostgreSQL EXPLAIN/EXPLAIN ANALYZE dapat digunakan untuk diagnosis query performance dengan hati-hati pada representative workload.

---

# 72. Statistics Maintenance

PostgreSQL statistics dan vacuum/analyze behavior harus dipelihara sesuai operational configuration.

Detail runtime tuning berada pada deployment/operations governance.

---

# 73. Storage Management

Storage growth harus dimonitor.

Table, index, WAL, backup, dan temporary storage growth harus memiliki operational visibility.

---

# 74. Capacity Planning

Capacity planning mempertimbangkan data growth, connection count, query workload, index growth, backup size, dan recovery requirements.

---

# 75. Monitoring Boundary

Database telemetry harus tersedia untuk health, connections, latency, errors, locks, storage, replication apabila ada, dan backup status.

---

# 76. Health Check

Database health mechanism harus dapat membedakan process availability dari usable readiness.

Application readiness dapat bergantung pada database connectivity.

---

# 77. Lock Monitoring

Long-running locks dan blocked transactions harus dapat dideteksi pada operational environment.

---

# 78. Connection Monitoring

Connection pool utilization dan database connection limits harus dipantau untuk mencegah exhaustion.

---

# 79. Testing Architecture

Database testing mencakup schema tests, migration tests, repository tests, integration tests, constraint tests, transaction tests, dan performance tests sesuai risk.

---

# 80. Migration Testing

Setiap migration harus diuji pada representative schema state sebelum deployment.

---

# 81. Constraint Testing

Tests harus memastikan primary key, foreign key, unique, not-null, dan check constraints bekerja sesuai design.

---

# 82. Transaction Testing

Transaction tests harus memverifikasi commit, rollback, atomicity, dan concurrency-sensitive behavior yang relevan.

---

# 83. Integration Testing

Integration tests dapat menjalankan backend → repository → PostgreSQL flow pada isolated test database.

---

# 84. Test Database Isolation

Test database harus terisolasi dari development dan production data.

Test fixtures harus deterministic dan reproducible.

---

# 85. Docker Relationship

Development database dapat dijalankan sebagai PostgreSQL container dalam Docker Compose.

Container configuration adalah development implementation dan bukan production topology.

---

# 86. Deployment Relationship

ARC-005 mendefinisikan database application/persistence architecture.

Deployment topology, managed service choice, networking, storage class, dan infrastructure configuration berada pada ARC-008.

---

# 87. Production Readiness

Production database harus memenuhi requirements untuk security, migration, backup, monitoring, recovery, capacity, access control, dan operational ownership.

---

# 88. Change Management

Database changes harus melalui controlled change process.

Schema, migration, indexes, retention, and recovery changes harus dapat ditelusuri.

---

# 89. Dependency Management

PostgreSQL driver, SQLAlchemy, Alembic, dan related dependencies harus version controlled dan diperbarui melalui engineering process.

---

# 90. Data Quality

Data quality harus dijaga melalui constraints, validation, reconciliation, duplicate detection, dan controlled correction workflows sesuai domain.

---

# 91. Reconciliation

Untuk critical data, reconciliation mechanism dapat digunakan untuk mendeteksi divergence antara application state dan dependent systems.

---

# 92. Operational Runbooks

Operational procedures untuk backup, restore, migration failure, lock issues, capacity alerts, dan recovery harus terdokumentasi.

---

# 93. Ownership

Setiap database domain harus memiliki technical ownership yang jelas.

Ownership mencakup schema changes, data quality, security, recovery, dan operational escalation.

---

# 94. Documentation Relationship

Database documentation harus tetap selaras dengan implementation, migrations, schema models, dan governance documents.

---

# 95. Future Roadmap

Potential future capabilities meliputi:

- read replicas;
- partitioning;
- advanced archival;
- analytics/data warehouse integration;
- vector storage integration where justified;
- stronger retention automation.

Setiap capability memerlukan architecture validation sebelum menjadi baseline.

---

# 96. Schema Review Governance

Perubahan schema harus direview dari sisi compatibility, integrity, performance, security, dan recovery impact.

---

# 97. Migration Rollback Governance

Rollback strategy harus dinilai sebelum migration diterapkan; irreversible migrations memerlukan explicit mitigation plan.

---

# 98. Database Incident Response

Database incidents harus memiliki escalation path, containment procedure, diagnosis, recovery, dan post-incident review.

---

# 99. Architecture Decision Records

Significant database architecture decisions harus dapat ditelusuri melalui architecture decision atau change records yang relevan.

---

# 100. Architecture Dependency Map

```text
HC-000
  |
  +-- FDN-001..FDN-005
  |
  +-- Planning Documents
          |
          v
      ARC-001
          |
          v
      ARC-005
          |
          +-- ARC-002 Backend
          +-- ARC-004 AI Service
          +-- ARC-006 Integration
          +-- ARC-007 Security
          +-- ARC-008 Deployment
          +-- ARC-009 Observability
```

---

# 101. Database Component Dependency

```text
Backend Service
      |
      v
Repository / Data Access
      |
      v
SQLAlchemy
      |
      v
PostgreSQL
  |       |
  v       v
Backup   Monitoring
```

---

# 102. Architecture Completion

ARC-005 v2.0 establishes the governed database architecture baseline for MAJE Platform.

The architecture separates persistence, integrity, schema evolution, security, recovery, performance, monitoring, and operational responsibilities.

---

# 103. Document Control

ARC-005 is governed under HC-011 Documentation Governance.

Changes to this document must:

- preserve document identity;
- maintain architecture consistency;
- update version information;
- record meaningful changes;
- remain aligned with ARC-001;
- be reviewed according to architecture governance.

---

# 104. Revision History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-20 | Initial Database Architecture |
| 2.0 | 2026-08-10 | Refactored as governed specialized Database Architecture under ARC-001; established persistence boundaries, relational integrity, migrations, indexing, security, backup, recovery, lifecycle, performance, testing, and deployment relationships |

---

# Final Statement

ARC-005 — Database Architecture

HARDYNATTA CHUNG Enterprise Software Engineering Ecosystem

Version 2.0 — Governed Specialized Database Architecture

The database architecture connects governed application behavior with durable, secure, consistent, recoverable, observable, and evolvable persistence.
