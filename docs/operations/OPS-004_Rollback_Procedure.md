# OPS-004 — Rollback Procedure

**Document ID:** OPS-004
**Project:** MAJE Platform
**Document Area:** Operations
**Status:** Procedure Baseline Established
**Version:** 1.0
**Owner:** Engineering Team
**Last Updated:** 2026-08-27

---

# 1. Purpose

Dokumen ini mendefinisikan prosedur rollback MAJE Platform secara
terkendali, dapat ditelusuri, dan berbasis evidence.

Procedure ini digunakan untuk:

- deployment failure;
- critical application defect;
- release regression;
- severe performance degradation;
- security-related release issue;
- restoration ke known-good release;
- post-rollback health validation;
- rollback evidence recording.

Procedure ini menerjemahkan requirement dari:

- ARC-008 — Deployment Architecture
- HC-008 — Deployment Governance
- HC-014 — Release Management
- OPS-001 — Deployment Procedure
- OPS-002 — Health Check Procedure

Dokumen ini tidak menyatakan bahwa production rollback telah dieksekusi
atau divalidasi apabila belum terdapat objective execution evidence.

---

# 2. Scope

Procedure ini mencakup:

- rollback decision;
- rollback preconditions;
- failed release identification;
- known-good release identification;
- Git revision validation;
- artifact identification;
- database compatibility assessment;
- rollback execution boundary;
- health validation;
- post-rollback validation;
- failure handling;
- evidence recording;
- production rollback limitations.

Procedure ini berlaku sebagai baseline operational rollback procedure.

Production rollback tetap membutuhkan environment, authorization,
release approval, access control, artifact availability, database
compatibility assessment, dan operational evidence yang sesuai.

---

# 3. Rollback Status Classification

Rollback capability menggunakan klasifikasi berikut:

## DOCUMENTED

Procedure telah ditetapkan tetapi execution belum dilakukan.

## IMPLEMENTED

Komponen atau mechanism pendukung rollback tersedia pada repository atau
runtime.

## VALIDATED

Rollback capability telah dieksekusi dan memiliki objective evidence.

## NOT YET EVIDENCED

Capability telah didefinisikan atau tersedia secara konseptual tetapi
belum memiliki execution evidence yang memadai untuk scope tertentu.

---

# 4. Current Rollback Baseline

Repository dan existing governance menyediakan baseline berikut:

| Capability | Status |
|---|---|
| Git version control | IMPLEMENTED |
| Release version identification | IMPLEMENTED |
| Docker image/build mechanism | IMPLEMENTED |
| Deployment configuration | IMPLEMENTED |
| Database migration mechanism | IMPLEMENTED |
| Health validation mechanism | IMPLEMENTED |
| Rollback procedure | DOCUMENTED |
| Known-good release selection | DOCUMENTED |
| Database compatibility assessment | DOCUMENTED |
| Production rollback execution | NOT YET EVIDENCED |
| Production rollback validation | NOT YET EVIDENCED |
| Automated rollback | NOT YET EVIDENCED |
| Production post-rollback validation | NOT YET EVIDENCED |

Status tersebut merupakan evidence boundary dan bukan production readiness
certification.

---

# 5. Rollback Principles

MAJE rollback operations mengikuti prinsip:

- Recover to Known Good State
- Controlled Recovery
- Data Integrity First
- Evidence Based Recovery
- Minimal Additional Change
- Traceable Execution
- Approval Controlled
- No Unverified Production Claims

Rollback tidak boleh digunakan sebagai alasan untuk melakukan perubahan
tambahan yang tidak terkait dengan recovery.

---

# 6. Rollback Decision

Rollback harus dipertimbangkan apabila release menyebabkan:

- service failure;
- critical application error;
- unacceptable regression;
- severe performance degradation;
- critical security issue;
- failed post-deployment validation;
- migration or compatibility condition yang membuat release tidak aman.

Rollback bukan selalu tindakan pertama.

Operator harus terlebih dahulu menentukan apakah kondisi dapat dipulihkan
tanpa rollback melalui controlled remediation.

Decision flow:

Issue Detected
    ↓
Assess Severity
    ↓
Determine Immediate Risk
    ↓
Remediation Safe?
   /        \
 YES        NO
  ↓          ↓
Remediate   Consider Rollback
  ↓          ↓
Validate    Approval / Authorization
             ↓
          Rollback

Keputusan rollback harus mempertimbangkan impact terhadap application,
database, user sessions, persistent data, dan dependent services.

---

# 7. Rollback Preconditions

Sebelum rollback dilakukan, operator harus memverifikasi:

- failed release telah diidentifikasi;
- known-good release telah diidentifikasi;
- target environment telah dikonfirmasi;
- Git revision atau artifact identity tersedia;
- release history dapat ditelusuri;
- database compatibility telah dinilai;
- applicable backup requirement telah dinilai;
- rollback authorization tersedia;
- validation criteria telah ditentukan;
- recovery evidence dapat direkam.

Production rollback tidak boleh dilakukan tanpa required authorization.

---

# 8. Failed Release Identification

Record release yang akan di-rollback.

Minimum information:

- release version;
- Git revision;
- artifact identity where applicable;
- deployment date/time;
- target environment;
- observed failure;
- affected service;
- relevant incident or change reference.

Example:

```text
Environment: staging
Release: 1.2.0
Git Revision: <git-sha>
Issue: critical regression
Service: backend

Release identity harus diverifikasi sebelum rollback.

9. Known-Good Release Identification

Rollback harus menuju release atau artifact yang diketahui lebih stabil
berdasarkan available evidence.

Known-good release dapat diidentifikasi melalui:

previous approved release;
previous validated revision;
known-good container image;
release record;
deployment evidence.

Operator tidak boleh menebak target rollback.

Target rollback harus memiliki identity yang dapat ditelusuri.

10. Git Validation

Jika rollback menggunakan Git revision, validasi revision:

git status -sb
git rev-parse <known-good-revision>
git log -1 --format='%H%n%ad%n%s' --date=iso <known-good-revision>

Operator harus memastikan revision yang dipilih benar-benar merupakan
known-good target.

Working tree dan deployment source harus dikendalikan sesuai release
procedure.

Rollback evidence harus mencatat:

current failed revision;
target known-good revision;
release version;
date/time.
11. Artifact Validation

Jika deployment menggunakan container artifact, operator harus
mengidentifikasi artifact yang akan digunakan.

Minimum identity:

image name;
image tag;
immutable digest where available;
build revision;
release version.

Artifact harus diverifikasi sebelum deployment rollback.

Tag yang mutable tidak boleh dianggap sebagai sufficient immutable
identity apabila deployment architecture menyediakan digest-based identity.

12. Database Compatibility Assessment

Database rollback berbeda dari application rollback.

Sebelum rollback application version, operator harus menilai:

current database migration;
target release migration;
schema compatibility;
backward compatibility;
data format compatibility;
destructive migration impact;
application/database dependency.

Baseline migration command:

alembic current

Database migration rollback tidak boleh dilakukan hanya karena application
rollback diperlukan.

Jika database schema telah berubah, recovery strategy harus ditentukan
secara terpisah.

13. Backup and Recovery Consideration

Rollback yang berpotensi memengaruhi persistent data harus mempertimbangkan
backup and recovery requirement.

Related procedure:

OPS-003 — Backup & Restore Procedure

Existing EVIDENCE-005 validates isolated PostgreSQL backup and restore
execution.

Evidence tersebut tidak membuktikan production restore capability.

Production recovery decision harus mempertimbangkan actual production
backup availability dan recovery controls.

14. Rollback Authorization

Production rollback harus mengikuti applicable approval boundary.

HC-014 menetapkan release approval structure yang dapat mencakup:

Engineering Lead Approval;
QA Approval;
Product Approval where required.

Untuk incident kritis, emergency rollback dapat mengikuti emergency
authorization process apabila governance tersebut telah ditetapkan.

Approval state atau emergency authorization harus dicatat sebagai evidence.

15. Rollback Execution Boundary

Rollback execution harus dilakukan menggunakan controlled deployment
mechanism.

Baseline flow:

Identify Failed Release
↓
Identify Known-Good Release
↓
Validate Artifact / Revision
↓
Assess Database Compatibility
↓
Confirm Authorization
↓
Execute Rollback
↓
Health Validation
↓
Post-Rollback Validation
↓
Record Evidence

Current repository contains deployment configuration and release
mechanisms, tetapi tidak terdapat objective evidence bahwa production
rollback telah dieksekusi.

Current status:

Rollback Configuration
↓
IMPLEMENTED / DOCUMENTED

Production Rollback Execution
↓
NOT YET EVIDENCED

16. Container Rollback Consideration

Untuk containerized deployment, rollback dapat dilakukan dengan
mengembalikan service ke known-good image atau build revision.

Sebelum rollback:

verify target image;
verify target revision;
verify configuration compatibility;
verify database compatibility;
confirm service dependencies.

Setelah rollback:

inspect container state;
validate application health;
inspect application logs;
validate critical workflow where applicable.

Rollback image yang berhasil dijalankan tidak otomatis membuktikan seluruh
application workflow telah pulih.

17. Development Rollback Validation

Development rollback dapat digunakan untuk memvalidasi procedure dan
dependency compatibility sebelum production use.

Baseline configuration validation:

docker compose -f docker-compose.dev.yml config

Container state:

docker compose -f docker-compose.dev.yml ps

Application health:

curl -f http://localhost:8000/health

Development execution harus dicatat sebagai development evidence dan tidak
boleh direpresentasikan sebagai production rollback evidence.

18. Production Rollback Boundary

Production rollback merupakan controlled operational action.

Current status:

Production Rollback Procedure
        ↓
DOCUMENTED

Production Rollback Execution
        ↓
NOT YET EVIDENCED

Production Rollback Validation
        ↓
NOT YET EVIDENCED

Keberadaan procedure, Docker configuration, Git history, atau health
endpoint tidak dengan sendirinya membuktikan successful production rollback.

19. Health Validation After Rollback

Setelah rollback, health validation wajib dilakukan.

Gunakan:

curl -f http://localhost:8000/health

Container state dapat diperiksa dengan:

docker compose ps

Health validation harus memastikan:

service process active;
application endpoint responds;
dependency condition sesuai;
no immediate startup failure;
recent logs tidak menunjukkan critical failure.

Related procedure:

OPS-002 — Health Check Procedure

20. Post-Rollback Validation

Post-rollback validation minimal mencakup:

deployed revision;
release identity;
container state;
application health;
database connectivity;
migration state;
application logs;
critical application workflow where applicable;
monitoring state where available.

Flow:

Rollback
↓
Container Validation
↓
Application Health
↓
Database Validation
↓
Critical Workflow
↓
Monitoring
↓
Evidence

Rollback tidak dianggap operationally successful hanya karena container
berstatus running.

21. Rollback Failure Handling

Jika rollback gagal:

Detection
↓
Stop / Contain
↓
Inspect Logs
↓
Verify Target Revision / Artifact
↓
Assess Database Compatibility
↓
Determine Recovery Action
↓
Controlled Retry or Recovery
↓
Health Validation
↓
Record Result

Operator tidak boleh melakukan repeated uncontrolled rollback attempts.

Jika application rollback tidak compatible dengan current database state,
recovery strategy harus ditentukan sebelum tindakan berikutnya.

22. Database Rollback Boundary

Application rollback dan database rollback harus diperlakukan sebagai
dua tindakan berbeda.

Database rollback dapat memiliki risiko:

data loss;
schema incompatibility;
referential integrity issue;
migration dependency;
application incompatibility.

Karena itu database rollback harus memiliki explicit recovery assessment.

Jika schema migration bersifat destructive atau irreversible, application
rollback mungkin memerlukan forward-compatible remediation atau database
restore daripada migration downgrade.

Exact action harus mengikuti actual migration design dan recovery evidence.

23. Rollback and Backup Relationship

Rollback harus mempertimbangkan backup requirement apabila release
melibatkan:

schema change;
persistent data transformation;
destructive migration;
irreversible data modification.

Related procedure:

OPS-003 — Backup & Restore Procedure

Recovery decision harus membedakan:

Application Rollback
versus
Database Recovery

Keduanya tidak boleh dianggap equivalent.

24. Evidence Recording

Setiap material rollback execution harus menghasilkan evidence yang
mencatat:

date/time;
environment;
failed release;
failed Git revision;
target known-good release;
target Git revision;
artifact identity where applicable;
database migration state;
authorization;
rollback command or method;
rollback result;
health result;
post-rollback validation;
recovery action;
operator/responsible role where applicable;
limitations.

Evidence harus disimpan sesuai Evidence Governance.

25. Rollback Evidence Quality

Evidence rollback harus memungkinkan pihak lain menjawab:

apa yang gagal;
release mana yang gagal;
release mana yang menjadi target rollback;
mengapa target tersebut dipilih;
siapa atau role apa yang mengotorisasi;
bagaimana rollback dilakukan;
apakah health pulih;
apakah database tetap compatible;
apakah critical workflow kembali berfungsi;
apakah rollback benar-benar selesai.

Evidence yang hanya menyatakan "rollback successful" tanpa supporting
execution information tidak dianggap sufficient objective evidence.

26. Incident Relationship

Rollback yang dilakukan akibat incident harus terhubung dengan incident
record apabila applicable.

Incident flow:

Incident Detection
↓
Impact Assessment
↓
Rollback Decision
↓
Rollback
↓
Health Validation
↓
Service Recovery
↓
Root Cause Analysis
↓
Documentation

Rollback menyelesaikan immediate recovery condition tetapi tidak menggantikan
Root Cause Analysis.

27. Post-Rollback Review

Setelah rollback material, review harus mempertimbangkan:

cause of release failure;
detection effectiveness;
rollback decision;
rollback execution time;
recovery result;
database impact;
monitoring effectiveness;
missing controls;
preventive action.

Hasil review dapat digunakan untuk continuous improvement sesuai HC-014.

28. Current Validation Status

OPS-004 saat ini diklasifikasikan sebagai:

DOCUMENTED

Procedure ini grounded pada:

ARC-008;
HC-008;
HC-014;
OPS-001;
OPS-002;
OPS-003;
existing Git and container configuration.

Current evidence boundary:

Production rollback execution
NOT YET EVIDENCED

Production rollback validation
NOT YET EVIDENCED

Automated rollback
NOT YET EVIDENCED

Production post-rollback validation
NOT YET EVIDENCED

Tidak ada production rollback claim yang dibuat oleh dokumen ini.

29. Operational Limitations

OPS-004 bukan merupakan:

production rollback certification;
disaster recovery certification;
production availability certification;
database rollback certification;
incident readiness certification;
automated rollback certification.

Procedure ini hanya menetapkan operational baseline.

Actual production rollback capability harus divalidasi melalui execution
evidence pada target production architecture.

30. Related Documents

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
OPS-003 — Backup & Restore Procedure

Evidence:

EVIDENCE-005 — Backup & Restore Validation
EVIDENCE-013 — CI/CD Implementation Validation
31. Document History
Version	Date	Change
1.0	2026-08-27	Established baseline rollback procedure
