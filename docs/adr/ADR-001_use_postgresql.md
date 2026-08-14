# ADR-001 — Use PostgreSQL

## HARDYNATTA CHUNG Enterprise Software Engineering Ecosystem

| Item | Value |
|---|---|
| Document ID | ADR-001 |
| Document Name | Use PostgreSQL |
| Version | 1.0 |
| Status | Accepted |
| Owner | HARDYNATTA CHUNG |
| Domain | Architecture Decision Record |
| Governance Authority | HC-010 ADR Governance |
| Primary Platform | MAJE — Mandarin AI Judge Enterprise |
| Decision Type | Database Architecture |
| Decision Scope | MAJE Backend Persistence |
| Review Cycle | When architecture, workload, or database requirements materially change |

---

# 1. Purpose

ADR-001 records the architectural decision to use PostgreSQL as the primary relational database and system of record for MAJE transactional application data.

This ADR provides controlled historical traceability between:

```text
Governance
↓
Architecture
↓
Decision
↓
Implementation
↓
Evidence
```

This document does not replace ARC-005 Database Architecture or the actual database implementation.

---

# 2. Context

MAJE requires a persistent relational data platform for transactional application data.

The MAJE backend contains application services, repositories, ORM models, migrations, and database-dependent workflows.

The current architecture establishes PostgreSQL as the persistence baseline.

ARC-002 Backend Architecture identifies PostgreSQL as the backend persistence baseline.

ARC-005 Database Architecture establishes PostgreSQL as the primary relational system of record for transactional application data.

The current development environment also uses PostgreSQL through Docker Compose.

---

# 3. Problem

The enterprise requires a controlled architectural decision identifying the primary relational database technology used by MAJE.

Without an explicit decision record:

- the database technology decision is difficult to trace historically;
- alternatives and rationale are not formally recorded;
- future database changes may lack a clear architectural baseline;
- implementation and architecture cannot be linked through a dedicated decision record.

Therefore, the database technology decision must be explicitly recorded.

---

# 4. Decision

## 4.1 Primary Decision

MAJE will use PostgreSQL as the primary relational database and system of record for transactional application data.

PostgreSQL is therefore the approved relational persistence baseline for the MAJE backend.

## 4.2 Architectural Position

PostgreSQL is positioned as the persistence layer below the application and service layers.

The application and service layers remain responsible for business workflows and transaction orchestration.

The database remains responsible for persistent relational data storage, integrity constraints, transactions, indexes, and database-level capabilities appropriate to the system requirements.

---

# 5. Alternatives Considered

The following alternatives are recognized as possible relational or persistence approaches.

## 5.1 Alternative A — PostgreSQL

**Selected.**

Advantages include:

- relational data model;
- transactional integrity;
- ACID transaction semantics;
- mature SQL capabilities;
- strong ecosystem support;
- compatibility with the current MAJE backend architecture;
- compatibility with SQLAlchemy and psycopg;
- suitability for the current Docker-based development environment;
- alignment with the existing MAJE implementation baseline.

## 5.2 Alternative B — MySQL / MariaDB

**Not selected as the current MAJE relational persistence baseline.**

Changing to this database family would introduce a different database technology and would require validation of:

- SQL behavior;
- migrations;
- constraints;
- transaction behavior;
- ORM compatibility;
- database-specific behavior;
- operational configuration;
- performance characteristics.

The current architecture does not require such a change.

## 5.3 Alternative C — NoSQL Database

**Not selected as the primary relational system of record.**

MAJE contains transactional and relational application data whose relationships, constraints, and transactional semantics are appropriately represented by a relational database.

A specialized NoSQL datastore may be introduced in the future for a specific justified workload, but it does not replace PostgreSQL as the primary relational system of record without a separate architectural decision.

## 5.4 Alternative D — Managed Relational Database Provider

**Not selected as a separate database technology decision.**

A managed PostgreSQL service may be used as a deployment implementation of this PostgreSQL decision when deployment architecture and operational requirements justify it.

The hosting model does not change the underlying database technology decision.

---

# 6. Rationale

The decision is based on the following considerations.

## 6.1 Relational Transactional Requirements

MAJE contains transactional workflows involving users, competitions, participants, judges, scores, rounds, results, and related application data.

A relational database provides an appropriate foundation for these relationships and transactional workflows.

## 6.2 Existing Architecture Alignment

ARC-002 Backend Architecture already establishes PostgreSQL as the persistence baseline.

ARC-005 Database Architecture establishes PostgreSQL as the primary relational system of record.

This ADR therefore formalizes an existing architectural baseline rather than introducing an unrelated technology.

## 6.3 Existing Implementation Alignment

The current MAJE backend implementation uses PostgreSQL connectivity through the existing database configuration and persistence stack.

The implementation therefore aligns with this ADR.

## 6.4 Transaction Integrity

MAJE workflows require reliable transaction semantics.

PostgreSQL provides the relational transaction capabilities required by the current architecture.

## 6.5 Engineering Ecosystem Alignment

The current backend architecture uses:

- SQLAlchemy;
- psycopg;
- Alembic;
- PostgreSQL;
- Docker Compose.

The selected database therefore aligns with the existing engineering ecosystem.

---

# 7. Consequences

## 7.1 Positive Consequences

The decision provides:

- a clear relational persistence baseline;
- consistent architectural direction;
- explicit database technology governance;
- traceability between architecture and implementation;
- support for transactional application workflows;
- compatibility with the current migration and ORM stack;
- a clear baseline for future database architecture decisions.

## 7.2 Negative Consequences

The decision also creates responsibilities.

The enterprise must maintain:

- PostgreSQL version compatibility;
- migration discipline;
- database backup and recovery capability;
- database security controls;
- schema governance;
- performance monitoring;
- operational maintenance;
- compatibility between application and database versions.

