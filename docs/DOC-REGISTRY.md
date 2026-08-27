# MAJE Enterprise Document Registry

## HARDYNATTA CHUNG Enterprise Software Engineering Ecosystem

---

# 1. Purpose

Dokumen ini mendefinisikan controlled registry untuk dokumentasi resmi yang digunakan dalam MAJE Enterprise Software Engineering Ecosystem.

DOC-REGISTRY merupakan authoritative registry untuk:

- document identifier;
- document prefix;
- document numbering;
- document naming;
- official document inventory;
- document status;
- document version;
- document ownership;
- document location;
- document governance;
- document lifecycle;
- document traceability.

Registry ini harus tetap konsisten dengan:

- HC-000 — Project Constitution;
- HC-011 — Documentation Governance;
- MDB-001 — Master Document Blueprint;
- PLN-001 — Document Roadmap;
- PLN-002 — Document Dependency;
- PLN-003 — Document Status;
- INDEX.md.

---

# 2. Registry Authority

DOC-REGISTRY merupakan controlled governance registry.

Registry menjawab:

> What official documents exist?

Registry tidak menggantikan:

- MASTER_DOCUMENT_BLUEPRINT.md sebagai target-state documentation architecture;
- DOCUMENT_ROADMAP.md sebagai documentation sequencing authority;
- DOCUMENT_DEPENDENCY.md sebagai dependency authority;
- DOCUMENT_STATUS.md sebagai current-state status authority;
- INDEX.md sebagai navigation entry point.

Relationship:

```text
MASTER DOCUMENT BLUEPRINT
        |
        v
DOCUMENT ROADMAP
        |
        v
DOCUMENT DEPENDENCY
        |
        v
DOCUMENT STATUS
        |
        v
DOC-REGISTRY
        |
        v
INDEX
```

---

# 3. Document Prefix Registry
Prefix	Name	Description
HC	Hardy Chung Governance Series	Enterprise Governance Documents
FDN	Foundation	Enterprise Foundation Documents
MDB	Master Documentation Blueprint	Master Documentation Architecture
PLN	Planning	Documentation Planning Documents
ARC	Architecture	Enterprise and System Architecture Documents
PRD	Product	Product and Business Requirement Documents
DB	Database	Database Documentation
API	API Specification	API and Integration Specification Documents
STD	Standard	Engineering Standards
OPS	Operations	Operations and Production Documents
ADR	Architecture Decision Record	Architecture Decision Documents
IMP	Implementation	Implementation and Engineering Records
EVD	Evidence Registry	Evidence Registry Documents
EVIDENCE	Evidence	Objective Validation and Assessment Evidence
GAP	Assessment	Enterprise Assessment and Gap Analysis Documents
TPL	Template	Documentation Templates
GEN	Generated	Generated Documents

Prefix dapat berkembang apabila domain dokumentasi baru secara resmi diperlukan.


Penambahan prefix harus mengikuti documentation governance dan diregistrasikan sebelum digunakan untuk official documents.

# 4. Prefix Rules

Setiap official document:

harus memiliki satu document identifier;
harus menggunakan prefix yang terdaftar;
harus memiliki nomor unik;
tidak boleh menggunakan identifier document lain;
tidak boleh mengganti identifier setelah dipublikasikan tanpa governance decision;
harus dapat ditelusuri ke lokasi file;
harus memiliki ownership dan governance authority;
harus mengikuti applicable documentation standard.

Satu dokumen hanya boleh memiliki satu primary identifier.

# 5. Document Identifier Strategy

Format identifier:

<PREFIX>-<NUMBER>

Contoh:

HC-000
FDN-001
MDB-001
PLN-001
ARC-001
ADR-001
PRD-001
DB-001
API-001
STD-001
OPS-001
IMP-001
EVD-001
EVIDENCE-001
GAP-001
TPL-001
GEN-001

Identifier harus:

unik;
stabil;
mudah dicari;
dapat digunakan dalam cross-reference;
dapat digunakan dalam governance;
dapat digunakan dalam traceability;
tidak bergantung pada filename semata.

Nomor yang telah digunakan tidak boleh digunakan kembali untuk dokumen lain.

# 6. Numbering Convention

Format:

<PREFIX>-<NUMBER>

Nomor menggunakan tiga digit sebagai baseline:

001
002
003
...

Contoh:

ARC-001
ARC-002
ARC-003

HC-000
HC-001
HC-002

FDN-001
FDN-002

PLN-001
PLN-002

ADR-001
ADR-002

Nomor harus unik dalam applicable document series.

