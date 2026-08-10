# ARC-002 — Backend Architecture

## HARDYNATTA CHUNG Enterprise Software Engineering Ecosystem

| Item | Value |
|---|---|
| Document ID | ARC-002 |
| Document Name | Backend Architecture |
| Project | MAJE Platform |
| Category | Architecture |
| Version | 2.0 |
| Status | Approved |
| Owner | Engineering Team |
| Governance Authority | HC-000 Project Constitution |
| Parent Architecture | ARC-001 System Architecture |
| Foundation References | FDN-001, FDN-002, FDN-003, FDN-004, FDN-005 |
| Planning References | MASTER_DOCUMENT_BLUEPRINT, DOCUMENT_ROADMAP, DOCUMENT_DEPENDENCY, DOCUMENT_STATUS |
| Specialized Architecture Relationship | ARC-005, ARC-006, ARC-007, ARC-008, ARC-009 |
| Review Cycle | Every Major Release |

---

# 1. Purpose

ARC-002 mendefinisikan arsitektur backend MAJE Platform sebagai specialized architecture di bawah ARC-001 System Architecture.

Dokumen ini menjadi acuan utama untuk struktur, tanggung jawab, boundary, dependency, integration, security, testing, deployment, dan evolution backend.

---

# 2. Architecture Role

ARC-002 merupakan specialized architecture document.

ARC-001 menetapkan system-level architecture.

ARC-002 menerjemahkan system architecture tersebut menjadi backend architecture.

ARC-002 tidak menggantikan ARC-001.

---

# 3. Architectural Scope

Scope ARC-002 meliputi:

- backend application;
- REST API;
- authentication;
- authorization;
- business services;
- repositories;
- schemas;
- database access;
- configuration;
- middleware;
- exception handling;
- AI integration boundary;
- background processing boundary;
- observability boundary;
- testing;
- deployment relationship.

---

# 4. Architectural Authority

Backend architecture harus konsisten dengan:

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

# 5. Backend Architectural Principles

Backend MAJE mengikuti prinsip:

- API First;
- Security by Design;
- Separation of Concerns;
- Dependency Inversion;
- Explicit Boundaries;
- Stateless Application Services;
- Transaction Integrity;
- Consistent Error Handling;
- Observable Operations;
- Testable Components;
- Evolutionary Architecture.

---

# 6. Backend System Boundary

Backend berada di antara client-facing applications dan internal platform capabilities.

Backend bertanggung jawab terhadap application behavior dan controlled access terhadap persistent data.

Backend tidak mengambil alih tanggung jawab frontend, database infrastructure, deployment infrastructure, atau AI implementation yang berada pada architecture domain masing-masing.

---

# 7. Backend Context

Backend menerima request dari:

- web frontend;
- future mobile clients;
- trusted internal services;
- approved integration clients.

Backend berkomunikasi dengan:

- PostgreSQL;
- AI services;
- external integrations;
- observability infrastructure.

---

# 8. High-Level Backend Architecture

```text
Client
  |
  v
API Boundary
  |
  v
Middleware / Dependencies
  |
  v
API Layer
  |
  v
Service Layer
  |
  +----------------------+
  |                      |
  v                      v
Repository Layer      Integration Layer
  |                      |
  v                      +---- AI Service
PostgreSQL               |
                         +---- External Services
```

---

# 9. Architectural Layers

Backend architecture terdiri dari:

- API layer;
- dependency and middleware layer;
- service layer;
- domain/application logic;
- repository layer;
- schema layer;
- model/data layer;
- integration layer;
- infrastructure support.

Setiap layer memiliki tanggung jawab yang berbeda.

---

# 10. API Layer

API layer bertanggung jawab terhadap:

- HTTP endpoint;
- request handling;
- authentication dependency;
- authorization dependency;
- input validation;
- service invocation;
- response serialization;
- HTTP status handling.

API layer tidak boleh menjadi tempat utama business logic.

---

# 11. Service Layer

Service layer bertanggung jawab terhadap:

- business workflow;
- orchestration;
- business rules;
- transaction coordination;
- authorization-aware operations;
- integration orchestration.

