# HC-002 — Development Workflow

**Document ID:** HC-002  
**Project:** MAJE Platform  
**Category:** Engineering Documentation  
**Status:** Approved  
**Version:** 1.0  

---

# 1. Purpose

Dokumen ini mendefinisikan workflow pengembangan software MAJE.

Development Workflow menjadi standar bagi seluruh engineer dalam:

- membuat perubahan kode
- mengembangkan fitur baru
- melakukan review
- melakukan testing
- melakukan deployment

---

# 2. Development Lifecycle

MAJE menggunakan lifecycle:
Planning
↓
Development
↓
Testing
↓
Code Review
↓
Integration
↓
Release
↓
Monitoring
---

# 3. Branch Strategy

Struktur branch:
main
|
└── develop
|
├── feature/*
├── bugfix/*
└── hotfix/*
## main

Fungsi:

- production branch
- kode stabil
- deployment resmi

---

## develop

Fungsi:

- integrasi fitur
- testing sebelum release

---

## feature/*

Digunakan untuk:

- fitur baru
- perubahan besar

Format:
feature/nama-fitur
Contoh:
feature/user-authentication
feature/payment-module

---

## bugfix/*

Digunakan untuk:

- perbaikan bug non-critical

Contoh:
bugfix/login-error

---

## hotfix/*

Digunakan untuk:

- masalah production urgent

Contoh:
hotfix/security-patch

---

# 4. Feature Development Flow

Alur standar:
Create Branch
↓
Develop Feature
↓
Run Tests
↓
Create Pull Request
↓
Code Review
↓
Merge
↓
Deploy

---

# 5. Commit Convention

MAJE menggunakan conventional commit.

Format:
type: description

Jenis:

| Type | Fungsi |
|---|---|
| feat | fitur baru |
| fix | bug fix |
| docs | dokumentasi |
| refactor | perubahan struktur kode |
| test | testing |
| chore | maintenance |

Contoh:
feat: add user authentication

fix: resolve login validation issue

docs: update API documentation

---

# 6. Pull Request Policy

Setiap perubahan wajib melalui:

- Pull Request
- Review
- Testing

Minimum:

- 1 reviewer
- CI validation berhasil
- tidak ada conflict

---

# 7. Code Review Standard

Reviewer memeriksa:

## Architecture

- sesuai struktur MAJE
- tidak melanggar separation of concern

## Security

- authentication
- authorization
- data protection

## Quality

- readable code
- maintainability
- testing coverage

---

# 8. Testing Requirement

Sebelum merge:

Wajib:
Unit Test
Integration Test
API Test

Tidak diperbolehkan merge jika:

- test gagal
- error kritikal ditemukan
- dokumentasi tidak diperbarui

---

# 9. Release Workflow

Release:
develop
↓
Release Branch
↓
Testing
↓
main
↓
Production
---

# 10. Emergency Procedure

Untuk kondisi kritis:
main
↓
hotfix/*
↓
review
↓
production deployment
---

# 11. Developer Responsibility

Setiap developer bertanggung jawab:

- menjaga kualitas kode
- mengikuti standar repository
- memperbarui dokumentasi
- melakukan testing
- menjaga keamanan sistem

---

# 12. Document History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-18 | Initial Development Workflow |