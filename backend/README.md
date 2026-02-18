# FastAPI CRUD Lab - Item Management API

## Lab Overview

Welcome to the **FastAPI CRUD Lab**! This is a comprehensive, teaching-oriented REST API project designed for a **4-hour hands-on laboratory session** for undergraduate students learning backend development.

This lab will teach you how to build a complete REST API from scratch using modern Python technologies.

---

## Learning Outcomes

After completing this lab, you will be able to:

1. **Explain REST API Concepts** - HTTP methods, status codes, endpoints
2. **Build APIs using FastAPI** - Routes, request/response handling
3. **Design Database Models** - Schema design with Pydantic
4. **Implement CRUD Operations** - Create, Read, Update, Delete
5. **Validate Input Data** - Using Pydantic validators
6. **Test APIs using Swagger UI** - Interactive API testing
7. **Run and Debug Backend Servers** - Using uvicorn and logging

---

## Tech Stack

| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Programming Language | 3.9+ |
| **FastAPI** | Web Framework | 0.110+ |
| **MongoDB** | Database | 4.4+ |
| **Motor** | Async MongoDB Driver | 3.3+ |
| **Pydantic** | Data Validation | 2.6+ |
| **Uvicorn** | ASGI Server | 0.25+ |

---

## Lab Time Breakdown

### Hour 1: Environment Setup & Hello API (60 minutes)

**Topics Covered:**
- Python virtual environment setup
- Installing dependencies
- Understanding project structure
- Creating your first endpoint
- Running the server

**What You'll Build:**
- Health check endpoint
- Root welcome endpoint

### Hour 2: Database, Models & Schemas (60 minutes)

**Topics Covered:**
- MongoDB basics
- Pydantic models and validation
- Request/Response schemas
- Field validation rules

**What You'll Build:**
- Item data model
- Create and Response schemas

### Hour 3: CRUD Operations (60 minutes)

**Topics Covered:**
- HTTP Methods (GET, POST, PUT, DELETE)
- Path and Query parameters
- Error handling with HTTPException
- Database operations

**What You'll Build:**
- Create Item (POST)
- List Items (GET)
- Get Item by ID (GET)
- Update Item (PUT)
- Delete Item (DELETE)

### Hour 4: Testing, Validation & Mini-Assignment (60 minutes)

**Topics Covered:**
- Testing with Swagger UI
- Testing with curl commands
- Input validation
- Error responses
- Mini-assignment implementation

**What You'll Build:**
- Search functionality
- Pagination
- Category filter

---

## Software Requirements

Before starting the lab, ensure you have:

1. **Python 3.9+** - [Download](https://www.python.org/downloads/)
2. **MongoDB** - [Download](https://www.mongodb.com/try/download/community)
3. **Text Editor/IDE** - VS Code recommended
4. **Terminal/Command Prompt**
5. **Web Browser** - For Swagger UI

---

## Installation Steps

### Step 1: Clone or Create Project

```bash
mkdir crud_lab
cd crud_lab
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install fastapi uvicorn motor pydantic python-dotenv
```

### Step 4: Create .env File

```bash
# Create .env file with:
MONGO_URL="mongodb://localhost:27017"
DB_NAME="crud_lab_db"
CORS_ORIGINS="*"
```

### Step 5: Start MongoDB

```bash
# Make sure MongoDB is running on your system
mongod
```

### Step 6: Run the Server

```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

### Step 7: Open Swagger UI

Open your browser and navigate to:
```
http://localhost:8001/api/docs
```

---

## API Endpoint Reference

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| `GET` | `/api/` | Welcome message | 200 |
| `GET` | `/api/health` | Health check | 200, 503 |
| `POST` | `/api/items` | Create new item | 201, 422 |
| `GET` | `/api/items` | List all items (paginated) | 200 |
| `GET` | `/api/items/{id}` | Get item by ID | 200, 404 |
| `PUT` | `/api/items/{id}` | Update item | 200, 404, 422 |
| `DELETE` | `/api/items/{id}` | Delete item | 200, 404 |
| `GET` | `/api/items/stats/summary` | Get statistics | 200 |

---

## Sample curl Requests

### 1. Health Check

```bash
curl -X GET "http://localhost:8001/api/health"
```

**Expected Response:**
```json
{
    "message": "API is healthy!",
    "detail": "Database connection: OK"
}
```

### 2. Create Item

```bash
curl -X POST "http://localhost:8001/api/items" \
     -H "Content-Type: application/json" \
     -d '{
         "name": "Laptop",
         "description": "High-performance laptop for coding",
         "price": 999.99,
         "quantity": 10,
         "category": "Electronics"
     }'
```

**Expected Response:**
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Laptop",
    "description": "High-performance laptop for coding",
    "price": 999.99,
    "quantity": 10,
    "category": "Electronics",
    "created_at": "2024-01-15T10:30:00.000Z",
    "updated_at": "2024-01-15T10:30:00.000Z"
}
```

### 3. List All Items

```bash
curl -X GET "http://localhost:8001/api/items"
```

### 4. List Items with Pagination

```bash
curl -X GET "http://localhost:8001/api/items?page=1&page_size=5"
```

### 5. Search Items by Name

```bash
curl -X GET "http://localhost:8001/api/items?search=laptop"
```

### 6. Filter by Category

```bash
curl -X GET "http://localhost:8001/api/items?category=Electronics"
```

### 7. Get Single Item

```bash
curl -X GET "http://localhost:8001/api/items/{item_id}"
```

### 8. Update Item

```bash
curl -X PUT "http://localhost:8001/api/items/{item_id}" \
     -H "Content-Type: application/json" \
     -d '{
         "price": 899.99,
         "quantity": 15
     }'
```

### 9. Delete Item

```bash
curl -X DELETE "http://localhost:8001/api/items/{item_id}"
```

---

## Exercises

### Exercise 1: Create Multiple Items
Create 5 different items with varying categories:
- Electronics (2 items)
- Books (2 items)  
- Clothing (1 item)

### Exercise 2: Test Validation
Try creating an item with:
- Negative price (should fail)
- Empty name (should fail)
- Missing required fields (should fail)

### Exercise 3: Pagination
1. Create 20 items
2. Retrieve items page by page (page_size=5)
3. Verify total pages calculation

### Exercise 4: Search & Filter
1. Search for items containing "laptop"
2. Filter items by "Electronics" category
3. Combine search and pagination

---

## Mini Assignment

Implement the following features:

### Task 1: Add Category Field (Done)
The category field has already been added to the Item model.

### Task 2: Search by Name (Done)
Search functionality is implemented using the `search` query parameter.

### Task 3: Add Pagination (Done)
Pagination is implemented with `page` and `page_size` parameters.

### Bonus Tasks:
1. Add a `tags` field (list of strings) to items
2. Implement sorting by price (ascending/descending)
3. Add bulk delete endpoint

---

## Viva Questions

### Conceptual Questions:

1. **What is REST API?**
   - REST (Representational State Transfer) is an architectural style for designing networked applications using stateless, client-server communication over HTTP.

2. **What are HTTP methods and when to use each?**
   - GET: Retrieve data
   - POST: Create new resource
   - PUT/PATCH: Update existing resource
   - DELETE: Remove resource

3. **What is the difference between path parameters and query parameters?**
   - Path parameters: Part of URL path (e.g., `/items/123`)
   - Query parameters: After `?` (e.g., `/items?page=1`)

4. **What is Pydantic and why do we use it?**
   - Pydantic is a data validation library that uses Python type hints to validate and serialize data.

5. **What is FastAPI and its advantages?**
   - FastAPI is a modern Python web framework. Advantages: auto-documentation, type hints, async support, fast performance.

6. **What are status codes 200, 201, 400, 404, 500?**
   - 200: OK
   - 201: Created
   - 400: Bad Request
   - 404: Not Found
   - 500: Internal Server Error

7. **What is CRUD?**
   - Create, Read, Update, Delete - the four basic operations for persistent storage.

8. **What is async/await in Python?**
   - Keywords for asynchronous programming, allowing non-blocking I/O operations.

9. **What is MongoDB and why use it?**
   - MongoDB is a NoSQL document database that stores data in JSON-like documents.

10. **What is middleware in FastAPI?**
    - Software that processes requests/responses between client and server (e.g., CORS middleware).

---

## Multiple Choice Questions (MCQs)

### Q1. Which HTTP method is used to create a new resource?
a) GET  
b) POST ✓  
c) PUT  
d) DELETE