Identifier HC-000 merupakan constitutional document identifier dan tidak boleh digunakan kembali untuk dokumen lain.

Nomor tidak boleh digunakan ulang setelah identifier dipublikasikan.

# 7. Filename Standard

Format umum:

<PREFIX>-<NUMBER>_<Descriptive_Name>.md

Contoh:

FDN-005_Enterprise_Roadmap.md
ARC-001_System_Architecture.md
HC-011_Documentation_Governance.md
ADR-002_authentication_strategy.md

Untuk evidence:

EVIDENCE-001_backend_test_validation.txt

Aturan filename:

gunakan identifier yang sesuai dengan document ID;
gunakan descriptive name;
gunakan underscore sebagai separator;
hindari nama ambigu;
hindari duplicate filename;
jangan membuat filename berbeda hanya karena case;
jangan mengubah filename official tanpa mempertimbangkan traceability;
historical backup harus ditandai secara eksplisit sebagai historical atau backup.

Filename merupakan physical representation.

Document ID merupakan logical identity.

# 8. Document Metadata

Setiap official document harus memiliki metadata yang sesuai dengan document type.

Minimum metadata yang direkomendasikan:

Document ID
Document Name
Version
Status
Owner
Document Type
Domain
Governance Authority
Review Cycle

Metadata memungkinkan:

registry management;
lifecycle management;
ownership;
review;
traceability;
auditability.
# 9. Document Status

Status document menggunakan controlled lifecycle vocabulary.

Status	Meaning
Draft	Sedang dikembangkan
Review	Sedang ditinjau
Approved	Telah disetujui
Active	Berlaku sebagai current reference
Deprecated	Tidak lagi direkomendasikan
Superseded	Digantikan oleh dokumen lain
Archived	Dipindahkan ke historical archive

Status harus mencerminkan kondisi aktual dokumen.

File yang berada di repository tidak otomatis berarti file tersebut merupakan official active document.

# 10. Versioning

Official documents menggunakan semantic document versioning:

MAJOR.MINOR

Contoh:

1.0
1.1
2.0

MAJOR version berubah apabila:

struktur governance berubah secara signifikan;
authority berubah;
architectural position berubah;
scope fundamental berubah.

MINOR version berubah apabila:

terdapat clarification;
terdapat improvement;
terdapat additional detail;
terdapat correction yang tidak mengubah fundamental authority.

Version harus diperbarui bersama revision history apabila perubahan signifikan dilakukan.

# 11. Document Lifecycle

Lifecycle baseline:

Idea
  |
  v
Draft
  |
  v
Review
  |
  v
Approved
  |
  v
Active
  |
  v
Updated
  |
  v
Superseded / Deprecated
  |
  v
Archived

Lifecycle harus dapat ditelusuri.

Perubahan lifecycle harus tetap memiliki historical traceability.

# 12. Document Creation

Dokumen baru harus:

memiliki purpose;
memiliki domain;
memiliki identifier;
memiliki owner;
memiliki governance authority;
memiliki applicable status;
memiliki version;
memiliki dependency apabila relevan;
memiliki expected lifecycle;
terdaftar dalam registry apabila menjadi official document.

Dokumen tidak dianggap official hanya karena file telah dibuat.

Official status harus didukung oleh applicable:

ownership;
review;
approval;
registry;
version;
governance.
# 13. Document Review

Document review harus mempertimbangkan:

accuracy;
completeness;
consistency;
dependency;
governance;
technical correctness;
business relevance;
maintainability;
traceability.

Review tidak hanya memeriksa grammar atau formatting.

Review harus memastikan tidak terdapat contradiction material antar controlled documents.

# 14. Document Approval

Approval harus mengikuti governance authority yang berlaku.

Dokumen tidak menjadi official hanya karena:

berada di Git;
telah dibuat oleh engineer;
telah di-commit;
telah di-push;
telah muncul dalam INDEX.

Official status membutuhkan applicable governance approval dan registry recognition.

# 15. Document Update

Perubahan significant terhadap official document harus:

mempertahankan Document ID;
memperbarui version apabila diperlukan;
memperbarui revision history;
memeriksa dependency;
memeriksa downstream impact;
diperiksa melalui Git;
direview sesuai governance.

Document ID tidak boleh diganti hanya karena document mengalami revision.

# 16. Document Retirement

Dokumen dapat retired apabila:

tidak lagi relevan;
digantikan dokumen baru;
architecture berubah;
product berubah;
governance berubah;
document scope tidak lagi diperlukan.

Retirement harus mempertahankan historical traceability.

