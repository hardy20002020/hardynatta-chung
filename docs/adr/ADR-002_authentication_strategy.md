ADR-002 — Authentication Strategy

HARDYNATTA CHUNG Enterprise Software Engineering Ecosystem

| Item | Value |
|---|---|
| Document ID | ADR-002 |
| Document Name | Authentication Strategy |
| Version | 1.0 |
| Status | Accepted |
| Owner | HARDYNATTA CHUNG |
| Domain | Architecture Decision Record |
| Governance Authority | HC-010 ADR Governance |
| Primary Platform | MAJE — Mandarin AI Judge Enterprise |
| Decision Type | Security Architecture |
| Decision Scope | MAJE Application Authentication and Authorization |
| Review Cycle | When security architecture, identity requirements, or authentication technology materially change |

---

# 1. Purpose

ADR-002 records the architectural decision to use token-based authentication with JSON Web Token (JWT) as the baseline application authentication mechanism for MAJE, together with Role-Based Access Control (RBAC) as the authorization model.

This ADR provides controlled historical traceability between:

```text
Governance
↓
Security Architecture
↓
Decision
↓
Implementation
↓
Validation
↓
Evidence
```
This document does not replace ARC-007 Security Architecture, ARC-002 Backend Architecture, the actual authentication implementation, or applicable security governance.

# 2. Context

MAJE requires a controlled identity and access mechanism for protected application resources.

The backend exposes authenticated application operations and protected administrative capabilities.

The current MAJE architecture establishes token-based authentication and Role-Based Access Control as security baselines.

ARC-002 Backend Architecture establishes token-based authentication as the baseline backend authentication mechanism.

ARC-002 also establishes Role-Based Access Control as the authorization baseline.

ARC-007 Security Architecture establishes JWT as the baseline application authentication mechanism and RBAC as the baseline authorization model.

The current backend implementation contains authentication, password handling, token validation, authenticated-user resolution, and authorization enforcement components.

The current MAJE implementation therefore already aligns with the authentication and authorization architecture recorded by this ADR.

# 3. Problem

The enterprise requires a controlled architectural decision identifying how MAJE authenticates users and authorizes protected operations.

Without an explicit decision record:

the authentication technology decision is difficult to trace historically;
authentication and authorization responsibilities may become ambiguous;
alternative approaches are not formally recorded;
future security changes may lack a clear architectural baseline;
implementation and security architecture cannot be linked through a dedicated decision record.

Therefore, the authentication and authorization strategy must be explicitly recorded.

# 4. Decision

## 4.1 Primary Authentication Decision

MAJE will use token-based authentication with JWT as the baseline application authentication mechanism.

JWT-based authentication establishes an authenticated identity that can subsequently be evaluated by the authorization layer.

The authentication mechanism is therefore:

Client
  ↓
Authentication Request
  ↓
Credential Verification
  ↓
JWT Issuance
  ↓
Authenticated Request
  ↓
JWT Validation
  ↓
Authenticated Identity

JWT is the approved baseline token mechanism for the current MAJE application architecture.

## 4.2 Authorization Decision

MAJE will use Role-Based Access Control (RBAC) as the baseline authorization model.

Authorization occurs after successful authentication.

The authorization relationship is:

Authenticated Identity
        ↓
Role
        ↓
Permission / Policy
        ↓
Protected Operation

Authentication establishes identity.

Authorization determines whether the authenticated identity is permitted to perform a protected operation.

These are separate security concerns and must remain separately governed.

## 4.3 Architectural Position

The authentication and authorization boundary is positioned between the client/application request and protected application services.

The baseline relationship is:

Client
  ↓
Authentication
  ↓
JWT Validation
  ↓
Authenticated Identity
  ↓
RBAC Authorization
  ↓
Protected Application Operation

Successful authentication does not automatically grant authorization to every protected operation.

# 5. Authentication Model

## 5.1 Authentication Objective

Authentication establishes that a request is associated with a valid application identity.

The authentication process must verify the supplied credentials according to the applicable security controls.

Upon successful authentication, MAJE issues an application authentication token according to the approved JWT configuration.

## 5.2 Credential Verification

User credentials must be validated using the approved password security mechanism.

Passwords must not be stored as plaintext.

Credential verification must use the application's controlled password hashing and verification implementation.

