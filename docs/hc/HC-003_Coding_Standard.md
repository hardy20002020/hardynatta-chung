# HC-003 — Coding Standard

**Document ID:** HC-003  
**Project:** MAJE Platform  
**Category:** Engineering Documentation  
**Status:** Approved  
**Version:** 1.0  

---

# 1. Purpose

Dokumen ini mendefinisikan standar penulisan kode pada MAJE Platform.

Coding Standard bertujuan memastikan:

- konsistensi antar developer
- kode mudah dibaca dan dipelihara
- kualitas software terjaga
- scalable untuk pengembangan enterprise

---

# 2. General Principles

MAJE menggunakan prinsip:

- Clean Code
- Separation of Concern
- Explicit over Implicit
- Maintainability First

Kode harus:

- mudah dipahami
- memiliki tanggung jawab jelas
- memiliki dokumentasi
- memiliki testing

---

# 3. Programming Language Standard

Backend MAJE menggunakan:


Python 3.x
FastAPI Framework
SQLAlchemy ORM
Pydantic Schema


Frontend mengikuti:


TypeScript
Modern JavaScript Framework


---

# 4. Naming Convention

## File

Gunakan:


snake_case


Contoh:


user_service.py
auth_controller.py
payment_repository.py


---

## Class

Gunakan:


PascalCase


Contoh:

```python
class UserService:
    pass
Function

Gunakan:

snake_case

Contoh:

def create_user():
    pass
Variable

Gunakan:

user_name
access_token
5. Backend Structure Standard

Struktur:

app/

├── api/
├── core/
├── models/
├── schemas/
├── services/
├── repositories/
├── exceptions/
└── main.py

Aturan:

API Layer

Bertanggung jawab:

menerima request
validasi input
mengembalikan response

Tidak boleh:

business logic kompleks
Service Layer

Bertanggung jawab:

business rules
workflow aplikasi
Repository Layer

Bertanggung jawab:

database access
query management
6. Type Hint Requirement

Semua function wajib menggunakan type hint.

Contoh:

def get_user(user_id: int) -> User:
    return user

Hindari:

def get_user(user_id):
7. Schema Standard

Pydantic schema digunakan untuk:

request validation
response serialization

Contoh:

class UserCreate(BaseModel):
    username: str
    email: EmailStr
8. Error Handling

Tidak diperbolehkan:

except:
    pass

Gunakan:

raise CustomException()

Semua error harus:

memiliki kode
memiliki message
tercatat di log
9. Logging Standard

Gunakan logging:

logger.info()
logger.warning()
logger.error()

Tidak menggunakan:

print()
10. Security Standard

Developer wajib memperhatikan:

password hashing
input validation
authentication
authorization
secret management

Tidak diperbolehkan:

menyimpan password plaintext
hardcode credential
commit secret ke repository
11. Documentation Requirement

Kode kompleks wajib memiliki:

docstring
komentar seperlunya
dokumentasi perubahan
12. Code Review Checklist

Reviewer memastikan:

mengikuti struktur MAJE
tidak ada duplicate logic
testing tersedia
security diperhatikan
dokumentasi diperbarui
13. Document History
Version	Date	Change
1.0	2026-07-18	Initial Coding Standard

Setelah selesai:

```bash
git add docs/hc/HC-003_Coding_Standard.md

cek:

git status

commit:

git commit -m "docs: add HC-003 Coding Standard"