Document yang retired tidak boleh disamarkan sebagai current active reference.

# 17. Official Document Inventory

Registry berikut mencatat official documents yang saat ini teridentifikasi dalam active repository baseline.

## 17.1 Governance

| Document ID | Document | Location | Status |
|---|---|---|---|
| HC-000 | Project Constitution | `docs/hc/HC-000_Project_Constitution.md` | Approved |
| HC-001 | Repository Blueprint | `docs/hc/HC-001_Repository_Blueprint.md` | Approved |
| HC-002 | Development Workflow | `docs/hc/HC-002_Development_Workflow.md` | Approved |
| HC-003 | Coding Standard | `docs/hc/HC-003_Coding_Standard.md` | Approved |
| HC-004 | API Governance | `docs/hc/HC-004_API_Governance.md` | Approved |
| HC-005 | Database Governance | `docs/hc/HC-005_Database_Governance.md` | Approved |
| HC-006 | Security Governance | `docs/hc/HC-006_Security_Governance.md` | Approved |
| HC-007 | Testing Governance | `docs/hc/HC-007_Testing_Governance.md` | Approved |
| HC-008 | Deployment Governance | `docs/hc/HC-008_Deployment_Governance.md` | Approved |
| HC-009 | Monitoring & Observability Governance | `docs/hc/HC-009_Monitoring_Observability_Governance.md` | Approved |
| HC-010 | ADR Governance | `docs/hc/HC-010_ADR_Governance.md` | Approved |
| HC-011 | Documentation Governance | `docs/hc/HC-011_Documentation_Governance.md` | Approved |
| HC-012 | Engineering Quality Governance | `docs/hc/HC-012_Engineering_Quality_Governance.md` | Approved |
| HC-013 | Technical Debt Management | `docs/hc/HC-013_Technical_Debt_Management.md` | Approved |
| HC-014 | Release Management | `docs/hc/HC-014_Release_Management.md` | Approved |

## 18. Foundation Inventory

| Document ID | Document | Location | Status |
|---|---|---|---|
| FDN-001 | Enterprise Definition | `docs/foundation/FDN-001_Enterprise_Definition.md` | Approved |
| FDN-002 | Vision, Mission & Core Values | `docs/foundation/FDN-002_Vision_Mission_Core_Values.md` | Approved |
| FDN-003 | Enterprise Principles | `docs/foundation/FDN-003_Enterprise_Principles.md` | Approved |
| FDN-004 | Business Capability | `docs/foundation/FDN-004_Business_Capability.md` | Approved |
| FDN-005 | Enterprise Roadmap | `docs/foundation/FDN-005_Enterprise_Roadmap.md` | Approved |

## 19. Planning Inventory

| Document ID | Document | Location | Status |
|---|---|---|---|
| MDB-001 | Master Document Blueprint | `docs/planning/MASTER_DOCUMENT_BLUEPRINT.md` | Approved |
| PLN-001 | Document Roadmap | `docs/planning/DOCUMENT_ROADMAP.md` | Approved |
| PLN-002 | Document Dependency | `docs/planning/DOCUMENT_DEPENDENCY.md` | Approved |
| PLN-003 | Document Status | `docs/planning/DOCUMENT_STATUS.md` | Approved |

## 20. Architecture Inventory

| Document ID | Document | Location | Status |
|---|---|---|---|
| ARC-001 | System Architecture | `docs/architecture/ARC-001_System_Architecture.md` | Approved |
| ARC-002 | Backend Architecture | `docs/architecture/ARC-002_Backend_Architecture.md` | Approved |
| ARC-003 | Frontend Architecture | `docs/architecture/ARC-003_Frontend_Architecture.md` | Approved |
| ARC-004 | AI Service Architecture | `docs/architecture/ARC-004_AI_Service_Architecture.md` | Approved |
| ARC-005 | Database Architecture | `docs/architecture/ARC-005_Database_Architecture.md` | Approved |
| ARC-006 | Integration Architecture | `docs/architecture/ARC-006_Integration_Architecture.md` | Approved |
| ARC-007 | Security Architecture | `docs/architecture/ARC-007_Security_Architecture.md` | Approved |
| ARC-008 | Deployment Architecture | `docs/architecture/ARC-008_Deployment_Architecture.md` | Approved |
| ARC-009 | Observability Architecture | `docs/architecture/ARC-009_Observability_Architecture.md` | Approved |

## 21. Architecture Decision Record Inventory