Service layer menjadi boundary utama antara API dan persistence.

---

# 12. Repository Layer

Repository layer bertanggung jawab terhadap:

- database queries;
- persistence operations;
- entity retrieval;
- entity creation;
- entity update;
- entity deletion;
- transaction-aware persistence.

Repository tidak boleh mengambil alih business policy.

---

# 13. Schema Layer

Schema layer menggunakan Pydantic untuk:

- request validation;
- response serialization;
- data contract;
- input normalization;
- API-facing validation.

Schema harus dipisahkan dari persistence model apabila diperlukan.

---

# 14. Model Layer

Model layer merepresentasikan persistence entities.

SQLAlchemy models bertanggung jawab terhadap:

- table mapping;
- relationship mapping;
- persistence metadata;
- database-level representation.

Model tidak boleh menjadi pengganti service layer.

---

# 15. Dependency Injection

FastAPI dependency injection digunakan untuk:

- database session;
- current user;
- authentication;
- authorization;
- configuration;
- shared request dependencies.

Dependency harus reusable dan memiliki boundary yang jelas.

---

# 16. Request Lifecycle

Request lifecycle secara umum:

```text
HTTP Request
    |
    v
Middleware
    |
    v
Authentication
    |
    v
Authorization
    |
    v
Validation
    |
    v
API Endpoint
    |
    v
Service
    |
    v
Repository / Integration
    |
    v
Response
```

---

# 17. Authentication Architecture

Authentication memastikan identitas client atau user.

MAJE menggunakan token-based authentication sebagai baseline backend authentication mechanism.

JWT digunakan untuk authentication flow sesuai security governance.

---

# 18. Authorization Architecture

Authentication tidak sama dengan authorization.

Authorization menentukan apakah authenticated principal memiliki hak untuk menjalankan operation tertentu.

Authorization harus diterapkan secara konsisten pada protected resources.

---

# 19. RBAC Architecture

MAJE menggunakan Role-Based Access Control sebagai authorization baseline.

RBAC dapat melibatkan:

- user;
- role;
- permission;
- protected operation.

Authorization policy harus dipusatkan pada security boundary dan tidak tersebar secara tidak konsisten pada endpoint.

---

# 20. Current User Context

Backend menyediakan mekanisme untuk memperoleh authenticated user context.

Current user context digunakan oleh:

- authorization;
- audit;
- business rules;
- ownership checks;
- personalization apabila diperlukan.

---

# 21. Password Security

Password tidak boleh disimpan dalam plaintext.

Backend harus menggunakan secure password hashing.

Password verification dilakukan melalui security service atau security utility yang terkontrol.

---

# 22. Token Security

JWT implementation harus memperhatikan:

- signing algorithm;
- secret management;
- token expiration;
- claims;
- subject identity;
- validation;
- revocation strategy apabila dibutuhkan.

Secrets tidak boleh disimpan dalam source code.

---

# 23. API Architecture

API MAJE menggunakan REST-oriented HTTP interfaces.

API harus memiliki:

- predictable resource naming;
- consistent HTTP semantics;
- consistent response structure;
- authentication rules;
- authorization rules;
- validation;
- documented contracts.

---

# 24. API Routing

Endpoint routing dikelompokkan berdasarkan domain atau capability.

Contoh baseline:

```text
/auth
/users
/provinces
/cities
/dashboard
```

Route organization harus tetap konsisten dengan API governance.

---

# 25. API Versioning

API versioning harus dikendalikan secara eksplisit.

Apabila versioned API path digunakan, format baseline adalah:

```text
/api/v1/
```

Perubahan breaking contract harus melalui versioning policy.

---

# 26. API Response Contract

API response harus konsisten.

Baseline response envelope:

```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {},
  "errors": null
}
```

Response contract harus dikendalikan oleh HC-004 API Governance.

---

# 27. Pagination

Collection endpoints harus mendukung pagination apabila dataset dapat berkembang secara signifikan.

Pagination harus memiliki:

- page or offset strategy;
- page size control;
- stable ordering;
- predictable metadata.

---

# 28. Filtering and Sorting

Collection APIs dapat mendukung:

- filtering;
- sorting;
- search;
- pagination.

Parameter harus divalidasi dan tidak boleh memungkinkan arbitrary unsafe database expressions.

---

# 29. Input Validation

Seluruh external input harus divalidasi.

Validation dilakukan pada:

- request body;
- path parameter;
- query parameter;
- headers apabila relevan.

Pydantic menjadi baseline validation mechanism.

---

# 30. Output Validation

Response data harus sesuai dengan declared response schema.

Output validation membantu menjaga:

- API contract;
- data consistency;
- client compatibility;
- documentation accuracy.

---

# 31. Error Architecture

Backend menggunakan centralized error handling.

Error architecture harus menghasilkan:

- predictable HTTP status;
- consistent response;
- safe public message;
- useful internal logging;
- correlation information apabila tersedia.

---

# 32. Exception Hierarchy

Application exceptions harus memiliki hierarchy yang jelas.

Contoh kategori:

- validation error;
- authentication error;
- authorization error;
- resource not found;
- conflict;
- business rule violation;
- integration failure;
- internal error.

---

# 33. HTTP Status Semantics

Backend menggunakan HTTP status sesuai semantic meaning.

Contoh:

- 200 OK;
- 201 Created;
- 204 No Content;
- 400 Bad Request;
- 401 Unauthorized;
- 403 Forbidden;
- 404 Not Found;
- 409 Conflict;
- 422 Unprocessable Entity;
- 500 Internal Server Error.

---

# 34. Transaction Management

Transaction boundary harus dikendalikan secara eksplisit.

Service workflow yang membutuhkan atomicity harus menggunakan transaction yang sesuai.

Repository tidak boleh membuat transaction behavior yang bertentangan dengan service orchestration.

---

# 35. Database Session

Database session dikelola melalui controlled dependency mechanism.

Session harus:

- dibuat sesuai request/work scope;
- digunakan secara konsisten;
- di-close setelah selesai;
- tidak bocor antar-request.

---

# 36. Database Access

Backend menggunakan SQLAlchemy sebagai database access layer.

Database persistence baseline menggunakan PostgreSQL.

Database access harus mengikuti HC-005 Database Governance.

---

# 37. PostgreSQL Architecture

PostgreSQL merupakan primary relational database untuk MAJE backend.

Database bertanggung jawab terhadap:

- persistence;
- relational integrity;
- constraints;
- indexing;
- transaction consistency.

---

# 38. Migration Architecture

Alembic digunakan untuk schema migration.

Migration harus:

- version controlled;
- deterministic;
- reviewable;
- reversible apabila memungkinkan;
- tidak dilakukan secara manual di production tanpa governance.

---

# 39. Database Integrity

Backend harus menghormati database constraints.

Integrity dapat menggunakan:

- primary keys;
- foreign keys;
- unique constraints;
- not-null constraints;
- indexes;
- check constraints apabila diperlukan.

---

# 40. Repository Query Discipline

Repository queries harus:

- explicit;
- maintainable;
- parameterized;
- testable;
- efficient.

Raw SQL hanya digunakan apabila memiliki alasan teknis yang jelas.

---

# 41. ORM Discipline

SQLAlchemy ORM digunakan sebagai abstraction layer.

ORM models tidak boleh digunakan untuk menyembunyikan business rules yang seharusnya berada pada service/domain layer.

---

# 42. Configuration Architecture

Configuration dikelola melalui environment-aware configuration.

Pydantic Settings menjadi baseline configuration mechanism.

Configuration harus memisahkan:

- application settings;
- database settings;
- security settings;
- environment settings;
- integration settings.

---

# 43. Environment Separation

Backend mendukung environment separation.

Minimum conceptual environments:

```text
development
testing
staging
production
```

Configuration antar-environment tidak boleh tercampur.

---

# 44. Secrets Management

Secrets harus berasal dari secure environment configuration.

Contoh secrets:

- JWT secret;
- database credentials;
- external API keys;
- integration credentials.