Authentication failure must not reveal unnecessary information about whether a specific account exists.

## 5.3 JWT Token

JWT is used as the application authentication token mechanism.

The token represents an authenticated application identity and must contain only the claims required by the authentication and authorization architecture.

JWT validation must verify applicable token integrity and validity requirements.

At minimum, validation must consider:

token signature;
token structure;
expiration;
applicable issuer requirements;
applicable audience requirements;
identity claims;
required security claims.

## 5.4 Token Lifetime

JWT tokens must have controlled lifetimes.

Token expiration must be enforced by the authentication layer.

Long-lived tokens must not be introduced without explicit security justification and appropriate architecture review.

Token lifetime requirements may evolve as the security architecture matures.

## 5.5 Token Secret and Signing Configuration

JWT signing secrets or equivalent signing credentials must not be hard-coded into source code.

Authentication secrets must be provided through controlled configuration and appropriate secret-management mechanisms.

Production secrets must be separated from development credentials.

# 6. Authorization Model

## 6.1 RBAC Principle

MAJE uses Role-Based Access Control as the authorization baseline.

A role represents a controlled set of permissions or authorized application capabilities.

Authorization decisions must be based on the authenticated identity and applicable role or permission rules.

## 6.2 Role Assignment

Role assignment must be controlled.

A user must not receive administrative privileges merely because authentication succeeded.

Administrative privileges must be explicitly associated with an authorized role.

## 6.3 Permission Enforcement

Protected application operations must enforce authorization at the appropriate application boundary.

Authorization must not depend solely on frontend visibility or user-interface restrictions.

Backend authorization remains authoritative for protected operations.

## 6.4 Administrative Access

Administrative operations must require appropriate authenticated identity and authorization.

Administrative access must be restricted to identities assigned the required administrative role or permission.

Administrative authorization must be enforced server-side.

## 6.5 Least Privilege

RBAC implementation must follow the principle of least privilege.

Users should receive only the permissions required to perform their authorized responsibilities.

Permissions should not be granted broadly merely for implementation convenience.

# 7. Alternatives Considered

The following authentication and authorization approaches are recognized as possible alternatives.

## 7.1 Alternative A — JWT-Based Token Authentication with RBAC

Selected.

Advantages include:

alignment with the current MAJE backend architecture;
stateless application authentication capability;
compatibility with the current backend security implementation;
clear separation between authentication and authorization;
compatibility with protected API operations;
support for role-based authorization;
compatibility with the current FastAPI-based backend architecture;
suitability for the current MAJE application model.

This alternative is therefore the approved baseline.

## 7.2 Alternative B — Server-Side Session Authentication

Not selected as the current MAJE authentication baseline.

A server-side session model could maintain authenticated sessions on the server and provide session identifiers to clients.

Adopting this model would introduce different requirements for:

session storage;
session lifecycle;
session expiration;
session invalidation;
distributed session handling;
session security;
deployment architecture.

The current architecture does not require replacing JWT-based authentication with server-side sessions.

## 7.3 Alternative C — OAuth 2.0 / OpenID Connect as Primary Identity Architecture

Not selected as the current primary MAJE identity architecture.

OAuth 2.0 and OpenID Connect may become appropriate if MAJE requires:

external identity providers;
enterprise single sign-on;
federated identity;
social login;
centralized identity management;
external authorization delegation.

Such adoption would require a dedicated architecture decision covering identity provider integration, token flows, trust boundaries, claims, lifecycle, security, and operational responsibilities.

OAuth 2.0 or OpenID Connect may therefore complement or supersede the current baseline in the future through a separate governed architecture decision.

## 7.4 Alternative D — API Key Authentication

Not selected as the primary user authentication mechanism.

API keys may be appropriate for selected machine-to-machine integrations.

They do not provide the same identity and authorization model required for the current MAJE user-facing application architecture.

If API keys are introduced for a specialized integration capability, the associated security model must be separately governed.

## 7.5 Alternative E — Basic Authentication

Not selected.

Basic Authentication does not provide the required token lifecycle and application authorization model for the current MAJE architecture.

It also introduces additional credential transmission and operational considerations that are not aligned with the selected application authentication baseline.

# 8. Rationale

The decision is based on the following considerations.