| Document ID | Document | Location | Status |
|---|---|---|---|
| ADR-001 | Use PostgreSQL | `docs/adr/ADR-001_use_postgresql.md` | Accepted |
| ADR-002 | Authentication Strategy | `docs/adr/ADR-002_authentication_strategy.md` | Accepted |

## 22. Assessment Inventory

| Document ID | Document | Location | Status |
|---|---|---|---|
| GAP-001 | MAJE Enterprise Gap Analysis | `docs/assessment/GAP-001_MAJE_Enterprise_Gap_Analysis.md` | Active |

## 23. Evidence Inventory

| Document ID | Document | Location | Status |
|---|---|---|---|
| EVIDENCE-001 | Backend Test Validation | `docs/evidence/backend/EVIDENCE-001_backend_test_validation.txt` | Valid |
| EVIDENCE-002 | Backend Docker Test Validation | `docs/evidence/backend/EVIDENCE-002_backend_docker_test_validation.txt` | Valid - Historical |
| EVIDENCE-003 | Evidence Publication and Traceability Validation | `docs/evidence/EVIDENCE-003_evidence_publication_traceability_validation.txt` | Valid |
| EVIDENCE-004 | Production Readiness Validation | `docs/evidence/EVIDENCE-004_production_readiness_validation.txt` | Valid |
| EVIDENCE-005 | Backup & Restore Validation | `docs/evidence/EVIDENCE-005_backup_restore_validation.txt` | Valid |
| EVIDENCE-006 | Observability Validation | `docs/evidence/EVIDENCE-006_observability_validation.txt` | Valid |
| EVIDENCE-007 | Security Validation | `docs/evidence/EVIDENCE-007_security_validation.txt` | Valid |
| EVIDENCE-008 | Frontend Validation | `docs/evidence/EVIDENCE-008_frontend_validation.txt` | Valid |
| EVIDENCE-009 | Test Execution Validation | `docs/evidence/EVIDENCE-009_test_execution_validation.txt` | Valid |
| EVIDENCE-010 | Current Backend Regression Validation | `docs/evidence/EVIDENCE-010_backend_current_regression_validation.txt` | Valid |
| EVIDENCE-011 | AI Service Implementation Validation | `docs/evidence/EVIDENCE-011_ai_service_implementation_validation.txt` | Valid |
| EVIDENCE-012 | Infrastructure Implementation Validation | `docs/evidence/EVIDENCE-012_infrastructure_implementation_validation.txt` | Valid |
| EVIDENCE-013 | CI/CD Implementation Validation | `docs/evidence/EVIDENCE-013_ci_cd_implementation_validation.txt` | Valid - F004 Remediation |

# 24. Evidence Registry

The evidence domain is additionally governed by:

docs/evidence/EVIDENCE-REGISTRY.md

Evidence Registry identifier:

EVD-001

EVD-001 is the registry document for evidence records.

Evidence IDs themselves use:

EVIDENCE-<NUMBER>

The distinction is intentional:

EVD-001
    |
    v
Evidence Registry

EVIDENCE-001
EVIDENCE-002
EVIDENCE-003
...
    |
    v
Individual Evidence Records
# 25. Documentation Category Entry Points

The following documentation domains currently have repository entry points:

Domain	Entry Point
API	docs/api/README.md
Database	docs/database/README.md
Product	docs/product/README.md
Operations	docs/operations/README.md
Standards	docs/standards/README.md
Templates	docs/templates/README.md
Generated	docs/generated/README.md
ADR	docs/adr/README.md

An entry-point README does not automatically constitute a numbered controlled document.

# 26. Historical Documents

Historical documents may remain in the repository when required for traceability.

Example:

docs/hc/HC-000_Project_Constitution.v1.backup.md

Historical backup files:

are not current active references;
must not replace the current official document;
must not create a new document identity;
must preserve historical traceability.
# 27. Registry and Index

DOC-REGISTRY.md and INDEX.md have different responsibilities.

DOC-REGISTRY

Answers:

What official documents exist?

Registry responsibilities:

inventory;
identity;
status;
location;
governance;
lifecycle;
traceability.
INDEX

Answers:

What should I read?

Index responsibilities:

navigation;
discovery;
entry points;
document grouping;
reader orientation.

Therefore:

DOC-REGISTRY = Governance / Inventory
INDEX         = Navigation

INDEX is not a replacement for DOC-REGISTRY.

# 28. Registry and Master Blueprint

MASTER_DOCUMENT_BLUEPRINT.md and DOC-REGISTRY.md have different authorities.

MASTER DOCUMENT BLUEPRINT

Defines:

Target State

