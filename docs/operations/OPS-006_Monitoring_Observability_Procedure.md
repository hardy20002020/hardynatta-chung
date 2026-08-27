# OPS-006 — Monitoring & Observability Procedure

**Document ID:** OPS-006
**Project:** MAJE Platform
**Document Area:** Operations
**Status:** Procedure Baseline Established
**Version:** 1.0
**Owner:** Engineering Team
**Last Updated:** 2026-08-27

---

# 1. Purpose

Dokumen ini mendefinisikan prosedur monitoring dan observability MAJE
Platform secara terkendali, dapat ditelusuri, dan berbasis evidence.

Procedure ini digunakan untuk:

- application health observation;
- container observation;
- database observation;
- application log inspection;
- operational signal identification;
- incident detection;
- post-deployment observation;
- failure investigation;
- recovery observation;
- evidence recording.

Procedure ini menerjemahkan requirement dari:

- ARC-008 — Deployment Architecture
- HC-008 — Deployment Governance
- HC-009 — Monitoring & Observability Governance
- HC-014 — Release Management

menjadi operational procedure yang dapat digunakan untuk monitoring
dan observability validation.

Dokumen ini tidak menyatakan bahwa production monitoring stack,
production alerting, metrics platform, tracing platform, atau operational
dashboard telah tersedia atau tervalidasi apabila belum terdapat
implementation dan execution evidence yang sesuai.

---

# 2. Scope

Procedure ini mencakup:

- monitoring principles;
- health signals;
- container state;
- PostgreSQL state;
- application logs;
- metrics boundary;
- tracing boundary;
- alerting boundary;
- incident detection;
- operational dashboard boundary;
- deployment observation;
- post-deployment monitoring;
- monitoring failure investigation;
- evidence recording;
- production monitoring boundary.

Procedure ini berlaku sebagai baseline operational monitoring and
observability procedure.

Production monitoring tetap membutuhkan environment, infrastructure,
access controls, monitoring platform, retention controls, alert routing,
on-call responsibility, dan operational evidence yang sesuai.

---

# 3. Monitoring and Observability Status Classification

Monitoring capability menggunakan klasifikasi berikut:

## DOCUMENTED

Requirement atau procedure telah didokumentasikan.

## IMPLEMENTED

Capability atau mechanism tersedia pada repository atau runtime.

## VALIDATED

Capability telah dieksekusi dan memiliki objective evidence.

## NOT YET EVIDENCED

Capability telah didefinisikan atau tersedia secara konseptual tetapi
belum memiliki execution evidence yang memadai untuk scope tertentu.

---

# 4. Current Monitoring and Observability Baseline

Repository dan existing evidence menunjukkan baseline berikut:

| Capability | Status |
|---|---|
| Backend application health endpoint | IMPLEMENTED |
| PostgreSQL container healthcheck | IMPLEMENTED |
| Backend container healthcheck | IMPLEMENTED |
| Compose dependency health | IMPLEMENTED |
| Application log output | IMPLEMENTED |
| Container log inspection | IMPLEMENTED |
| Development health observation | IMPLEMENTED |
| Production healthcheck configuration | IMPLEMENTED |
| Production monitoring stack | NOT YET EVIDENCED |
| Production metrics collection | NOT YET EVIDENCED |
| Production tracing implementation | NOT YET EVIDENCED |
| Production alerting implementation | NOT YET EVIDENCED |
| Production operational dashboard | NOT YET EVIDENCED |
| Production incident alert routing | NOT YET EVIDENCED |
| Production monitoring execution | NOT YET EVIDENCED |
| Production monitoring SLA/SLO validation | NOT YET EVIDENCED |

Status tersebut merupakan evidence boundary dan bukan production readiness
certification.

---

# 5. Monitoring Principles

MAJE monitoring dan observability mengikuti prinsip:

- Evidence Based Observation
- Actionable Signals
- Controlled Access
- Traceable Events
- Security-Aware Logging
- Least Privilege
- Failure Visibility
- No Unverified Production Claims

Monitoring harus menghasilkan signal yang dapat digunakan untuk
mendeteksi, memahami, atau menginvestigasi operational condition.

Monitoring configuration tidak boleh dianggap sebagai monitoring
execution evidence hanya karena configuration file tersedia.

---

# 6. Observability Layers

Baseline observability MAJE dapat dipahami sebagai beberapa layer:

Application
    ↓
Health Endpoint / Application Logs

Container
    ↓
Container State / Healthcheck / Logs

Database
    ↓
PostgreSQL Health / Database Logs

Deployment
    ↓
Deployment Result / Health Validation

Operations
    ↓
Monitoring / Alerting / Incident Detection

Setiap layer memiliki scope yang berbeda.

Application health tidak otomatis membuktikan container, database,
monitoring, atau business workflow dalam kondisi sehat.