## 8.1 Existing Architecture Alignment

ARC-002 Backend Architecture already establishes token-based authentication as the backend authentication baseline.

ARC-007 Security Architecture establishes JWT as the baseline application authentication mechanism.

This ADR therefore formalizes an existing architectural baseline rather than introducing an unrelated technology.

## 8.2 Existing Implementation Alignment

The current MAJE backend contains authentication and authorization components aligned with the selected architecture.

The backend provides authentication workflows, token handling, authenticated identity resolution, and authorization enforcement.

The implementation therefore provides direct alignment with this ADR.

## 8.3 Separation of Authentication and Authorization

Separating authentication from authorization provides a clear security boundary.

Authentication determines who the requester is.

Authorization determines what the requester is allowed to do.

This separation supports maintainability and controlled security enforcement.

## 8.4 API Architecture Alignment

MAJE exposes protected application operations through backend APIs.

Token-based authentication provides an appropriate mechanism for authenticating API requests without requiring every request to carry reusable plaintext credentials.

## 8.5 RBAC Alignment

MAJE contains administrative and non-administrative application capabilities.

RBAC provides an explicit mechanism for controlling access according to assigned roles.

This aligns with the current backend authorization architecture.

## 8.6 Engineering Ecosystem Alignment

The current backend security ecosystem includes:

FastAPI;
JWT-based token handling;
password hashing and verification;
authenticated-user resolution;
RBAC authorization;
protected API endpoints.

The selected architecture therefore aligns with the current engineering ecosystem.

# 9. Consequences

## 9.1 Positive Consequences

The decision provides:

a clear authentication baseline;
explicit authorization governance;
separation between identity and access control;
compatibility with protected API operations;
server-side authorization enforcement;
role-based administrative access;
traceability between security architecture and implementation;
a controlled baseline for future identity architecture evolution.

## 9.2 Negative Consequences

The decision also creates security and operational responsibilities.

The enterprise must maintain:

JWT signing-key security;
token expiration controls;
authentication failure handling;
password security;
role governance;
permission governance;
authorization enforcement;
security testing;
credential lifecycle management;
authentication configuration management;
security monitoring.

## 9.3 Operational Consequence

JWT-based authentication requires careful management of token lifetime and credential/signing-key security.

Compromise of signing credentials could affect token trust and therefore requires appropriate security controls.

## 9.4 Future Consequence

If MAJE adopts an external identity provider, federated authentication, or a substantially different authentication architecture, the change must be introduced through an appropriate architecture decision.

The existing ADR must not be silently rewritten to conceal the historical decision.

# 10. Implementation

The current MAJE backend provides an authentication and authorization implementation consistent with the selected architecture.

The logical security flow is:

Client
    ↓
Login / Authentication Request
    ↓
Credential Validation
    ↓
JWT Generation
    ↓
Authenticated API Request
    ↓
JWT Verification
    ↓
Current User Resolution
    ↓
RBAC Authorization
    ↓
Protected Endpoint

The backend security implementation includes the relevant authentication and authorization layers.

The implementation may include:

password hashing;
password verification;
JWT creation;
JWT decoding;
JWT validation;
authenticated-user resolution;
role validation;
permission enforcement;
protected endpoint dependencies.

Implementation details remain governed by the applicable backend and security architecture.

# 11. Authentication Boundary

The authentication boundary must be enforced by the backend.

The frontend may provide login interfaces and user experience controls, but frontend behavior must not be treated as the authoritative security boundary.

The authoritative security flow is:

Frontend / Client
       ↓
Backend Authentication
       ↓
JWT Validation
       ↓
Authenticated Identity
       ↓
Backend Authorization
       ↓
Protected Resource

A malicious client must not be able to bypass authorization by modifying frontend state.

# 12. Security Considerations

## 12.1 Password Security

Passwords must never be stored as plaintext.

Password storage must use an approved password hashing mechanism.

Password verification must occur through controlled backend security code.

## 12.2 Secret Management

JWT signing secrets and other authentication secrets must not be committed to source control.

Secrets must be supplied through controlled configuration.

Development, testing, staging, and production credentials must be appropriately separated.

## 12.3 Token Validation

Every protected request must validate the authentication token according to the applicable security requirements.

Expired or invalid tokens must not be accepted.

