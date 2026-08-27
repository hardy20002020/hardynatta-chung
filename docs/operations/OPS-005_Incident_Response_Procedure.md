# OPS-005 — Incident Response Procedure

**Document ID:** OPS-005
**Project:** MAJE Platform
**Document Area:** Operations
**Status:** Procedure Baseline Established
**Version:** 1.0
**Owner:** Engineering Team
**Last Updated:** 2026-08-27

---

# 1. Purpose

Dokumen ini mendefinisikan prosedur incident response MAJE Platform secara
terkendali, dapat ditelusuri, dan berbasis evidence.

Procedure ini digunakan untuk:

- incident detection;
- incident triage;
- impact assessment;
- containment;
- recovery;
- health validation;
- root cause analysis;
- post-incident review;
- evidence recording;
- corrective and preventive action.

Procedure ini menerjemahkan requirement dari:

- HC-008 — Deployment Governance
- HC-009 — Monitoring & Observability Governance
- HC-014 — Release Management
- OPS-001 — Deployment Procedure
- OPS-002 — Health Check Procedure
- OPS-003 — Backup & Restore Procedure
- OPS-004 — Rollback Procedure

Dokumen ini tidak menyatakan bahwa production incident response telah
dieksekusi atau divalidasi apabila belum terdapat objective execution
evidence.

---

# 2. Scope

Procedure ini mencakup:

- incident identification;
- initial assessment;
- severity classification;
- service impact assessment;
- containment;
- investigation;
- recovery decision;
- health validation;
- rollback consideration;
- backup and restore consideration;
- root cause analysis;
- post-incident review;
- evidence recording;
- communication;
- incident closure;
- operational limitations.

Procedure ini berlaku sebagai baseline operational incident response
procedure.

Production incident response tetap membutuhkan operational monitoring,
alerting, access control, responsible roles, communication channels,
authorization, dan incident evidence yang sesuai.

---

# 3. Incident Status Classification

Incident response capability menggunakan klasifikasi berikut:

## DOCUMENTED

Procedure atau requirement telah didokumentasikan.

## IMPLEMENTED

Supporting mechanism tersedia pada repository atau runtime.

## VALIDATED

Incident response capability telah dieksekusi dan memiliki objective
evidence.

## NOT YET EVIDENCED

Capability telah didefinisikan atau tersedia secara konseptual tetapi
belum memiliki execution evidence yang memadai untuk scope tertentu.

---

# 4. Current Incident Response Baseline

Repository, governance, dan existing evidence menunjukkan baseline berikut:

| Capability | Status |
|---|---|
| Application logging | IMPLEMENTED |
| Application health endpoint | IMPLEMENTED |
| Container healthchecks | IMPLEMENTED |
| Git traceability | IMPLEMENTED |
| Deployment procedure | DOCUMENTED |
| Health check procedure | DOCUMENTED |
| Backup and restore procedure | DOCUMENTED |
| Rollback procedure | DOCUMENTED |
| Incident response procedure | DOCUMENTED |
| Production monitoring stack | NOT YET EVIDENCED |
| Production alerting implementation | NOT YET EVIDENCED |
| Production incident execution | NOT YET EVIDENCED |
| Production incident communication execution | NOT YET EVIDENCED |
| Production incident recovery execution | NOT YET EVIDENCED |
| Production post-incident review execution | NOT YET EVIDENCED |

Status tersebut merupakan evidence boundary dan bukan production readiness
certification.

---

# 5. Incident Response Principles

MAJE incident response mengikuti prinsip:

- Detect Early
- Assess Before Acting
- Contain Before Escalating Impact
- Data Integrity First
- Controlled Recovery
- Evidence Based Investigation
- Traceable Actions
- Least Privilege
- Clear Responsibility
- No Unverified Production Claims

Incident response harus mengutamakan stabilisasi layanan dan perlindungan
data sebelum melakukan perubahan tambahan yang tidak diperlukan.

---

# 6. Incident Lifecycle

Baseline incident lifecycle:

Detection
    ↓
Triage
    ↓
Impact Assessment
    ↓
Containment
    ↓
