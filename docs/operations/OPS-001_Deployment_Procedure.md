# OPS-001 — Deployment Procedure

**Document ID:** OPS-001  
**Project:** MAJE Platform  
**Document Area:** Operations  
**Status:** Procedure Baseline Established  
**Version:** 1.0  
**Owner:** Engineering Team  
**Last Updated:** 2026-08-27

---

# 1. Purpose

Dokumen ini mendefinisikan prosedur deployment MAJE Platform secara
terkendali, dapat ditelusuri, dan berbasis evidence.

Procedure ini menerjemahkan requirement dari:

- ARC-008 — Deployment Architecture
- HC-008 — Deployment Governance
- HC-014 — Release Management

menjadi operational procedure yang dapat digunakan untuk validation,
deployment preparation, deployment execution, dan post-deployment
verification.

Dokumen ini tidak menyatakan bahwa production deployment automation telah
tersedia apabila capability tersebut belum memiliki implementation dan
execution evidence.

---

# 2. Scope

Procedure ini mencakup:

- deployment prerequisites;
- source and Git validation;
- CI validation;
- container validation;
- database migration consideration;
- deployment execution boundary;
- health validation;
- post-deployment validation;
- evidence recording;
- failure handling;
- rollback consideration.

Procedure ini berlaku sebagai baseline operational procedure.

Production deployment tetap membutuhkan environment, authorization, artifact,
credential, infrastructure, dan approval controls yang sesuai dengan
deployment architecture dan governance.

---

# 3. Deployment Status Classification

Deployment capability menggunakan klasifikasi:

## DOCUMENTED

Procedure telah ditetapkan tetapi execution belum dilakukan.

## IMPLEMENTED

Komponen atau capability telah tersedia pada repository/runtime.

## VALIDATED

Capability telah dieksekusi dan memiliki objective evidence.

## NOT YET EVIDENCED

Capability didefinisikan dalam architecture atau governance tetapi belum
memiliki execution evidence yang memadai.

---

# 4. Current Deployment Baseline

Repository saat ini menyediakan beberapa deployment primitives:

| Capability | Status |
|---|---|
| Docker containerization | IMPLEMENTED |
| Backend Dockerfile | IMPLEMENTED |
| Development Compose configuration | IMPLEMENTED |
| Production Compose configuration | IMPLEMENTED |
| PostgreSQL container | IMPLEMENTED |
| PostgreSQL healthcheck | IMPLEMENTED |
| Backend healthcheck | IMPLEMENTED |
| Container restart policy | IMPLEMENTED |
| Environment-specific configuration | IMPLEMENTED |
| Alembic migration mechanism | IMPLEMENTED |
| GitHub Actions CI workflow | IMPLEMENTED |
| GitHub Actions CI execution | VALIDATED |
| Backend automated tests | VALIDATED |
| Frontend lint | VALIDATED |
| Frontend production build | VALIDATED |
| Production deployment execution | NOT YET EVIDENCED |
| Automated deployment promotion | NOT YET EVIDENCED |
| Artifact registry/publication | NOT YET EVIDENCED |
| Production rollback execution | NOT YET EVIDENCED |
| Production post-deployment validation | NOT YET EVIDENCED |

This table describes the current evidence boundary and is not a production
readiness certification.

---

# 5. Deployment Flow

Governed deployment follows:

Code Change
    ↓
Code Review
    ↓
CI Validation
    ↓
Build / Artifact
    ↓
Security Validation
    ↓
Release Approval
    ↓
Target Environment Deployment
    ↓
Health Validation
    ↓
Post-Deployment Validation
    ↓
Monitoring
    ↓
Evidence Recording

The currently validated repository execution establishes the CI portion of
this flow.

Deployment, production promotion, and post-production operational execution
remain subject to separate evidence.

---

# 6. Preconditions

Before deployment activity begins, the responsible operator must verify:

- correct Git branch;
- intended Git revision;
- working tree state;
- required code review state;
- CI result;
- applicable release approval;
- target environment;
- environment configuration;
- required credentials;
- database migration status;
- backup requirement;
- rollback consideration.

No production deployment should proceed when required authorization or
release controls are absent.

---

# 7. Source and Git Validation

Record the intended release revision:

```bash
git status -sb
git rev-parse HEAD
git log -1 --format='%H%n%ad%n%s' --date=iso
The working tree should be clean before a controlled release unless a
documented exception has been approved.

The deployment evidence should record:

branch;
commit SHA;
commit message;
date/time;
operator or responsible role where applicable.
8. CI Validation

The release candidate must pass the applicable CI workflow before
deployment.

Current MAJE CI validates:

backend dependency installation;
database initialization;
Alembic migration;
database seed;
backend pytest;
frontend dependency installation;
frontend lint;
frontend production build.

The validated CI execution recorded in EVIDENCE-013 includes:

MAJE CI #5
Commit: 29c1f4a

Backend Tests:
SUCCESS

188 passed
0 failed
0 errors

Frontend Validation:
SUCCESS

Overall workflow:
SUCCESS

CI success is a prerequisite for controlled release consideration but does
not by itself constitute production deployment approval.

9. Container Validation

Before deployment, validate the applicable container configuration.

Development baseline:

docker compose -f docker-compose.dev.yml config

Production baseline:

docker compose -f docker-compose.prod.yml config

Configuration validation must confirm that:

required services are present;
dependency relationships are correct;
healthchecks are defined where required;
environment configuration is correctly referenced;
no unintended development configuration is used for production.

The production Compose definition currently provides PostgreSQL and backend
services with healthchecks and restart policies.

10. Database Migration

Database changes must use the governed Alembic migration mechanism.

Before applying production migration:

identify the target migration;
verify migration history;
validate compatibility;
confirm backup requirement;
confirm rollback/recovery plan.

Baseline command:

alembic current

Migration execution:

alembic upgrade head

Production database migration must only be performed through an authorized
deployment process.

Destructive migration must not be executed without explicit impact
assessment and recovery planning.

11. Backup Requirement

Before a production deployment that changes persistent data or schema,
the applicable backup requirement must be evaluated.

Current evidence establishes successful isolated PostgreSQL backup and
restore validation through EVIDENCE-005.

That evidence does not establish:

automated production backup scheduling;
off-site backup retention;
production restore execution;
point-in-time recovery;
production RTO/RPO compliance.

Therefore backup readiness must be assessed separately for each production
deployment.

12. Deployment Execution Boundary

The current repository contains deployment configuration but does not yet
provide objective evidence of an executed production deployment.

Accordingly:

Deployment Configuration
        ↓
IMPLEMENTED

Production Deployment Execution
        ↓
NOT YET EVIDENCED

No production deployment should be represented as successful unless
execution evidence exists.

Where deployment automation is introduced in the future, the procedure must
record:

release version;
Git revision;
artifact identity;
target environment;
deployment start/end;
deployment result;
approval;
validation result.
13. Health Validation

After deployment, validate service health.

Current backend health endpoint:

GET /health

The repository also defines container healthchecks for the backend and
PostgreSQL services.

Health validation should confirm:

application process is active;
required dependency is available;
service responds successfully;
no immediate startup failure is present.

Example:

curl -f http://localhost:8000/health

A successful health response does not by itself establish complete
production operational readiness.

14. Post-Deployment Validation

Post-deployment validation should include, where applicable:

health endpoint;
database connectivity;
API availability;
critical application workflow;
migration state;
application logs;
error condition;
resource condition;
monitoring status.

Validation result must be recorded with the deployed revision.

15. Deployment Failure Handling

If deployment fails:

Detection
    ↓
Stop / Contain
    ↓
Investigate
    ↓
Determine Recovery Action
    ↓
Rollback if Required
    ↓
Health Validation
    ↓
Document Result

The operator must avoid uncontrolled repeated deployment attempts.

Failure handling must preserve sufficient evidence for later analysis.

16. Rollback Consideration

Rollback should restore the service to a known-good release or artifact.

Before rollback:

identify failed release;
identify known-good release;
assess database compatibility;
determine whether database rollback is safe;
obtain required approval where applicable.

After rollback:

validate health;
validate critical API behavior;
inspect logs;
verify database compatibility;
record rollback evidence.

Production rollback execution is currently:

DOCUMENTED
NOT YET VALIDATED
17. Security Controls

Deployment must follow security governance.

The operator must verify:

credentials are not committed to Git;
production secrets are provided through controlled configuration;
access is role-based;
privileged operations are auditable;
production access is not performed through shared accounts;
deployment changes remain traceable.
18. Release Approval

Production release must follow the applicable approval boundary.

HC-014 establishes:

Engineering Lead Approval;
QA Approval;
Product Approval where required.

Approval state should be recorded before production deployment.

A CI success result must not be treated as a substitute for required
production release approval.

19. Evidence Recording

Each material deployment execution should produce evidence containing:

deployment date/time;
environment;
Git revision;
release version;
artifact identity where applicable;
operator/responsible role;
approval state;
deployment result;
health result;
post-deployment validation;
rollback result where applicable;
limitations.

Evidence must be stored according to MAJE Evidence Governance.

20. Current Validation Status

OPS-001 is currently classified as:

DOCUMENTED

The procedure is grounded in currently available repository configuration,
architecture, governance, and existing validation evidence.

The following capabilities remain without production execution evidence:

production deployment;
automated deployment promotion;
artifact publication;
production rollback;
production post-deployment validation;
production monitoring and alerting execution.
21. Related Documents

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

Evidence:

EVIDENCE-005 — Backup & Restore Validation
EVIDENCE-013 — CI/CD Implementation Validation
22. Document History
Version	Date	Change
1.0	2026-08-27	Established baseline deployment procedure