## 12.4 Token Exposure

Authentication tokens must be protected against unnecessary exposure through:

logs;
error messages;
URLs;
source code;
configuration files;
debugging output.

Sensitive authentication material must not be unnecessarily recorded in application logs.

## 12.5 Authorization Enforcement

Authorization must be enforced at the backend security boundary.

Client-side role checks may improve user experience but must not replace backend authorization.

## 12.6 Administrative Security

Administrative operations require explicit authorization.

Administrative credentials and roles must receive additional security attention because compromise may have broader system impact.

## 12.7 Brute Force Protection

Authentication architecture should support appropriate controls against repeated credential attacks.

Depending on operational requirements, these controls may include:

rate limiting;
login attempt monitoring;
temporary account controls;
anomaly detection;
security alerting.

Such controls may be implemented through the applicable security and operations architecture.

## 12.8 Transport Security

Authentication credentials and tokens must be transmitted through protected communication channels.

HTTPS/TLS is the baseline for protected production communication.

# 13. Reliability and Recovery Considerations

Authentication is a critical dependency for protected MAJE operations.

Therefore the operational architecture must provide appropriate:

health validation;
configuration validation;
authentication service monitoring;
failure handling;
secret management;
deployment validation;
rollback capability.

Authentication configuration changes must be validated before production deployment.

Failure of authentication infrastructure must not result in uncontrolled access to protected operations.

# 14. Observability Considerations

Authentication and authorization events should be observable through the applicable observability architecture.

Relevant signals may include:

authentication failures;
successful authentication events;
expired token events;
invalid token events;
authorization failures;
administrative access attempts;
repeated login failures;
security-related application errors.

Sensitive credentials, passwords, signing secrets, and raw authentication tokens must not be written to logs.

Observability implementation remains governed by the applicable observability and operations documentation.

# 15. Testing Considerations

The authentication architecture requires validation through automated and controlled testing.

Testing should cover:

successful authentication;
invalid credentials;
invalid token;
expired token;
missing token;
authenticated-user resolution;
authorized role access;
unauthorized role access;
administrative authorization;
protected endpoint enforcement;
password verification;
authentication error handling.

Authentication tests must verify both positive and negative security paths.

Successful authentication testing does not by itself prove complete production security readiness.

# 16. Architecture References

This ADR is supported by the following architectural and governance documents.

## 16.1 HC-000 — Project Constitution

Defines the enterprise governance authority and establishes the requirement for significant architecture decisions to be documented through Architecture Decision Records.

## 16.2 HC-010 — ADR Governance

Defines governance and required structure for Architecture Decision Records.

## 16.3 ARC-002 — Backend Architecture

Defines token-based authentication as the baseline backend authentication mechanism and RBAC as the authorization baseline.

## 16.4 ARC-007 — Security Architecture

Defines JWT as the baseline application authentication mechanism and RBAC as the baseline authorization model.

## 16.5 ARC-008 — Deployment Architecture

Defines deployment and operational relationships relevant to protected application services and configuration.

## 16.6 ARC-009 — Observability Architecture

Defines observability relationships for authentication, authorization, application services, and operational monitoring.

# 17. Evidence

The current backend Docker test validation provides objective evidence that the current backend automated test suite executes successfully inside the Docker Compose backend environment.

## 17.1 Evidence Record

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

## 17.2 Evidence Source

docs/evidence/backend/EVIDENCE-002_backend_docker_test_validation.txt

## 17.3 Evidence Interpretation

EVIDENCE-002 provides objective evidence that the backend automated test suite completed successfully in the Docker Compose backend environment.

The evidence supports implementation validation.

However, EVIDENCE-002 does not independently prove every authentication or security requirement.

Security-specific validation remains subject to the applicable architecture, security testing, penetration testing, operational validation, and production readiness requirements.

# 18. Traceability

The authentication decision is traceable through the following chain:

HC-000 Project Constitution
        ↓
HC-010 ADR Governance
        ↓
ARC-002 Backend Architecture
        ↓
ARC-007 Security Architecture
        ↓
ADR-002 Authentication Strategy
        ↓
Authentication Implementation
        ↓
JWT Validation
        ↓
RBAC Authorization
        ↓
Protected Backend Operations
        ↓
Backend Validation
        ↓
