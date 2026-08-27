# OPS-002 — Health Check Procedure

**Document ID:** OPS-002
**Project:** MAJE Platform
**Document Area:** Operations
**Status:** Procedure Baseline Established
**Version:** 1.0
**Owner:** Engineering Team
**Last Updated:** 2026-08-27

---

# 1. Purpose

Dokumen ini mendefinisikan prosedur health check MAJE Platform secara
terkendali, dapat ditelusuri, dan berbasis evidence.

Procedure ini digunakan untuk memvalidasi bahwa application service,
database dependency, dan container runtime berada dalam kondisi yang
dapat diobservasi melalui health mechanisms yang tersedia.

Procedure ini menerjemahkan requirement dari:

- ARC-002 — Backend Architecture
- ARC-005 — Database Architecture
- ARC-008 — Deployment Architecture
- HC-008 — Deployment Governance
- HC-009 — Monitoring & Observability Governance

menjadi operational procedure untuk health validation.

Dokumen ini tidak menyatakan production availability atau production
monitoring readiness apabila capability tersebut belum memiliki execution
evidence yang sesuai.

---

# 2. Scope

Procedure ini mencakup:

- application health endpoint;
- PostgreSQL health validation;
- Docker container healthcheck;
- Compose dependency health;
- development health validation;
- deployment health validation;
- post-deployment health validation;
- health failure investigation;
- recovery consideration;
- evidence recording;
- operational limitations.

Procedure ini berlaku sebagai baseline operational health procedure.

Production health validation tetap membutuhkan environment, authorization,
network access, credentials, monitoring controls, dan operational evidence
yang sesuai.

---

# 3. Health Status Classification

Health capability menggunakan klasifikasi berikut:

## DOCUMENTED

Procedure atau requirement telah didokumentasikan.

## IMPLEMENTED

Health mechanism tersedia pada repository atau runtime configuration.

## VALIDATED

Health mechanism telah dieksekusi dan memiliki objective evidence.

## NOT YET EVIDENCED

Capability telah didefinisikan atau tersedia secara konseptual tetapi
belum memiliki execution evidence yang memadai untuk scope tertentu.

---

# 4. Current Health Baseline

Repository saat ini menyediakan:

| Capability | Status |
|---|---|
| Backend `/health` endpoint | IMPLEMENTED |
| PostgreSQL Docker healthcheck | IMPLEMENTED |
| Backend Docker healthcheck | IMPLEMENTED |
| Development Compose healthchecks | IMPLEMENTED |
| Production Compose healthchecks | IMPLEMENTED |
| PostgreSQL healthy dependency condition | IMPLEMENTED |
| Application health response | IMPLEMENTED |
| Production health execution | NOT YET EVIDENCED |
| Production monitoring stack | NOT YET EVIDENCED |
| Production alerting implementation | NOT YET EVIDENCED |
| Production availability certification | NOT YET EVIDENCED |

Status tersebut merupakan evidence boundary dan bukan production readiness
certification.

---

# 5. Current Health Architecture

MAJE memiliki beberapa health validation layers:

Application
    ↓
GET /health

PostgreSQL
    ↓
pg_isready

Container Runtime
    ↓
Docker healthcheck

Service Dependency
    ↓
service_healthy

Deployment / Operations
    ↓
Health Validation

Application health dan dependency health harus dipahami sebagai
lapisan yang berbeda.

Application endpoint menunjukkan bahwa application process dapat
memberikan response.

Database healthcheck memvalidasi availability PostgreSQL melalui mekanisme
container.

Container health status menggabungkan healthcheck result dengan lifecycle
management container.

---

# 6. Application Health Endpoint

Backend MAJE menyediakan:

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

Current response shape:

{
  "success": true,
  "message": "MAJE healthy"
}

Endpoint ini merupakan application-level health mechanism.

7. Application Health Interpretation

Successful response dari /health menunjukkan bahwa application endpoint
dapat dipanggil dan menghasilkan response sesuai implementation saat ini.

Health response tersebut tidak dengan sendirinya membuktikan:

seluruh database operation berhasil;
seluruh external dependency tersedia;
seluruh business workflow berfungsi;
production availability target terpenuhi;
monitoring dan alerting production aktif.