It answers:

What documentation structure should exist?

DOC-REGISTRY

Defines:

Current Registered State

It answers:

What official documents currently exist?

Relationship:

MASTER DOCUMENT BLUEPRINT
        |
        v
Target Documentation Set
        |
        v
DOC-REGISTRY
        |
        v
Current Official Inventory

Any material difference between target-state and current-state documentation should be explainable through planning, status, or governance.

# 29. Registry and Planning

The registry must remain consistent with:

MDB-001
PLN-001
PLN-002
PLN-003

Responsibilities:

Document	Authority
MDB-001	Documentation structure and target inventory
PLN-001	Documentation sequence and roadmap
PLN-002	Document dependencies
PLN-003	Current document status
DOC-REGISTRY	Official registered inventory
INDEX	Navigation
# 30. Single Source of Truth

The Git repository is the single source of truth for official MAJE documentation.

Official documentation must not exist only in:

personal computers;
chat conversations;
email;
uncontrolled cloud folders;
applications without version control;
undocumented local copies.

Important documentation must be consolidated into the repository when it becomes part of the official baseline.

# 31. Git Traceability

Controlled documentation changes must remain traceable through Git.

Baseline workflow:

Working Tree
    |
    v
Git Diff
    |
    v
Review
    |
    v
Commit
    |
    v
Push
    |
    v
Pull Request
    |
    v
Review / Approval
    |
    v
Merge

Documentation changes must not bypass applicable governance.

# 32. Registry Maintenance

DOC-REGISTRY must be updated when:

a new official document is created;
a document becomes officially approved;
an official document is retired;
a document is superseded;
a document location changes;
a document identifier changes under formal governance;
a new documentation domain is introduced;
a document is renamed under approved change control.

Registry updates must preserve historical traceability.

# 33. Registry Quality Gate

The registry is considered structurally valid when:

every registered document has a unique identifier;
every identifier maps to a repository location;
every active official document is represented;
document status is identifiable;
document ownership is governed;
naming conventions are followed;
numbering is unique;
registry and INDEX are reconcilable;
registry and PLN-003 are reconcilable;
registry and MDB-001 are explainably aligned;
historical documents are distinguishable from active documents.
# 34. Registry Reconciliation

Registry reconciliation should compare at minimum:

Filesystem Inventory
        |
        v
Document Identifiers
        |
        v
DOC-REGISTRY
        |
        v
INDEX
        |
        v
PLN-003
        |
        v
MDB-001

Differences must be classified as:

missing document;
undocumented document;
historical document;
planned document;
retired document;
naming mismatch;
identifier mismatch;
status mismatch;
location mismatch.

No discrepancy should be silently ignored when it affects official document identity or governance.

# 35. Governance Authority

DOC-REGISTRY is governed under:

HC-000 — Project Constitution
HC-011 — Documentation Governance

Planning alignment is maintained through:

MDB-001 — Master Document Blueprint
PLN-001 — Document Roadmap
PLN-002 — Document Dependency
PLN-003 — Document Status
# 36. Review Cycle

DOC-REGISTRY must be reviewed:

every major release;
when a controlled document is added;
when a controlled document is retired;
when document structure changes;
when governance changes;
when architecture baseline changes materially;
when documentation reconciliation identifies inconsistency.
# 37. Revision History
Version	Date	Change
2.0	Previous Baseline	Established controlled document prefix registry, numbering, versioning, and repository authority.
2.1	2026-08-26	Expanded registry into controlled official document inventory, identifier strategy, filename standard, lifecycle, governance, reconciliation, and traceability model.
# 38. Current Registry Status

Registry Type:

Controlled Enterprise Document Registry

Status:

Approved

Version:

2.1

Repository Baseline:

feature/docs-refactor-v2

Last Structural Validation:

2026-08-26

Repository Authority:

Git Repository
Final Statement

DOC-REGISTRY.md is the controlled inventory and governance registry for official MAJE Enterprise documentation.

The registry establishes document identity, numbering, naming, lifecycle, ownership, status, location, and traceability.

It must remain synchronized with the enterprise documentation architecture and its governing planning documents.

Governance
    |
    v
Foundation
    |
    v
Planning
    |
    v
Architecture
    |
    v
Implementation
    |
    v
Evidence
    |
    v
Assessment
    |
    v
Controlled Documentation Registry
    |
    v
Navigation Index

The registry does not itself constitute production readiness, architecture approval, implementation approval, or closure of any GAP-001 finding.

Those decisions remain subject to their applicable governance, evidence, assessment, and approval processes.