Investigation
    ↓
Recovery Decision
    ↓
Recovery
    ↓
Health Validation
    ↓
Monitoring
    ↓
Root Cause Analysis
    ↓
Post-Incident Review
    ↓
Closure

Setiap tahap harus menghasilkan informasi yang cukup untuk mendukung tahap
berikutnya.

---

# 7. Incident Detection

Incident dapat terdeteksi melalui:

- application error;
- failed health check;
- container failure;
- database failure;
- abnormal performance;
- security event;
- user report;
- deployment validation failure;
- monitoring alert apabila monitoring tersedia.

Current repository menyediakan health endpoint dan container healthcheck.

Namun production monitoring dan alerting execution belum memiliki evidence
yang memadai dalam current baseline.

Incident detection harus mencatat:

- detection date/time;
- detection source;
- affected service;
- initial symptom;
- environment;
- initial severity assessment.

---

# 8. Initial Triage

Initial triage bertujuan menentukan apakah kondisi merupakan incident dan
berapa besar dampaknya.

Operator harus menentukan:

- affected service;
- affected environment;
- observed symptom;
- start time if known;
- current availability;
- potential data impact;
- potential security impact;
- deployment relation;
- immediate recovery option.

Triage tidak boleh langsung mengubah sistem tanpa memahami impact kecuali
tindakan containment diperlukan untuk mencegah kerusakan lebih lanjut.

---

# 9. Incident Severity

Severity dapat digunakan sebagai baseline:

| Severity | General Condition |
|---|---|
| Critical | layanan utama unavailable atau risiko data/security sangat tinggi |
| High | fungsi penting terganggu secara signifikan |
| Medium | fungsi terbatas terganggu tetapi service utama masih tersedia |
| Low | dampak kecil atau workaround tersedia |

Severity harus ditentukan berdasarkan actual impact dan business
criticality.

Nilai severity tidak boleh digunakan tanpa mempertimbangkan konteks
operasional.

---

# 10. Impact Assessment

Impact assessment harus mempertimbangkan:

- user impact;
- service availability;
- data integrity;
- database condition;
- security exposure;
- performance;
- affected release;
- affected environment;
- dependent services;
- recovery complexity.

Operator harus membedakan:

Observed Impact
versus
Potential Impact

Assessment harus diperbarui apabila informasi baru tersedia.

---

# 11. Immediate Containment

Containment bertujuan membatasi perluasan impact.

Possible controlled actions:

- stop affected deployment;
- disable affected functionality where supported;
- isolate affected service;
- prevent repeated failing operations;
- suspend further release activity;
- rollback known-bad release;
- protect affected database;
- restrict privileged access.

Containment action harus dicatat.

Operator tidak boleh melakukan destructive action tanpa memahami impact
dan recovery consequence.

---

# 12. Deployment-Related Incident

Jika incident berkaitan dengan deployment:

Deployment Failure
        ↓
Validate Current Revision
        ↓
Assess Impact
        ↓
Contain
        ↓
Determine Remediation or Rollback
        ↓
Health Validation
        ↓
Post-Incident Review

Related procedures:

- OPS-001 — Deployment Procedure
- OPS-002 — Health Check Procedure
- OPS-004 — Rollback Procedure

CI success tidak menghilangkan kemungkinan runtime incident.

---

# 13. Health Check Failure

Jika incident terdeteksi melalui health check:

```bash
curl -f http://localhost:8000/health

Periksa container state:

docker compose ps

Periksa backend logs:

docker compose logs --tail=200 backend

Jika database dependency dicurigai:

docker compose ps postgres
docker compose logs --tail=200 postgres

Health investigation harus menentukan apakah failure berasal dari:

application process;
configuration;
database dependency;
container runtime;
resource condition;
deployment change;
other dependency.

Related procedure:

OPS-002 — Health Check Procedure

14. Application Investigation

Application investigation dapat mencakup:

startup errors;
import errors;
configuration errors;
runtime exceptions;
failed requests;
authentication failures;
authorization failures;
dependency failures;
resource-related errors.

Relevant logs harus dipertahankan sebagai evidence apabila diperlukan.

Investigation harus menggunakan least-privilege access sesuai security
governance.

15. Database Incident Investigation

Jika incident berkaitan dengan database:

verify database identity;
verify database availability;
inspect database logs;
inspect migration state;
assess transaction failures;
assess storage condition;
assess data integrity risk.

Baseline migration validation:

alembic current

Database recovery decision harus mempertimbangkan OPS-003.

Jangan melakukan database restore atau migration downgrade hanya karena
application service mengalami error.

16. Security-Related Incident

Security-related incident harus mempertimbangkan:

unauthorized access;
credential exposure;
privilege escalation;
suspicious activity;
authentication failure;
authorization failure;
audit trail.

Jika terdapat risiko security, containment dapat mencakup:

revoke affected access;
isolate affected service;
stop affected deployment;
preserve relevant logs;
escalate according to applicable security governance.

Security incident handling harus tetap menjaga evidence integrity.

17. Recovery Decision

Recovery action dipilih berdasarkan root symptom, impact, dan available
evidence.

Possible recovery actions:

configuration correction;
service restart;
dependency recovery;
controlled remediation;
application rollback;
database recovery;
restore from validated backup where applicable.

Decision flow:

Incident
↓
Assess Cause / Risk
↓
Safe Remediation?
/ YES NO
↓ ↓
Fix Rollback / Recovery
↓ ↓
Validate Validate

Recovery action harus memiliki alasan yang dapat ditelusuri.

18. Rollback Relationship

Rollback dapat digunakan sebagai incident recovery action apabila incident
berkaitan dengan a known-bad release.

Related procedure:

OPS-004 — Rollback Procedure

Sebelum rollback:

identify failed release;
identify known-good release;
assess database compatibility;
verify authorization;
define validation criteria.

Rollback tidak boleh dianggap berhasil hanya karena deployment command
selesai.

Health dan post-rollback validation tetap diperlukan.

19. Backup and Restore Relationship

Jika incident memerlukan database recovery:

Related procedure:

OPS-003 — Backup & Restore Procedure

Recovery assessment harus menentukan:

approved backup identity;
recovery target;
recovery point;
data impact;
authorization;
validation criteria.

EVIDENCE-005 memvalidasi isolated PostgreSQL backup and restore execution.

Evidence tersebut tidak membuktikan production restore capability.

Production database recovery tetap membutuhkan actual production evidence.

20. Recovery Execution

Recovery harus dilakukan menggunakan controlled action.

Baseline:

Incident
↓
Approved Recovery Action
↓
Execution
↓
Health Validation
↓
Critical Workflow Validation
↓
Monitoring
↓
Recovery Evidence

Operator harus mencatat:

recovery action;
start/end time;
responsible role;
target environment;
affected revision;
resulting revision or state;
validation result.
21. Health Validation After Recovery

Setelah recovery:

curl -f http://localhost:8000/health

Periksa:

application response;
container state;
dependency state;
application logs;
migration state where applicable.

Related procedure:

OPS-002 — Health Check Procedure

Health recovery tidak otomatis membuktikan seluruh business workflow
berfungsi.

Critical workflow validation harus dilakukan apabila incident scope
memerlukannya.

22. Monitoring After Recovery

Setelah recovery, sistem harus diobservasi untuk memastikan incident tidak
segera kembali.

Monitoring dapat mencakup:

error rate;
response latency;
request failures;
database errors;
resource utilization;
health state.

Current production monitoring stack belum memiliki execution evidence.

Karena itu monitoring requirement harus disesuaikan dengan actual
environment capability.

23. Incident Communication

Material incident harus memiliki communication record apabila applicable.

Communication dapat mencakup:

incident detected;
impact summary;
containment status;
recovery status;
service restored;
follow-up action.

Communication harus:

factual;
time-aware;
traceable;
tidak membuat klaim yang belum diverifikasi.

Production communication channels dan escalation matrix belum dinyatakan
validated oleh dokumen ini.

24. Evidence Preservation

Incident evidence dapat mencakup:

timestamps;
Git revision;
deployment record;
health results;
application logs;
database logs;
container state;
commands executed;
recovery actions;
approval records;
screenshots or relevant artifacts where applicable.

Evidence harus dipertahankan sesuai Evidence Governance.

Operator harus menghindari perubahan atau penghapusan evidence yang dapat
menghambat investigation.

25. Incident Record

Setiap material incident sebaiknya memiliki incident record dengan minimum:

Incident ID:
Date/Time:
Environment:
Affected Service:
Severity:
Detection Source:
Observed Impact:
Current Release:
Known-Good Release:
Containment:
Recovery Action:
Health Result:
Post-Recovery Result:
Root Cause:
Corrective Action:
Responsible Role:
Closure Date:
Limitations:

Incident record harus dapat menghubungkan incident dengan release,
deployment, recovery, dan evidence terkait.

26. Root Cause Analysis

Setelah immediate recovery, lakukan Root Cause Analysis (RCA) apabila
incident material.

RCA harus menjawab:

what happened;
when it happened;
what changed;
why it happened;
why it was not prevented;
why it was or was not detected earlier;
what recovered the service;
what will prevent recurrence.

RCA tidak boleh berhenti pada symptom.

Root cause harus dibedakan dari contributing factors.

27. Corrective and Preventive Actions

Hasil RCA dapat menghasilkan:

code fix;
configuration correction;
test improvement;
monitoring improvement;
alert improvement;
deployment control improvement;
documentation improvement;
security control improvement;
backup/recovery improvement.

Setiap corrective action harus memiliki owner dan tracking mechanism
apabila applicable.

28. Post-Incident Review

Post-incident review mengevaluasi:

detection;
triage;
containment;
recovery;
rollback decision;
health validation;
communication;
evidence quality;
RCA;
corrective actions.

Tujuannya bukan hanya mencari kesalahan individu, tetapi meningkatkan
system resilience dan operational process.

29. Incident Closure

Incident dapat ditutup apabila:

service condition telah stabil;
recovery telah divalidasi;
immediate risk telah ditangani;
required evidence telah dikumpulkan;
RCA telah dilakukan apabila required;
corrective actions telah dicatat;
responsible role menyetujui closure.

Incident tidak boleh ditutup hanya karena service kembali running jika
required validation belum selesai.

30. Production Incident Boundary

Production incident response merupakan controlled operational capability.

Current status:

Incident Response Procedure
        ↓
DOCUMENTED

Production Incident Detection
        ↓
NOT YET EVIDENCED

Production Incident Recovery
        ↓
NOT YET EVIDENCED

Production Post-Incident Review
        ↓
NOT YET EVIDENCED

Keberadaan procedure dan repository health mechanisms tidak membuktikan
bahwa production incident response telah dieksekusi.

31. Current Validation Status

OPS-005 saat ini diklasifikasikan sebagai:

DOCUMENTED

Procedure ini grounded pada:

HC-008;
HC-009;
HC-014;
OPS-001;
OPS-002;
OPS-003;
OPS-004;
existing application, container, Git, and database mechanisms.

Current evidence boundary:

Production incident execution
NOT YET EVIDENCED

Production incident communication execution
NOT YET EVIDENCED

Production incident recovery execution
NOT YET EVIDENCED

Production post-incident review execution
NOT YET EVIDENCED

Production monitoring and alerting execution
NOT YET EVIDENCED

Tidak ada production incident readiness claim yang dibuat oleh dokumen ini.

32. Operational Limitations

OPS-005 bukan merupakan:

production incident readiness certification;
SLA certification;
SLO certification;
monitoring certification;
alerting certification;
disaster recovery certification;
security incident certification;
production recovery certification.

Procedure ini menetapkan operational baseline.

Actual production incident capability harus divalidasi melalui execution
evidence pada target production environment.

33. Related Documents

Architecture:

ARC-001 — Master System Architecture
ARC-002 — Backend Architecture
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
OPS-004 — Rollback Procedure

Evidence:

EVIDENCE-005 — Backup & Restore Validation
EVIDENCE-013 — CI/CD Implementation Validation
34. Document History
Version	Date	Change
1.0	2026-08-27	Established baseline incident response procedure
