# OPS-003 — Backup & Restore Procedure

**Document ID:** OPS-003
**Project:** MAJE Platform
**Document Area:** Operations
**Status:** Procedure Baseline Established
**Version:** 1.0
**Owner:** Engineering Team
**Last Updated:** 2026-08-27

---

# 1. Purpose

Dokumen ini mendefinisikan prosedur backup dan restore MAJE Platform
secara terkendali, dapat ditelusuri, dan berbasis evidence.

Procedure ini digunakan untuk:

- database backup;
- backup archive validation;
- isolated restore;
- restored database validation;
- recovery integrity validation;
- recovery evidence recording;
- failure handling;
- recovery readiness assessment.

Procedure ini menerjemahkan requirement dari:

- ARC-005 — Database Architecture
- ARC-008 — Deployment Architecture
- HC-005 — Database Governance
- HC-008 — Deployment Governance

serta menggunakan EVIDENCE-005 sebagai execution evidence untuk
PostgreSQL backup dan isolated restore validation.

Dokumen ini tidak menyatakan production backup atau production disaster
recovery readiness apabila capability tersebut belum memiliki implementation
dan execution evidence yang sesuai.

---

# 2. Scope

Procedure ini mencakup:

- backup preconditions;
- PostgreSQL backup creation;
- backup archive inspection;
- isolated restore;
- table inventory validation;
- migration state validation;
- database accessibility validation;
- row-count validation;
- recovery integrity assessment;
- evidence recording;
- recovery failure handling;
- production recovery boundary.

Procedure ini berlaku sebagai baseline operational backup and restore
procedure.

Production backup dan restore tetap membutuhkan environment,
authorization, storage controls, credential controls, retention policy,
recovery objectives, dan operational evidence yang sesuai.

---

# 3. Backup and Recovery Status Classification

Backup and recovery capability menggunakan klasifikasi berikut:

## DOCUMENTED

Procedure atau requirement telah didokumentasikan.

## IMPLEMENTED

Capability atau mechanism tersedia pada repository atau runtime.

## VALIDATED

Capability telah dieksekusi dan memiliki objective evidence.

## NOT YET EVIDENCED

Capability telah didefinisikan atau tersedia secara konseptual tetapi
belum memiliki execution evidence yang memadai untuk scope tertentu.

---

# 4. Current Backup and Recovery Baseline

Repository dan existing evidence menunjukkan baseline berikut:

| Capability | Status |
|---|---|
| PostgreSQL database runtime | IMPLEMENTED |
| PostgreSQL backup mechanism | IMPLEMENTED |
| PostgreSQL restore mechanism | IMPLEMENTED |
| Isolated PostgreSQL backup execution | VALIDATED |
| Backup archive inspection | VALIDATED |
| Isolated PostgreSQL restore execution | VALIDATED |
| Restored table inventory validation | VALIDATED |
| Migration state validation | VALIDATED |
| Restored database accessibility validation | VALIDATED |
| Row-count validation | VALIDATED |
| Automated production backup | NOT YET EVIDENCED |
| Off-site backup retention | NOT YET EVIDENCED |
| Encrypted production backup storage | NOT YET EVIDENCED |
| Production restore execution | NOT YET EVIDENCED |
| Point-in-Time Recovery | NOT YET EVIDENCED |
| PostgreSQL replication | NOT YET EVIDENCED |
| Production RTO/RPO compliance | NOT YET EVIDENCED |
| Production disaster recovery execution | NOT YET EVIDENCED |

Status tersebut merupakan evidence boundary dan bukan production readiness
certification.

---

# 5. Recovery Architecture Relationship

Backup and restore operations harus konsisten dengan:

- ARC-005 — Database Architecture;
- ARC-008 — Deployment Architecture;
- HC-005 — Database Governance;
- HC-008 — Deployment Governance;
- OPS-001 — Deployment Procedure;
- OPS-002 — Health Check Procedure.

ARC-005 menetapkan bahwa backup harus mendukung recovery objectives,
restore testing merupakan bagian dari recovery assurance, dan recovery
objectives harus ditentukan berdasarkan business criticality.

OPS-003 menerjemahkan requirement tersebut menjadi operational procedure.

---

# 6. Recovery Principles

MAJE backup and recovery operations mengikuti prinsip:

- Recovery Before Assumption
- Evidence Based Recovery
- Data Integrity First
- Controlled Restore
- Isolated Validation
- Traceable Execution
- Least Privilege
- No Unverified Production Claims

Backup yang berhasil dibuat tidak otomatis berarti backup dapat dipulihkan.

Backup yang dapat dipulihkan ke isolated validation database juga tidak
otomatis berarti production disaster recovery telah tervalidasi.

---

# 7. Backup Preconditions

Sebelum membuat backup, operator harus memverifikasi:

- target database;
- target environment;
- database accessibility;
- database identity;
- database user;
- applicable migration state;
- available storage;
- backup format;
- destination path;
- required authorization;
- sensitive-data handling requirement;
- recovery objective yang berlaku apabila telah ditentukan.

Material backup execution harus mencatat environment dan database scope.

---

# 8. Source Database Validation

Sebelum backup dilakukan, validasi source database.

Baseline identity validation:

```bash
docker compose exec -T postgres   psql -U postgres -d maje   -c "SELECT current_database(), current_user;"

Source database harus dapat diakses.

Untuk validasi migration state:

docker compose exec backend alembic current

Database identity dan migration state harus dicatat sebagai bagian dari
evidence apabila backup digunakan untuk recovery validation.

9. Backup Creation

PostgreSQL custom-format backup dapat dibuat menggunakan pg_dump.

Baseline command:

docker compose exec -T postgres   pg_dump -U postgres -d maje --format=custom   > docs/evidence/backend/f009-work/maje_f009_backup.dump

Backup format:

CUSTOM

Operator harus memastikan command selesai tanpa error.

Backup artifact harus diperlakukan sesuai security dan retention policy
yang berlaku.

Backup yang mengandung sensitive data tidak boleh ditempatkan pada
repository source control kecuali governance secara eksplisit
mengizinkannya.

10. Backup Archive Validation

Backup archive harus diperiksa sebelum digunakan untuk restore.

Baseline command:

docker compose exec -T postgres   pg_restore --list   < docs/evidence/backend/f009-work/maje_f009_backup.dump

Validation harus memastikan archive dapat dibaca oleh pg_restore.

Archive inspection merupakan validation terhadap struktur backup archive,
bukan validation bahwa seluruh recovery scenario production telah berhasil.

11. Backup Integrity Consideration

Backup integrity harus dinilai berdasarkan hasil execution.

Minimum validation baseline:

backup command completed successfully;
archive dapat dibaca;
archive memiliki TOC entries;
backup format teridentifikasi;
restore dapat dilakukan pada isolated database apabila procedure
membutuhkan recovery validation.

EVIDENCE-005 menunjukkan bahwa backup archive berhasil diperiksa dan
memiliki TOC entries pada execution validation tersebut.

12. Restore Preconditions

Restore harus dilakukan pada target database yang telah ditentukan.

Untuk validation, target restore harus menggunakan isolated database.

Operator harus memastikan:

target database bukan database production aktif;
target database dapat menerima restore;
target database memiliki authorization yang sesuai;
backup artifact yang digunakan telah diidentifikasi;
target database tidak mengandung data yang tidak boleh tertimpa;
recovery validation scope telah ditentukan.

Restore terhadap production database memerlukan authorization dan
controlled recovery procedure tersendiri.

13. Isolated Restore Procedure

Untuk recovery validation, restore dilakukan ke isolated validation database.

Contoh target:

maje_f009_restore

Baseline restore command:

docker compose exec -T postgres   pg_restore   -U postgres   -d maje_f009_restore   --exit-on-error   < docs/evidence/backend/f009-work/maje_f009_backup.dump

--exit-on-error digunakan agar execution berhenti apabila terjadi error
yang relevan selama restore.

Restore result harus dicatat.

14. Restore Completion Validation

Setelah restore selesai, operator harus memastikan:

command selesai tanpa error;
target database dapat diakses;
restored schema tersedia;
expected tables tersedia;
migration metadata tersedia;
data dapat di-query.

Restore completion tanpa subsequent validation tidak dianggap sebagai
complete recovery assurance.

15. Restored Database Identity

Validasi identity database hasil restore.

Baseline:

SELECT current_database(), current_user;

Expected validation harus menunjukkan database target yang benar.

Contoh validation dari EVIDENCE-005:

current_database = maje_f009_restore
current_user = postgres

Database identity harus dicatat untuk mencegah validation dilakukan
terhadap database yang salah.

16. Table Inventory Validation

Setelah restore, inventory public tables harus dibandingkan dengan source
database.

Validation baseline:

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

Source dan restored table inventory harus dibandingkan.

Perbedaan inventory harus diinvestigasi sebelum recovery dinyatakan
berhasil.

EVIDENCE-005 menunjukkan bahwa source dan restored database masing-masing
memiliki 25 public tables dan inventory comparison menghasilkan no
differences.

17. Migration State Validation

Migration state harus divalidasi setelah restore.

Source validation:

docker compose exec backend alembic current

Restore validation:

SELECT version_num FROM alembic_version;

Migration state harus dicatat.

EVIDENCE-005 menunjukkan source dan restored database sama-sama melaporkan:

b7d725ec3821

Migration state matching merupakan bagian dari recovery integrity
validation.

18. Restored Database Accessibility

Restored database harus dapat diakses dan di-query.

Minimum validation:

connection berhasil;
current database benar;
current user benar;
required schema dapat diakses;
query dapat dijalankan.

Accessibility validation tidak sama dengan validation seluruh application
workflow.

19. Row Count Validation

Untuk isolated recovery validation, row counts dapat dibandingkan antara
source dan restored database.

Validation harus dilakukan terhadap seluruh public tables yang termasuk
dalam recovery scope.

Expected result:

Source tables:
25

Restore tables:
25

Matching row counts:
25/25

EVIDENCE-005 menunjukkan bahwa seluruh 25 public tables memiliki matching
row counts antara source dan restored database.

Row-count matching merupakan evidence kuat terhadap data restoration
consistency pada validation scope, tetapi bukan jaminan terhadap seluruh
production recovery scenario.

20. Recovery Integrity Assessment

Recovery validation dapat dinyatakan PASS apabila applicable validation
checks berhasil, termasuk:

backup creation;
backup archive inspection;
isolated restore;
table inventory comparison;
migration state comparison;
database accessibility;
row-count comparison.

Assessment harus selalu menyebutkan validation scope.

Successful isolated restore membuktikan recovery execution pada tested
environment dan tested database scope.

Itu tidak membuktikan production disaster recovery readiness.

21. Backup Artifact Handling

Backup artifact harus dikelola sesuai environment dan governance.

Untuk validation execution, temporary backup artifact dapat dibuat pada
working area dan dihapus setelah validation selesai apabila retention
tidak diperlukan.

EVIDENCE-005 menggunakan temporary custom-format backup artifact dan
mencatat bahwa binary backup artifact tidak dipertahankan sebagai
Git-tracked repository artifact.

Backup artifacts yang diperlukan untuk operational recovery harus memiliki
retention dan access control yang sesuai.

22. Production Backup Boundary

Production backup harus diperlakukan sebagai capability terpisah dari
development backup validation.

Current status:

Production Backup Configuration
        ↓
NOT YET EVIDENCED

Production Backup Scheduling
        ↓
NOT YET EVIDENCED

Production Backup Retention
        ↓
NOT YET EVIDENCED

Keberadaan pg_dump atau backup command tidak dengan sendirinya
membuktikan automated production backup.

Production backup readiness memerlukan evidence terhadap actual production
environment dan applicable operational controls.

23. Off-Site Backup Boundary

Off-site backup retention belum dinyatakan validated.

Belum terdapat evidence dalam current baseline yang membuktikan:

off-site backup storage;
geographically separate retention;
cross-environment replication of backups;
verified retrieval from off-site storage.

Karena itu statusnya:

NOT YET EVIDENCED
24. Backup Encryption Boundary

ARC-005 mensyaratkan perlindungan backup yang mengandung sensitive data
sesuai security policy.

OPS-003 tidak menyatakan bahwa production backup encryption telah
diimplementasikan atau divalidasi.

Current status:

Production Backup Encryption
        ↓
NOT YET EVIDENCED

Encryption implementation dan validation harus memiliki evidence tersendiri
apabila diwajibkan oleh deployment/security environment.

25. Point-in-Time Recovery Boundary

ARC-005 menyatakan bahwa PostgreSQL WAL-based point-in-time recovery dapat
digunakan apabila didukung oleh deployment architecture dan workload
requirements.

Current repository evidence tidak digunakan untuk menyatakan PITR
production telah tersedia atau tervalidasi.

Current status:

Point-in-Time Recovery
        ↓
NOT YET EVIDENCED
26. Replication Boundary

PostgreSQL replication atau managed database high availability dapat
digunakan apabila business requirement membutuhkannya.

OPS-003 tidak menyatakan bahwa replication production telah
diimplementasikan.

Current status:

Production Database Replication
        ↓
NOT YET EVIDENCED
27. RPO and RTO Boundary

ARC-005 menetapkan bahwa recovery harus memiliki target RPO dan RTO
berdasarkan business criticality.

Nilai RPO/RTO tidak boleh diasumsikan tanpa business requirement.

OPS-003 karena itu tidak menetapkan arbitrary production RPO/RTO value.

Current status:

Production RPO/RTO Compliance
        ↓
NOT YET EVIDENCED
28. Production Restore Boundary

Production restore adalah controlled operational action.

Restore terhadap production database tidak boleh dilakukan hanya karena
isolated restore validation berhasil.

Sebelum production restore:

identify incident or recovery reason;
identify approved backup;
verify backup identity;
verify target database;
assess data impact;
obtain required authorization;
confirm recovery procedure;
establish validation criteria;
preserve recovery evidence.

Current status:

Production Restore Execution
        ↓
NOT YET EVIDENCED
29. Recovery Failure Handling

Jika restore gagal:

Detection
    ↓
Stop / Contain
    ↓
Inspect Error
    ↓
Verify Backup Artifact
    ↓
Verify Target Database
    ↓
Determine Recovery Action
    ↓
Retry Only When Controlled
    ↓
Validate Recovery
    ↓
Record Result

Operator tidak boleh melakukan repeated uncontrolled restore attempts
terhadap production database.

Failure investigation harus mempertimbangkan:

corrupt or incomplete backup;
incompatible PostgreSQL environment;
target database condition;
insufficient permission;
insufficient storage;
schema or migration mismatch;
dependency issue;
operational configuration error.
30. Data Integrity Considerations

Recovery harus memprioritaskan data integrity.

Operator harus mempertimbangkan:

table inventory;
migration state;
row counts;
referential integrity;
application compatibility;
transaction consistency;
backup timestamp;
recovery point;
data loss exposure.

Row-count matching alone tidak membuktikan seluruh business-level
data integrity.

Business-level validation harus dilakukan apabila recovery scope
memerlukannya.

31. Relationship to Health Validation

Setelah restore, database recovery validation dapat dilanjutkan dengan
application health validation apabila database digunakan oleh application
service.

Related procedure:

OPS-002 — Health Check Procedure

Recovery flow dapat menjadi:

Restore
   ↓
Database Validation
   ↓
Application Startup
   ↓
Health Check
   ↓
Critical Workflow Validation
   ↓
Evidence

Database restore success tidak otomatis berarti application health telah
pulih.

32. Relationship to Deployment

Backup and restore operations harus terintegrasi dengan controlled
deployment lifecycle.

Untuk deployment yang mengubah schema atau persistent data:

Release Preparation
        ↓
Backup Requirement Assessment
        ↓
Backup
        ↓
Migration / Deployment
        ↓
Health Validation
        ↓
Post-Deployment Validation

Applicable release governance tetap mengikuti OPS-001, HC-008, dan HC-014.

33. Evidence Recording

Material backup or restore execution harus mencatat:

date/time;
environment;
source database;
target database;
Git revision where applicable;
migration revision;
backup format;
backup artifact identity;
command or validation method;
restore result;
table inventory result;
migration state result;
row-count result;
health result where applicable;
recovery action;
operator/responsible role where applicable;
limitations.

Evidence harus disimpan sesuai Evidence Governance.

34. Existing Validation Evidence

Current execution evidence:

EVIDENCE-005 — Backup & Restore Validation

EVIDENCE-005 memvalidasi:

PostgreSQL backup utility availability;
source database accessibility;
custom-format backup creation;
backup archive inspection;
isolated restore;
restored table inventory;
migration state;
restored database accessibility;
row-count consistency.

Overall result:

PASS

EVIDENCE-005 menyatakan:

25/25 table row counts matched.

Validation tersebut merupakan evidence untuk isolated PostgreSQL backup
and restore execution.

35. Current Validation Status

OPS-003 saat ini diklasifikasikan sebagai:

DOCUMENTED

Procedure ini grounded pada:

ARC-005;
ARC-008;
HC-005;
HC-008;
EVIDENCE-005;
existing PostgreSQL runtime configuration.

Existing evidence mendukung classification VALIDATED untuk isolated
PostgreSQL backup and restore execution.

Namun capabilities berikut tetap:

Automated production backup
NOT YET EVIDENCED

Off-site backup retention
NOT YET EVIDENCED

Production backup encryption
NOT YET EVIDENCED

Production restore execution
NOT YET EVIDENCED

Point-in-Time Recovery
NOT YET EVIDENCED

Production replication
NOT YET EVIDENCED

Production RPO/RTO compliance
NOT YET EVIDENCED

Production disaster recovery execution
NOT YET EVIDENCED
36. Operational Limitations

OPS-003 bukan merupakan:

production backup certification;
production restore certification;
disaster recovery certification;
business continuity certification;
RPO certification;
RTO certification;
off-site retention certification;
backup encryption certification;
replication certification;
production availability certification.

Current validated evidence hanya mencakup tested PostgreSQL backup and
isolated restore scope.

37. Related Documents

Architecture:

ARC-001 — Master System Architecture
ARC-005 — Database Architecture
ARC-008 — Deployment Architecture

Governance:

HC-000 — Project Constitution
HC-005 — Database Governance
HC-006 — Security Governance
HC-007 — Testing Governance
HC-008 — Deployment Governance
HC-009 — Monitoring & Observability Governance
HC-014 — Release Management

Operations:

OPS-001 — Deployment Procedure
OPS-002 — Health Check Procedure

Evidence:

EVIDENCE-005 — Backup & Restore Validation
EVIDENCE-013 — CI/CD Implementation Validation
38. Document History
Version	Date	Change
1.0	2026-08-27	Established baseline backup and restore procedure