Secrets tidak boleh masuk repository.

---

# 45. Middleware Architecture

Middleware digunakan untuk cross-cutting concerns.

Contoh:

- request logging;
- correlation identifier;
- CORS;
- security headers;
- timing;
- exception processing.

Business logic tidak boleh ditempatkan di middleware.

---

# 46. CORS

CORS configuration harus explicit.

Development environment dapat menggunakan policy yang lebih fleksibel.

Production harus menggunakan allowlist yang terkontrol.

---

# 47. Request Logging

Backend harus menyediakan request-level logging.

Minimum information dapat meliputi:

- method;
- path;
- status;
- duration;
- request identifier.

Sensitive information tidak boleh masuk log.

---

# 48. Audit Logging

Operation yang memiliki security atau governance significance harus dapat diaudit.

Audit logging dapat mencatat:

- actor;
- action;
- resource;
- timestamp;
- outcome.

---

# 49. Observability Boundary

Backend menyediakan telemetry boundary untuk:

- logs;
- metrics;
- health state;
- request timing;
- error monitoring.

Detail observability berada pada ARC-009.

---

# 50. Health Check

Backend menyediakan health endpoint atau equivalent health mechanism.

Health check digunakan untuk menentukan apakah application process aktif.

---

# 51. Readiness

Readiness berbeda dengan liveness.

Readiness dapat mempertimbangkan dependency penting seperti database.

Backend deployment environment harus dapat menggunakan readiness signal.

---

# 52. Application Startup

Startup process harus:

- load configuration;
- initialize required components;
- establish necessary infrastructure;
- expose service only when ready.

Startup failure harus menghasilkan diagnosable error.

---

# 53. Application Shutdown

Shutdown harus dilakukan secara graceful.

Application harus memberikan kesempatan untuk:

- finish safe operations;
- release resources;
- close database connections;
- stop background activity.

---

# 54. AI Integration Boundary

Backend dapat berkomunikasi dengan AI Service.

AI integration harus melalui explicit service boundary.

Backend tidak boleh mencampurkan AI-specific implementation dengan core API handlers.

---

# 55. AI Request Flow

Baseline AI flow:

```text
Client
  |
  v
Backend API
  |
  v
Application Service
  |
  v
AI Integration Service
  |
  v
AI Service
  |
  v
Backend
  |
  v
Client
```

---

# 56. AI Failure Handling

AI service failure harus diperlakukan sebagai integration failure.

Backend harus:

- timeout;
- handle unavailable service;
- avoid exposing internal details;
- log failure;
- return controlled response.

---

# 57. External Integration

External services harus diakses melalui integration boundary.

Integration code tidak boleh tersebar langsung pada API endpoints.

---

# 58. Integration Contracts

External integration contract harus mendefinisikan:

- request;
- response;
- authentication;
- timeout;
- retry;
- error behavior.

Detail contract dapat berada pada ARC-006.

---

# 59. Timeout Policy

External calls harus memiliki explicit timeout.

Tidak boleh ada indefinite blocking terhadap external dependency.

---

# 60. Retry Policy

Retry hanya boleh digunakan untuk failure yang memang retryable.

Retry harus mempertimbangkan:

- idempotency;
- backoff;
- maximum attempts;
- downstream load.

---

# 61. Idempotency

Operations yang berpotensi menghasilkan duplicate side effects harus mempertimbangkan idempotency.

Idempotency mechanism harus disesuaikan dengan operation type.

---

# 62. Background Processing

Backend architecture menyediakan boundary untuk background processing.

Background jobs digunakan untuk workload yang tidak perlu menyelesaikan HTTP request secara synchronous.

---

# 63. Background Job Technology

Celery dan Redis belum dianggap sebagai mandatory runtime component apabila belum menjadi bagian dari deployed runtime architecture.

Penggunaan future background infrastructure harus melalui architecture decision dan implementation validation.

---

# 64. Cache Architecture

Caching merupakan optional capability.

Redis dapat digunakan sebagai future caching infrastructure apabila kebutuhan scalability dan performance telah tervalidasi.