### Q2. What status code indicates a resource was successfully created?
a) 200  
b) 201 ✓  
c) 204  
d) 400

### Q3. Which status code means "Not Found"?
a) 400  
b) 401  
c) 403  
d) 404 ✓

### Q4. In FastAPI, which decorator is used to create a GET endpoint?
a) @app.get() ✓  
b) @app.fetch()  
c) @app.retrieve()  
d) @app.read()

### Q5. What does CRUD stand for?
a) Create, Remove, Update, Delete  
b) Create, Read, Update, Delete ✓  
c) Copy, Read, Update, Delete  
d) Create, Read, Upload, Delete

### Q6. Which library is used for data validation in FastAPI?
a) Django  
b) Flask  
c) Pydantic ✓  
d) SQLAlchemy

### Q7. What is the default port for uvicorn?
a) 3000  
b) 5000  
c) 8000 ✓  
d) 8080

### Q8. Which HTTP method is idempotent?
a) POST  
b) GET ✓  
c) Both a and b  
d) Neither

### Q9. What does the Field(...) with "..." mean in Pydantic?
a) Field is optional  
b) Field is required ✓  
c) Field has default value  
d) Field is deprecated

### Q10. What is Swagger UI used for?
a) Database management  
b) API documentation and testing ✓  
c) Code compilation  
d) Server deployment

---

## Assessment Rubric

| Criteria | Excellent (4) | Good (3) | Satisfactory (2) | Needs Improvement (1) |
|----------|---------------|----------|------------------|----------------------|
| **CRUD Implementation** | All 5 endpoints work correctly | 4 endpoints work | 3 endpoints work | Less than 3 work |
| **Data Validation** | All validations implemented | Most validations work | Some validations work | Minimal validation |
| **Code Quality** | Clean, well-commented code | Mostly clean code | Some organization | Disorganized code |
| **Error Handling** | Proper HTTP status codes | Most status codes correct | Some error handling | No error handling |
| **Testing** | Tested all endpoints | Tested most endpoints | Tested few endpoints | No testing done |
| **Documentation** | Complete README, comments | Good documentation | Basic documentation | No documentation |

**Total Points: 24**

**Grading Scale:**
- 22-24: A (Excellent)
- 18-21: B (Good)
- 14-17: C (Satisfactory)
- 10-13: D (Needs Improvement)
- Below 10: F (Fail)

---

## Common Mistakes to Avoid

1. **Forgetting to activate virtual environment**
   ```bash
   source venv/bin/activate  # Always do this first!
   ```

2. **Not starting MongoDB**
   - Error: "Connection refused"
   - Solution: Start MongoDB service

3. **Missing required fields in request body**
   - Error: 422 Unprocessable Entity
   - Solution: Check Pydantic schema for required fields

4. **Wrong Content-Type header**
   - Always use: `Content-Type: application/json`

5. **Using wrong HTTP method**
   - POST for create, GET for read, PUT for update, DELETE for delete

6. **Not handling 404 errors**
   - Always check if resource exists before operations

---

## Troubleshooting

### Server won't start
```bash
# Check if port is in use
lsof -i :8001
# Kill process if needed
kill -9 <PID>
```

### MongoDB connection error
```bash
# Check if MongoDB is running
sudo systemctl status mongod
# Start MongoDB
sudo systemctl start mongod
```

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

---

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

---

## License

This lab material is created for educational purposes.

---

**Happy Learning!** 🚀