Interpretasi health harus selalu mempertimbangkan scope validation.

8. PostgreSQL Health Check

PostgreSQL container menggunakan:

pg_isready

Development dan production Compose configuration menyediakan PostgreSQL
healthcheck.

Baseline PostgreSQL healthcheck memvalidasi readiness database service
melalui PostgreSQL readiness mechanism.

Healthcheck ini tidak menggantikan:

database integrity validation;
backup validation;
restore testing;
migration validation;
production disaster recovery validation.
9. Backend Container Health Check

Backend container menggunakan:

curl -f http://localhost:8000/health

Healthcheck tersebut digunakan untuk memeriksa apakah backend service dapat
memberikan successful response dari /health.

Current Compose configurations define backend healthchecks for:

default Compose environment;
development Compose environment;
production Compose environment.
10. Service Dependency Health

Compose configuration menggunakan dependency condition:

condition: service_healthy

Backend bergantung pada PostgreSQL yang telah mencapai healthy state
sebelum dependency relationship mengizinkan startup progression.

Dependency health harus dibedakan dari application health.

Database healthy tidak berarti seluruh application workflow sehat.

Application healthy juga tidak berarti seluruh database workload sehat.

11. Development Health Check

Development environment menggunakan:

docker compose -f docker-compose.dev.yml config

Setelah services dijalankan, operator dapat memeriksa container state:

docker compose -f docker-compose.dev.yml ps

Backend endpoint dapat divalidasi dengan:

curl -f http://localhost:8000/health

PostgreSQL readiness dapat diperiksa melalui container health status.

Development health validation digunakan untuk troubleshooting dan
deployment preparation.

12. Default Compose Health Check

Default Compose configuration dapat divalidasi dengan:

docker compose -f docker-compose.yml config

Container state dapat diperiksa dengan:

docker compose ps

Application health dapat divalidasi dengan:

curl -f http://localhost:8000/health

Health result harus dicatat apabila digunakan sebagai deployment evidence.

13. Production Health Check Boundary

Production Compose configuration menyediakan healthcheck mechanism.

Configuration validation dapat dilakukan dengan:

docker compose -f docker-compose.prod.yml config

Namun keberadaan production healthcheck configuration tidak sama dengan
successful production execution.

Current status:

Production Healthcheck Configuration
        ↓
IMPLEMENTED

Production Healthcheck Execution
        ↓
NOT YET EVIDENCED

Tidak boleh menyatakan production service healthy hanya berdasarkan
keberadaan configuration.

14. Manual Application Health Validation

Manual application validation:

curl -f http://localhost:8000/health

Expected successful response:

{
  "success": true,
  "message": "MAJE healthy"
}

Jika command menghasilkan successful HTTP response, application health
endpoint berhasil merespons pada environment yang sedang diuji.

Environment dan Git revision harus dicatat untuk evidence yang material.

15. Container Health Validation

Operator dapat memeriksa health state container dengan:

docker compose ps

Untuk detail container:

docker inspect <container-name>

Health status harus diperiksa terhadap container yang relevan.

Expected state untuk service dengan configured healthcheck:

healthy

State selain healthy harus diperlakukan sebagai operational condition
yang memerlukan investigation sebelum deployment atau release dilanjutkan.

16. Health Failure Investigation

Jika health validation gagal:

Detection
↓
Identify Service
↓
Inspect Container State
↓
Inspect Application Logs
↓
Inspect Dependency Health
↓
Determine Cause
↓
Recover / Restart / Rollback
↓
Repeat Health Validation
↓
Record Result

Operator tidak boleh melakukan repeated uncontrolled restart atau
deployment attempt tanpa memahami failure condition.

17. Application Log Investigation

Jika /health gagal, periksa backend logs:

docker compose logs --tail=200 backend

Untuk environment tertentu gunakan Compose file yang sesuai.

Investigation harus mencari:

startup failure;
import failure;
configuration failure;
database connection failure;
runtime exception;
dependency failure;
resource-related failure.

Log output yang relevan harus dipertahankan apabila dibutuhkan sebagai
incident atau deployment evidence.

18. Database Dependency Investigation

Jika backend health validation gagal dan database dependency dicurigai,
periksa PostgreSQL state:

docker compose ps postgres