## 7.3 Future Consequence

If MAJE later requires another database technology for a specialized workload, that technology must be introduced through an appropriate architecture decision and must not silently replace the PostgreSQL baseline.

---

# 8. Implementation

The current MAJE development architecture provides PostgreSQL through Docker Compose.

The backend connects to PostgreSQL through the application database configuration.

The persistence stack includes:

```text
Application / Service Layer
        ↓
Repository / Data Access
        ↓
SQLAlchemy
        ↓
psycopg
        ↓
PostgreSQL
```

Database schema changes are managed through the project's migration mechanism.

---

# 9. Deployment Relationship

PostgreSQL is currently used as part of the Docker-based development environment.

The current development topology includes:

```text
Docker Compose
    │
    ├── Backend Container
    │
    └── PostgreSQL Container
```

Deployment-specific topology, infrastructure, storage, networking, high availability, and managed database decisions remain governed by the applicable deployment architecture.

---

# 10. Security Considerations

PostgreSQL must operate within the security architecture and applicable security controls.

Database credentials must not be hard-coded into source code.

Database access must use controlled configuration and appropriate credential management.

Application access to PostgreSQL must follow least-privilege principles.

Database exposure must be restricted according to environment and deployment requirements.

Production database security must be validated separately as part of production readiness and security validation.

---

# 11. Reliability and Recovery Considerations

PostgreSQL is a critical persistence dependency for MAJE.

Therefore, the operational architecture must provide appropriate:

- backup;
- restore;
- recovery;
- monitoring;
- health validation;
- migration control;
- failure handling.

Recovery requirements must be determined according to business impact and applicable operational architecture.

---

# 12. Observability Considerations

Database operations should be observable through the applicable observability architecture.

Relevant signals may include:

- database availability;
- connection health;
- query performance;
- transaction failures;
- connection pool behavior;
- storage utilization;
- migration status;
- database errors.

Observability implementation remains governed by the applicable observability and operations documentation.

---

# 13. Architecture References

This ADR is supported by the following architectural and governance documents.

## 13.1 HC-010 — ADR Governance

Defines the governance and required structure for Architecture Decision Records.

## 13.2 ARC-002 — Backend Architecture

Defines PostgreSQL as the backend persistence baseline.

## 13.3 ARC-005 — Database Architecture

Defines PostgreSQL as the primary relational system of record for transactional application data.

## 13.4 ARC-008 — Deployment Architecture

Defines the deployment relationship for database and application services.

## 13.5 ARC-009 — Observability Architecture

Defines observability relationships for databases and services.

---

# 14. Evidence

The current backend Docker test validation provides objective evidence that the current backend test suite executes successfully in the Docker Compose backend environment.

## 14.1 Evidence Record

```text
Evidence ID:
EVIDENCE-002

Evidence:
Backend Docker Test Validation

Validation Date:
2026-08-14 09:31:08

Git Commit:
474a478

Git Branch:
feature/docs-refactor-v2

Execution Context:
Docker Compose backend container

Command:
docker compose exec backend python -m pytest -q

Result:
162 passed
0 failed
0 errors
0 warnings
```

## 14.2 Evidence Source

```text
docs/evidence/backend/EVIDENCE-002_backend_docker_test_validation.txt
```

EVIDENCE-002 validates backend execution but does not independently prove every database architecture requirement.

Database-specific validation remains subject to the applicable architecture, testing, security, and operational evidence requirements.

---

# 15. Traceability

The decision is traceable through the following chain:

```text
HC-000 Project Constitution
        ↓
HC-010 ADR Governance
        ↓
ADR-001 Use PostgreSQL
        ↓
ARC-002 Backend Architecture
        ↓
ARC-005 Database Architecture
        ↓
Database Implementation
        ↓
Docker PostgreSQL Runtime
        ↓
Backend Validation
        ↓
EVIDENCE-002
```

This traceability establishes the relationship between governance, architectural decision, implementation, and objective evidence.

---

# 16. Decision Status

**ACCEPTED**

The PostgreSQL decision is accepted as the current MAJE relational persistence baseline.

This ADR remains applicable until:

- the architecture materially changes;
- business requirements require a different persistence strategy;
- PostgreSQL no longer satisfies applicable requirements;
- a replacement architecture decision is formally approved.

---

# 17. Review Conditions

ADR-001 must be reviewed when:

- the primary database technology is proposed to change;
- database architecture materially changes;
- transaction requirements materially change;
- scalability requirements materially change;
- deployment architecture requires a different persistence strategy;
- significant database operational constraints are identified;
- security or compliance requirements materially change.

A replacement decision must explicitly supersede this ADR rather than silently modifying the historical decision.

---

# 18. Governance Rules

This ADR is governed by HC-010 ADR Governance.

Changes must preserve:

- decision identity;
- decision history;
- rationale;
- alternatives;
- consequences;
- traceability;
- auditability.

Historical decisions must not be rewritten to conceal previous architectural choices.

If the decision changes, a new ADR or formally governed superseding decision must be created.

---

# 19. Revision History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-08-14 | Initial ADR recording PostgreSQL as the primary relational database and system of record for MAJE |

---

# Final Statement

**ADR-001 — Use PostgreSQL**

HARDYNATTA CHUNG Enterprise Software Engineering Ecosystem

**Version 1.0 — Accepted Architecture Decision**

PostgreSQL is the approved primary relational database and system of record for MAJE transactional application data.

This decision establishes a controlled architectural baseline connecting:

```text
Governance
↓
Architecture
↓
Decision
↓
Implementation
↓
Validation
↓
Evidence
```

ADR-001 does not by itself constitute production readiness or closure of any GAP-001 finding.

It provides the formal architectural decision record required for traceability and governance.