EVIDENCE-002

This traceability establishes the relationship between governance, security architecture, architectural decision, implementation, validation, and objective evidence.

# 19. Decision Status

ACCEPTED

The JWT-based token authentication and RBAC authorization strategy is accepted as the current MAJE application security baseline.

This ADR remains applicable until:

the authentication architecture materially changes;
identity requirements materially change;
a different authentication technology is formally approved;
an external identity provider becomes an approved architectural requirement;
JWT is no longer suitable for the applicable system requirements;
a replacement architecture decision is formally approved.

# 20. Review Conditions

ADR-002 must be reviewed when:

the primary authentication mechanism is proposed to change;
JWT configuration or security model materially changes;
RBAC is replaced or materially extended;
external identity federation is introduced;
OAuth 2.0 or OpenID Connect becomes a primary identity architecture;
authentication requirements materially change;
security requirements materially change;
compliance requirements materially change;
significant authentication vulnerabilities are identified;
token lifecycle requirements materially change;
deployment architecture materially changes the authentication trust boundary.

A replacement decision must explicitly supersede this ADR rather than silently modifying the historical decision.

# 21. Governance Rules

This ADR is governed by HC-010 ADR Governance.

Changes must preserve:

decision identity;
decision history;
context;
rationale;
alternatives;
consequences;
implementation relationship;
evidence relationship;
traceability;
auditability.

Historical decisions must not be rewritten to conceal previous architectural choices.

If the authentication strategy changes materially, a new ADR or formally governed superseding decision must be created.

Minor implementation changes that remain within the approved architectural baseline do not automatically require a new ADR.

# 22. Relationship to Implementation

The implementation must remain consistent with the approved authentication architecture.

The following relationship must remain traceable:

Authentication Architecture
        ↓
JWT Authentication
        ↓
Authenticated Identity
        ↓
RBAC Authorization
        ↓
Protected Backend Endpoint

Implementation details may evolve while preserving the architectural decision.

If implementation requires a fundamentally different authentication model, the change must be reviewed through the ADR process.

# 23. Relationship to Production Readiness

ADR-002 establishes an architectural decision.

It does not constitute production security approval.

Production readiness requires additional validation of:

authentication configuration;
secret management;
token security;
authorization enforcement;
transport security;
logging;
monitoring;
vulnerability management;
security testing;
deployment configuration;
operational controls;
incident response capability.

The ADR therefore establishes the architectural baseline but does not independently close production security requirements.

# 24. Relationship to GAP-001

ADR-002 contributes to the remediation of the architecture decision documentation gap identified by GAP-001.

The ADR provides a formal record for a material security architecture decision.

This document should be referenced by the applicable GAP-001 assessment and remediation records.

ADR-002 does not by itself constitute formal closure of GAP-001.

Closure remains subject to the applicable assessment, remediation, validation, and evidence requirements.

# 25. Future Evolution

Future authentication architecture may include additional capabilities such as:

refresh-token mechanisms;
external identity providers;
enterprise single sign-on;
OAuth 2.0;
OpenID Connect;
multi-factor authentication;
stronger administrative authentication;
centralized identity lifecycle management;
service-to-service authentication.

Such capabilities must be introduced according to architectural need and security governance.

Future technology adoption must not silently replace the current authentication baseline.

# 26. Revision History

Version

Date

Change

1.0

2026-08-14

Initial ADR recording JWT-based token authentication and RBAC authorization as the primary MAJE application security baseline

Final Statement

ADR-002 — Authentication Strategy

HARDYNATTA CHUNG Enterprise Software Engineering Ecosystem

Version 1.0 — Accepted Architecture Decision

JWT-based token authentication is the approved baseline application authentication mechanism for MAJE.

Role-Based Access Control is the approved baseline authorization model.

This decision establishes a controlled architectural baseline connecting:

Governance
↓
Security Architecture
↓
Decision
↓
Implementation
↓
Validation
↓
Evidence

Authentication establishes application identity.

Authorization determines whether the authenticated identity is permitted to perform a protected operation.

The backend remains the authoritative security enforcement boundary.

ADR-002 does not by itself constitute production security approval, production readiness, or closure of any GAP-001 finding.

It provides the formal architectural decision record required for security architecture traceability, governance, implementation alignment, and future architectural review.