Container health tidak otomatis membuktikan complete application
availability.

Database health tidak otomatis membuktikan application health.

---

# 7. Application Health Signal

MAJE menyediakan application health endpoint:

```text
GET /health

Implementation berada pada:

backend/app/main.py

Current implementation:

@app.get("/health")
def health():
    return {
        "success": True,
        "message": "MAJE healthy",
    }

Current response:

{
  "success": true,
  "message": "MAJE healthy"
}

Endpoint tersebut merupakan application-level operational signal.

Successful response menunjukkan bahwa endpoint application dapat
memberikan response pada environment yang sedang diuji.

Endpoint tersebut tidak dengan sendirinya membuktikan:

seluruh dependency sehat;
seluruh database operation berhasil;
seluruh business workflow berhasil;
production availability target terpenuhi;
monitoring stack aktif;
alerting aktif.
8. Container Observation

Container state merupakan operational signal yang dapat digunakan untuk
menilai lifecycle dan health service.

Baseline command:

docker compose ps

Untuk detail container:

docker inspect <container-name>

Operator dapat menggunakan informasi:

running state;
restart state;
health state;
container uptime;
configured healthcheck;
exit condition.

Repeated container restart harus diperlakukan sebagai signal yang
memerlukan investigation.

Restart policy tidak boleh dianggap sebagai pengganti root-cause
investigation.

9. PostgreSQL Observation

PostgreSQL merupakan dependency utama backend pada current deployment
baseline.

PostgreSQL healthcheck menggunakan:

pg_isready

Container state dapat diperiksa melalui:

docker compose ps postgres

PostgreSQL logs dapat diperiksa melalui:

docker compose logs --tail=200 postgres

Readiness dapat divalidasi melalui:

docker compose exec postgres pg_isready -U postgres -d maje

Database health signal harus dibedakan dari:

database integrity;
migration state;
backup availability;
restore capability;
production disaster recovery.
10. Application Log Observation

Application logs merupakan operational signal untuk investigation dan
failure analysis.

Baseline command:

docker compose logs --tail=200 backend

Operator harus memperhatikan:

startup failures;
import failures;
configuration errors;
database connection errors;
authentication errors;
authorization failures;
unexpected exceptions;
repeated error patterns;
abnormal restart patterns.

Logs yang mengandung sensitive information harus diperlakukan sesuai
security governance.

Credential, secret, token, atau sensitive authentication material tidak
boleh sengaja dicatat sebagai operational evidence.

11. Log Retention Boundary

Current repository baseline menyediakan application dan container log
access melalui runtime mechanisms.

Namun keberadaan runtime logs tidak membuktikan bahwa production log
retention telah memenuhi requirement tertentu.

Current status:

Production Log Retention
↓
NOT YET EVIDENCED

Production log aggregation, centralized logging, retention duration,
access auditing, archival, dan deletion policy memerlukan evidence
tersendiri apabila diwajibkan.

12. Metrics Boundary

Metrics dapat digunakan untuk mengamati:

request volume;
response latency;
error rate;
resource utilization;
database condition;
container condition;
service availability.

Namun current repository evidence tidak digunakan untuk menyatakan
production metrics collection telah implemented atau validated.

Current status:

Production Metrics Collection
↓
NOT YET EVIDENCED

Metrics platform implementation harus memiliki:

defined metrics;
collection mechanism;
retention;
access control;
validation evidence.
13. Tracing Boundary

Distributed tracing dapat digunakan apabila MAJE architecture dan
workload membutuhkan visibility terhadap request flow antar service.

Current repository baseline tidak digunakan untuk menyatakan production
distributed tracing telah implemented atau validated.

Current status:

Production Tracing
↓
NOT YET EVIDENCED

Tracing implementation, instrumentation, storage, sampling, and
operational use memerlukan evidence tersendiri apabila diterapkan.

14. Alerting Boundary

Alerting merupakan mekanisme untuk mengubah operational signal menjadi
notification atau action trigger.

Potential alert conditions dapat mencakup:

service unavailable;
healthcheck failure;
repeated container restart;
database unavailable;
elevated error rate;
abnormal latency;
resource exhaustion;
critical security event.

Current repository evidence tidak membuktikan production alerting
implementation.

Current status:

Production Alerting
↓
NOT YET EVIDENCED

Alerting readiness membutuhkan evidence terhadap:

alert condition;
threshold;
evaluation mechanism;
notification destination;
responsible role;
alert test;
escalation path.
15. Operational Dashboard Boundary

Operational dashboard dapat digunakan untuk memberikan consolidated
visibility terhadap service condition.

Potential dashboard signals:

service availability;
health state;
error rate;
request volume;
latency;
database condition;
infrastructure condition;
active incidents.

Current repository evidence tidak membuktikan production operational
dashboard telah implemented atau validated.

Current status:

Production Operational Dashboard
↓
NOT YET EVIDENCED

16. Development Monitoring

Development monitoring dapat dilakukan menggunakan Compose runtime.

Configuration validation:

docker compose -f docker-compose.dev.yml config

Container observation:

docker compose -f docker-compose.dev.yml ps

Application health:

curl -f http://localhost:8000/health

Backend logs:

docker compose -f docker-compose.dev.yml logs --tail=200 backend

PostgreSQL logs:

docker compose -f docker-compose.dev.yml logs --tail=200 postgres

Development observation digunakan untuk:

troubleshooting;
validation;
development recovery;
deployment preparation.

Development observation tidak boleh direpresentasikan sebagai production
monitoring evidence.

17. Production Monitoring Boundary

Production Compose configuration menyediakan healthcheck mechanisms.

Configuration dapat diperiksa dengan:

docker compose -f docker-compose.prod.yml config

Namun configuration existence tidak sama dengan production monitoring
execution.

Current status:

Production Health Signal Configuration
↓
IMPLEMENTED

Production Monitoring Stack
↓
NOT YET EVIDENCED

Production Alerting
↓
NOT YET EVIDENCED

Production Dashboard
↓
NOT YET EVIDENCED

Production Monitoring Execution
↓
NOT YET EVIDENCED

Tidak boleh menyatakan production service is monitored hanya berdasarkan
keberadaan healthcheck configuration.

18. Deployment Monitoring

Monitoring merupakan bagian dari controlled deployment lifecycle.

Baseline:

Deployment
↓
Health Validation
↓
Log Observation
↓
Error Observation
↓
Critical Workflow
↓
Monitoring
↓
Evidence

Post-deployment monitoring harus dikaitkan dengan:

release version;
Git revision;
target environment;
deployment timestamp;
health result;
observed errors;
recovery actions.
19. Post-Deployment Observation

Setelah deployment, operator harus melakukan observation terhadap
service condition.

Minimum observation:

deployed revision;
container state;
application health;
database dependency;
recent application logs;
recent database logs;
critical application behavior where applicable;
monitoring status where available.

Jika monitoring platform belum tersedia, manual observation harus
didokumentasikan sebagai manual operational validation dan tidak
direpresentasikan sebagai automated monitoring.

20. Incident Detection

Operational incident dapat dideteksi melalui:

failed healthcheck;
application error;
database failure;
repeated container restart;
deployment failure;
user-visible service failure;
security signal;
monitoring alert apabila tersedia.

Detection flow:

Signal
↓
Detection
↓
Classification
↓
Investigation
↓
Containment
↓
Recovery
↓
Validation
↓
Evidence

Incident handling selanjutnya mengikuti:

OPS-005 — Incident Response Procedure

21. Monitoring Failure Investigation

Jika monitoring signal menunjukkan failure:

Detection
↓
Identify Signal
↓
Identify Service
↓
Inspect Container
↓
Inspect Application Logs
↓
Inspect Database Health
↓
Determine Cause
↓
Recover / Restart / Rollback
↓
Revalidate
↓
Record Evidence

Operator harus menghindari repeated uncontrolled restart atau deployment
attempt.

Monitoring signal harus digunakan untuk membantu investigation, bukan
sekadar untuk menghasilkan notification.

22. Healthcheck Failure

Jika backend healthcheck gagal:

docker compose ps backend

Periksa logs:

docker compose logs --tail=200 backend

Validasi endpoint:

curl -f http://localhost:8000/health

Jika dependency database dicurigai:

docker compose ps postgres

dan:

docker compose logs --tail=200 postgres

Healthcheck failure harus diperlakukan sebagai operational signal
sampai root cause ditentukan.

23. Database Monitoring Failure

Jika PostgreSQL menunjukkan unhealthy condition:

docker compose ps postgres

Periksa:

docker compose logs --tail=200 postgres

Validasi:

docker compose exec postgres pg_isready -U postgres -d maje

Operator harus menentukan apakah condition berasal dari:

PostgreSQL startup;
connection issue;
configuration;
resource condition;
storage;
migration;
runtime failure.

Recovery action harus mempertimbangkan data integrity.

24. Monitoring and Security

Monitoring harus mengikuti security governance.

Operator harus memastikan:

logs tidak sengaja mengekspos credentials;
secrets tidak dikirim ke dashboard tanpa control;
monitoring access menggunakan least privilege;
privileged operational data dibatasi;
audit-sensitive actions dapat ditelusuri;
log access mengikuti authorization.

Monitoring data dapat mengandung operationally sensitive information
dan harus diperlakukan sesuai applicable security controls.

25. Monitoring Evidence

Material monitoring validation harus mencatat:

date/time;
environment;
Git revision;
service;
monitoring signal;
command or validation method;
result;
relevant logs;
incident or recovery action;
responsible role where applicable;
limitations.

Example:

Environment: Development
Service: Backend
Revision: <git-sha>
Signal: GET /health
Method: curl -f http://localhost:8000/health
Result: PASS
Observation: Application responded successfully

Evidence harus disimpan sesuai Evidence Governance.

26. Evidence Classification

Monitoring evidence harus dibedakan menjadi:

Configuration Evidence

Membuktikan bahwa monitoring atau healthcheck configuration tersedia.

Execution Evidence

Membuktikan bahwa monitoring mechanism benar-benar dijalankan.

Operational Evidence

Membuktikan bahwa signal digunakan dalam operational activity.

Production Evidence

Membuktikan execution pada production environment.

Configuration evidence tidak boleh diperlakukan sebagai production
execution evidence.

27. Relationship to Health Check Procedure

Monitoring menggunakan health signal yang didefinisikan dalam:

OPS-002 — Health Check Procedure

OPS-002 mendefinisikan:

application health;
PostgreSQL health;
container health;
dependency health;
health failure investigation.

OPS-006 memperluas health signal tersebut menjadi operational
monitoring and observability context.

Healthcheck tetap merupakan salah satu signal, bukan keseluruhan
observability system.

28. Relationship to Incident Response

Monitoring dan observability mendukung incident detection dan
investigation.

Incident response mengikuti:

OPS-005 — Incident Response Procedure

Baseline flow:

Monitoring Signal
↓
Incident Detection
↓
Incident Response
↓
Recovery
↓
Health Validation
↓
Evidence

Monitoring tidak menggantikan incident response procedure.

29. Relationship to Rollback

Monitoring signals dapat menjadi input untuk rollback decision.

Potential rollback triggers:

deployment health failure;
repeated application failure;
critical workflow failure;
persistent dependency failure;
severe regression.

Rollback harus mengikuti:

OPS-004 — Rollback Procedure

Monitoring signal tidak dengan sendirinya memberikan authorization
untuk production rollback.

Required approval dan release governance tetap berlaku.

30. Relationship to Backup and Recovery

Monitoring dapat memberikan signal bahwa recovery action mungkin
diperlukan.

Recovery execution harus mengikuti:

OPS-003 — Backup & Restore Procedure

Monitoring failure tidak membuktikan backup availability.

Successful backup validation tidak membuktikan monitoring availability.

Kedua capability memiliki evidence boundary masing-masing.

31. Production Alert Escalation Boundary

Jika production alerting diterapkan, alert harus memiliki:

severity;
trigger condition;
notification route;
responsible role;
escalation path;
acknowledgement expectation;
resolution recording.

Current repository evidence tidak membuktikan production alert escalation
telah implemented atau validated.

Current status:

Production Alert Escalation
↓
NOT YET EVIDENCED

32. Monitoring Retention and Access Boundary

Production observability data harus memiliki controls yang sesuai untuk:

retention;
access;
confidentiality;
integrity;
availability;
archival;
deletion.

Current baseline tidak menetapkan arbitrary retention period.

Retention requirement harus mengikuti:

business requirement;
security governance;
infrastructure capability;
applicable legal/regulatory requirement;
operational requirement.
33. Current Validation Status

OPS-006 saat ini diklasifikasikan sebagai:

DOCUMENTED

Repository implementation yang mendukung procedure ini meliputi:

/health application endpoint;
PostgreSQL healthcheck;
backend container healthcheck;
Compose dependency health;
application/container log access;
development and production Compose configuration.

Existing implementation mendukung monitoring primitives.

Namun capabilities berikut tetap:

Production Monitoring Stack
NOT YET EVIDENCED

Production Metrics Collection
NOT YET EVIDENCED

Production Tracing
NOT YET EVIDENCED

Production Alerting
NOT YET EVIDENCED

Production Operational Dashboard
NOT YET EVIDENCED

Production Alert Escalation
NOT YET EVIDENCED

Production Monitoring Execution
NOT YET EVIDENCED

34. Operational Limitations

OPS-006 bukan merupakan:

production monitoring certification;
production observability certification;
metrics certification;
tracing certification;
alerting certification;
dashboard certification;
SLA certification;
SLO certification;
production incident readiness certification.

Current validated evidence tidak digunakan untuk menyatakan bahwa
production monitoring environment telah tersedia.

Healthcheck configuration merupakan monitoring primitive dan bukan
complete monitoring platform.

35. Related Documents

Architecture:

ARC-001 — Master System Architecture
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
OPS-005 — Incident Response Procedure

Evidence:

EVIDENCE-005 — Backup & Restore Validation
EVIDENCE-013 — CI/CD Implementation Validation

36. Document History
Version	Date	Change
1.0	2026-08-27	Established baseline monitoring and observability procedure