Periksa PostgreSQL logs:

docker compose logs --tail=200 postgres

Jika diperlukan, validasi readiness melalui:

docker compose exec postgres pg_isready -U postgres -d maje

Parameter database harus disesuaikan dengan environment yang sedang
divalidasi.

19. Recovery Consideration

Recovery action harus ditentukan berdasarkan failure condition.

Possible recovery actions:

correct configuration;
restore required dependency;
restart affected service;
correct database migration condition;
rollback deployment;
restore from validated backup where applicable.

Recovery action harus mempertimbangkan data integrity dan release state.

Backup restore procedure berada pada:

EVIDENCE-005 — Backup & Restore Validation

Production disaster recovery capability tidak dianggap validated hanya
karena recovery procedure telah didokumentasikan.

20. Post-Deployment Health Validation

Setelah deployment, minimal lakukan:

verify deployed revision;
verify container state;
verify application health;
verify database dependency;
inspect recent application logs;
validate critical application behavior where applicable;
record result.

Baseline flow:

Deployment
↓
Container Health
↓
Application Health
↓
Dependency Health
↓
Critical Workflow
↓
Monitoring
↓
Evidence

Post-deployment validation harus dikaitkan dengan release revision.

21. Health Check Evidence

Material health validation evidence harus mencatat:

date/time;
environment;
Git revision;
service;
endpoint or health mechanism;
command or validation method;
result;
relevant logs;
operator/responsible role where applicable;
failure/recovery action where applicable;
limitations.

Contoh evidence reference:

Environment: Development
Service: Backend
Revision: <git-sha>
Check: GET /health
Result: PASS

Evidence harus disimpan sesuai Evidence Governance.

22. Relationship to Deployment

Health validation merupakan bagian dari controlled deployment lifecycle.

Deployment tidak dianggap operationally validated hanya karena:

container berhasil dibuat;
image berhasil dibuild;
Compose configuration valid;
CI berhasil.

Deployment health harus diverifikasi pada target environment.

Current CI evidence establishes automated validation but does not establish
production health execution.

23. Relationship to Monitoring and Observability

Health check merupakan salah satu signal operational health.

HC-009 juga mendefinisikan:

logging;
metrics;
tracing;
alerting;
incident detection;
operational dashboard.

Health endpoint atau container healthcheck tidak menggantikan complete
monitoring and observability capability.

Production monitoring stack dan production alerting implementation masih
memerlukan evidence tersendiri.

24. Health Check and Backup/Recovery Relationship

Health validation harus dipertimbangkan bersama recovery capability.

Current evidence:

EVIDENCE-005 — Backup & Restore Validation

EVIDENCE-005 memvalidasi isolated PostgreSQL backup and restore execution.

Health validation tidak membuktikan bahwa backup tersedia atau restore
production berhasil.

Sebaliknya, successful restore validation tidak membuktikan application
production health.

Kedua capability harus tetap memiliki evidence boundary masing-masing.

25. Current Validation Status

OPS-002 saat ini diklasifikasikan sebagai:

DOCUMENTED

Repository implementation yang mendukung procedure ini meliputi:

/health application endpoint;
PostgreSQL healthcheck;
backend container healthcheck;
Compose dependency health condition;
development Compose configuration;
production Compose configuration.

Namun procedure ini belum menjadi bukti execution untuk production
environment.

Capabilities yang masih belum memiliki production execution evidence:

production health validation;
production monitoring;
production alerting;
production post-deployment health validation;
production incident execution.
26. Operational Limitations

Procedure ini tidak merupakan:

production availability certification;
SLA certification;
SLO certification;
monitoring platform certification;
alerting certification;
disaster recovery certification;
production incident readiness certification.

Health endpoint saat ini merupakan application-level endpoint dan tidak
dengan sendirinya membuktikan semua dependency atau business workflow sehat.

Exact production health requirements tetap mengikuti deployment architecture,
monitoring governance, security governance, release governance, dan applicable
business requirements.

27. Related Documents

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

Evidence:

EVIDENCE-005 — Backup & Restore Validation
EVIDENCE-013 — CI/CD Implementation Validation
28. Document History
Version	Date	Change
1.0	2026-08-27	Established baseline health check procedure