Cache tidak boleh menjadi source of truth untuk transactional data.

---

# 65. Concurrency

Backend harus aman terhadap concurrent requests.

Application code tidak boleh bergantung pada mutable global state untuk request-specific information.

---

# 66. Statelessness

Backend API service sebaiknya stateless pada application layer.

State persistent disimpan pada appropriate persistence or infrastructure service.

---

# 67. Scalability

Backend architecture dirancang agar dapat berkembang secara horizontal.

Scalability harus mempertahankan:

- stateless API behavior;
- database integrity;
- controlled connection pooling;
- predictable resource consumption.

---

# 68. Performance

Performance optimization harus berdasarkan measurement.

Area yang dapat dioptimalkan:

- query performance;
- indexing;
- serialization;
- connection pooling;
- external calls;
- caching.

Premature optimization harus dihindari.

---

# 69. Connection Pooling

Database connection pooling harus dikendalikan oleh SQLAlchemy engine configuration.

Pool configuration harus disesuaikan dengan deployment capacity.

---

# 70. Resource Management

Backend harus mengelola:

- database sessions;
- file handles;
- network connections;
- external clients;
- background resources.

Resource leakage harus dianggap sebagai engineering defect.

---

# 71. Security Boundary

Backend security mencakup:

- authentication;
- authorization;
- input validation;
- secret protection;
- secure headers;
- dependency security;
- audit logging.

Detail security architecture berada pada ARC-007.

---

# 72. Security by Design

Security harus dipertimbangkan sejak design dan implementation.

Security bukan tahap terakhir sebelum deployment.

---

# 73. Authorization Enforcement

Authorization enforcement harus terjadi sebelum protected business operation dijalankan.

Endpoint yang membutuhkan elevated privileges harus memiliki explicit policy.

---

# 74. Data Exposure Control

Backend hanya boleh mengembalikan data yang authorized untuk requester.

Response schema harus membantu mencegah accidental data exposure.

---

# 75. Sensitive Data Handling

Sensitive data harus:

- minimized;
- protected;
- excluded from logs;
- excluded from error messages;
- transmitted securely.

---

# 76. Dependency Security

Third-party dependencies harus dikelola secara version controlled.

Security vulnerabilities harus ditangani melalui dependency update process.

---

# 77. API Documentation

API harus terdokumentasi melalui OpenAPI-compatible documentation.

FastAPI-generated OpenAPI menjadi baseline API documentation mechanism.

---

# 78. OpenAPI Governance

OpenAPI specification harus konsisten dengan implementation.

Changes terhadap API contract harus mengikuti HC-004 API Governance.

Generated artifacts tidak boleh diedit secara manual sebagai source of truth.

---

# 79. Testing Architecture

Backend testing harus mencakup:

- unit tests;
- service tests;
- repository tests;
- API tests;
- authentication tests;
- authorization tests;
- integration tests.

---

# 80. Unit Testing

Unit tests digunakan untuk business logic dan isolated components.

Unit tests harus cepat dan deterministic.

---

# 81. API Testing

API tests harus memverifikasi:

- status code;
- response contract;
- validation;
- authentication;
- authorization;
- error behavior.

---

# 82. Authentication Testing

Authentication tests harus mencakup:

- valid credentials;
- invalid credentials;
- expired token;
- malformed token;
- missing token.

---

# 83. Authorization Testing

Authorization tests harus mencakup:

- allowed role;
- denied role;
- missing permission;
- protected endpoint;
- resource ownership apabila berlaku.

---

# 84. Database Testing

Database tests harus memverifikasi:

- persistence;
- relationships;
- constraints;
- migrations;
- transaction behavior.

---

# 85. Integration Testing

Integration testing memverifikasi interaction antar component.

Contoh:

```text
API
 |
 v
Service
 |
 v
Repository
 |
 v
PostgreSQL
```

---

# 86. Test Data Management

Test data harus isolated dari production data.

Seed data untuk testing harus deterministic dan reproducible.

---

# 87. Code Quality

Backend implementation harus mengikuti:

- HC-003 Coding Standard;
- maintainability principles;
- type safety where applicable;
- explicit naming;
- small focused functions;
- controlled complexity.

---

# 88. Dependency Management

Python dependencies harus dikelola secara explicit.

Dependency specification harus version controlled.

Unused dependency harus dihapus apabila tidak diperlukan.

---

# 89. Python Runtime

Backend runtime harus menggunakan Python version yang didukung oleh project baseline.

Perubahan major/minor runtime harus melalui compatibility validation.

---

# 90. FastAPI Runtime

FastAPI menjadi application framework utama backend.

Uvicorn digunakan sebagai ASGI server baseline untuk development dan appropriate deployment configurations.

---

# 91. Docker Architecture

Development backend dijalankan dalam Docker environment sebagai bagian dari MAJE development stack.

Baseline relationship:

```text
Docker Compose
      |
      +-- Backend Container
      |
      +-- PostgreSQL Container
```

---

# 92. Docker Backend Container

Backend container harus:

- memiliki reproducible build;
- expose application port;
- memiliki health mechanism;
- menggunakan environment configuration;
- tidak menyimpan persistent application state di container filesystem.

---

# 93. Development Container

Development environment dapat menggunakan bind mount untuk source synchronization.

Hot reload dapat digunakan untuk development.

Development configuration tidak boleh dianggap sebagai production configuration.

---

# 94. Production Deployment Relationship

ARC-002 mendefinisikan backend application architecture.

Deployment topology dan infrastructure detail berada pada ARC-008 Deployment Architecture.

---

# 95. Backend and Database Relationship

Backend memiliki controlled dependency terhadap PostgreSQL.

Database tidak boleh dianggap sebagai implementation detail yang dapat diubah tanpa migration governance.

---

# 96. Backend and Security Relationship

Security control backend harus mengikuti ARC-007 Security Architecture.

ARC-002 mendefinisikan security integration point.

ARC-007 mendefinisikan specialized security controls.

---

# 97. Backend and Observability Relationship

Backend menghasilkan telemetry yang dibutuhkan oleh observability architecture.

ARC-009 mendefinisikan specialized observability architecture.

ARC-002 bertanggung jawab memastikan application events dapat di-observe.

---

# 98. Backend and Integration Relationship

External service communication mengikuti ARC-006 Integration Architecture.

Backend integration layer menjadi implementation boundary.

---

# 99. Backend and Database Architecture Relationship

Database-specific architecture berada pada ARC-005.

ARC-002 mendefinisikan bagaimana backend menggunakan persistence layer.

ARC-005 mendefinisikan database architecture secara specialized.

---

# 100. Backend Architecture Dependency Map

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
      ARC-002
          |
          +-- ARC-005 Database
          +-- ARC-006 Integration
          +-- ARC-007 Security
          +-- ARC-008 Deployment
          +-- ARC-009 Observability
```

---

# 101. Backend Component Dependency

```text
API
 |
 +--> Dependencies
 |
 +--> Services
        |
        +--> Repositories
        |      |
        |      +--> SQLAlchemy
        |             |
        |             +--> PostgreSQL
        |
        +--> Integration Services
               |
               +--> AI / External Services
```

---

# 102. Backend Architecture Completion

ARC-002 v2.0 establishes the governed backend architecture baseline for MAJE Platform.

The architecture separates API, application, persistence, integration, security, and infrastructure responsibilities.

---

# 103. Document Control

ARC-002 is governed under HC-011 Documentation Governance.

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
| 1.0 | 2026-07-20 | Initial Backend Architecture |
| 2.0 | 2026-08-10 | Refactored as governed specialized Backend Architecture under ARC-001; established backend boundaries, API, service, repository, security, integration, testing, deployment, and observability relationships |

---

# Final Statement

ARC-002 — Backend Architecture

HARDYNATTA CHUNG Enterprise Software Engineering Ecosystem

Version 2.0 — Governed Specialized Backend Architecture

The backend architecture connects system-level intent with secure, maintainable, testable, observable, and evolvable application implementation.
