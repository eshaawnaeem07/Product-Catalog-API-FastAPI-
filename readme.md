# 🚀 FastAPI Product Catalog API

A backend REST API built using **FastAPI**, **SQLAlchemy**, **JWT Authentication**, and **Alembic Migrations**.

This project demonstrates secure API development with authentication, database integration, protected routes, and production-ready architecture.

---

# 📌 What This Project Demonstrates

This project showcases the following backend development concepts:

## ✅ 1. REST API Development (FastAPI)

- User Registration  
- User Login  
- Category CRUD APIs  
- Protected Routes  

Implements standard REST principles using HTTP methods.

---

## ✅ 2. Authentication & Authorization (JWT)

- Secure user login  
- JWT token generation  
- Protected endpoints using token validation  
- Authorization header handling  

---

## ✅ 3. Database Integration (SQLAlchemy ORM)

- Model creation (`User`, `Category`)  
- CRUD operations  
- Relationships & constraints  
- Session management  

---

## ✅ 4. Database Migrations (Alembic)

- Schema version control  
- Auto-generated migrations  
- Upgrade/Downgrade database versions  
- Production-ready migration workflow  

---

Follows modular architecture and separation of concerns.

---

# 🔄 Project Life Cycle

## 1️⃣ Requirement Gathering

- User authentication  
- Category management  
- Protected APIs  

---

## 2️⃣ Database Design

- Designed `User` and `Category` tables  
- Defined primary keys & relationships  

---

## 3️⃣ Model Creation

SQLAlchemy models define database structure.

---

## 4️⃣ Migration Setup

Using Alembic:

```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

5️⃣ API Development

Routes defined using FastAPI

Schemas used for validation

Dependency injection used for auth & DB sessions

6️⃣ Testing via Swagger

FastAPI automatically provides:

/docs

Interactive API testing interface.

## 🌐 API Request Life Cycle

### Example: `POST /categories`

---

## 1️⃣ Request from Frontend

```http
POST /categories
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "name": "Electronics"
}
The frontend sends a request with a JWT token in the Authorization header and JSON data in the request body.

## 2️⃣ Router Matches Endpoint

FastAPI matches the incoming request to the correct route handler based on:

HTTP method (POST)
URL path (/categories)

## 3️⃣ Dependency Injection Executes

Before executing the route logic, FastAPI runs dependencies:

- `get_db()` → Creates a database session  
- `get_current_user()` → Validates the JWT token  

If the token is invalid or missing → **401 Unauthorized**

---

## 4️⃣ JWT Validation

Inside `get_current_user()`:

- Token is decoded  
- Signature is verified  
- Expiration time is checked  
- User is fetched from the database  

If validation fails → **Access denied**

---

## 5️⃣ Request Validation (Pydantic)

The request body is validated using Pydantic schemas:

- Required fields are checked  
- Data types are validated  

If validation fails → **422 Unprocessable Entity**

---

## 6️⃣ Business Logic Execution

- A new category object is created  
- The object is added to the database session  
- The transaction is committed  

---

## 7️⃣ Response Returned

```json
{
  "id": 1,
  "name": "Electronics"
}

🔄 Protection Flow

User logs in
Server generates a JWT token
Frontend stores the token
Every protected request includes:
Authorization: Bearer <token>
The token is validated before executing route logic
If valid → ✅ Access granted
If invalid → ❌ 401 Unauthorized


# 📘 Quick Glossary

| Term | Meaning |
|------|----------|
| **FastAPI** | Modern, high-performance Python web framework |
| **ORM** | Object Relational Mapper |
| **SQLAlchemy** | Python ORM for database interaction |
| **Alembic** | Database migration tool for SQLAlchemy |
| **JWT** | JSON Web Token for authentication |
| **Dependency Injection** | Automatic dependency management in FastAPI |
| **Pydantic** | Data validation and parsing library |
| **Migration** | Database schema version control |
| **CRUD** | Create, Read, Update, Delete operations |
| **Schema** | Request/response data structure |
| **Protected Route** | Endpoint requiring authentication |