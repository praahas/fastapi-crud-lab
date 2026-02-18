# FastAPI CRUD Lab - Student Worksheet

## Lab Information

| Field | Value |
|-------|-------|
| **Lab Title** | Building REST APIs with FastAPI |
| **Duration** | 4 Hours |
| **Prerequisites** | Basic Python knowledge |
| **Student Name** | _________________________ |
| **Date** | _________________________ |

---

# Hour 1: Environment Setup & Hello API

## Learning Objectives
- Set up Python development environment
- Install required packages
- Create your first FastAPI application
- Run the development server

## Theory: What is REST API?

**REST** (Representational State Transfer) is an architectural style for designing web services:

- **Stateless**: Each request contains all information needed
- **Client-Server**: Separation of concerns
- **Uniform Interface**: Standard HTTP methods
- **Resource-Based**: Everything is a resource with a URL

**HTTP Methods:**
| Method | Operation | Example |
|--------|-----------|---------|
| GET | Read | Get all items |
| POST | Create | Create new item |
| PUT | Update | Update existing item |
| DELETE | Delete | Remove item |

---

## Step 1.1: Project Structure

Create the following folder structure:

```
crud_lab/
├── server.py        # Main application
├── requirements.txt # Dependencies
├── .env            # Environment variables
└── README.md       # Documentation
```

**Understanding each file:**
- `server.py` - Main FastAPI application code
- `requirements.txt` - List of Python packages
- `.env` - Configuration variables (database URL, etc.)

---

## Step 1.2: Install Dependencies

Open your terminal and run:

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate      # Windows

# Install packages
pip install fastapi uvicorn motor pydantic python-dotenv
```

**What each package does:**
- `fastapi` - Web framework for building APIs
- `uvicorn` - ASGI server to run our app
- `motor` - Async MongoDB driver
- `pydantic` - Data validation
- `python-dotenv` - Load environment variables

---

## Step 1.3: Create Your First Endpoint

Create `server.py` with a simple hello world:

```python
from fastapi import FastAPI

# Create FastAPI application
app = FastAPI(
    title="My First API",
    description="Learning REST APIs",
    version="1.0.0"
)

# Root endpoint
@app.get("/api/")
async def hello():
    return {"message": "Hello, World!"}

# Health check endpoint
@app.get("/api/health")
async def health():
    return {"status": "healthy"}
```

**Code Explanation:**
1. `FastAPI()` - Creates the application instance
2. `@app.get("/api/")` - Decorator that creates a GET endpoint
3. `async def` - Defines an asynchronous function
4. `return {...}` - Returns JSON response

---

## Step 1.4: Run the Server

```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

**Command breakdown:**
- `server:app` - File name : FastAPI instance
- `--reload` - Auto-restart on code changes
- `--host 0.0.0.0` - Accept connections from any IP
- `--port 8001` - Port number

---

## Step 1.5: Test Your API

Open your browser and visit:
- **Swagger UI**: http://localhost:8001/api/docs
- **ReDoc**: http://localhost:8001/api/redoc

Or use curl:
```bash
curl http://localhost:8001/api/
curl http://localhost:8001/api/health
```

---

## Hour 1 Checkpoint

### What should work:
- [ ] Server starts without errors
- [ ] Swagger UI loads at `/api/docs`
- [ ] GET `/api/` returns hello message
- [ ] GET `/api/health` returns status

### Verification Steps:
1. Check terminal for "Uvicorn running on..." message
2. Open browser to http://localhost:8001/api/docs
3. Click "Try it out" on each endpoint

### Checkpoint Questions:

**Q1:** What HTTP method did we use for our endpoints?
```
Answer: ___________________________________
```

**Q2:** What does the `@app.get()` decorator do?
```
Answer: ___________________________________
```

**Q3:** Why do we use `async def` instead of just `def`?
```
Answer: ___________________________________
```

---

# Hour 2: Database, Models & Schemas

## Learning Objectives
- Connect to MongoDB database
- Create Pydantic models for data validation
- Understand request vs response schemas
- Add field validation rules

## Theory: Pydantic Models

Pydantic models define the structure of your data:

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str                    # Required string
    price: float = Field(gt=0)   # Must be > 0
    quantity: int = Field(ge=0)  # Must be >= 0
```

**Validation Rules:**
- `gt=0` - Greater than 0
- `ge=0` - Greater than or equal to 0
- `le=100` - Less than or equal to 100
- `min_length=1` - Minimum string length
- `max_length=100` - Maximum string length

---

## Step 2.1: Create Environment File

Create `.env`:

```
MONGO_URL="mongodb://localhost:27017"
DB_NAME="crud_lab_db"
CORS_ORIGINS="*"
```

**Why use .env?**
- Keep sensitive data out of code
- Easy to change between environments
- Security best practice

---

## Step 2.2: Connect to MongoDB

Add database connection to `server.py`:

```python
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Connect to MongoDB
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]
```

**Code Explanation:**
1. `load_dotenv()` - Loads variables from .env file
2. `os.environ['MONGO_URL']` - Gets the database URL
3. `AsyncIOMotorClient` - Creates async database connection
4. `db = client[DB_NAME]` - Selects the database

---

## Step 2.3: Create Item Schemas

Define your data models:

```python
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime, timezone
import uuid

# Schema for creating items (input)
class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)
    category: Optional[str] = Field(None, max_length=50)

# Schema for complete item (output)
class Item(ItemCreate):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
```

**Schema Types:**
1. `ItemCreate` - Used for POST requests (no ID)
2. `Item` - Full item with auto-generated fields

---

## Step 2.4: Understand Schema Inheritance

```
ItemBase (common fields)
    │
    ├── ItemCreate (for creating - no ID)
    │
    └── Item (full model with ID and timestamps)
```

**Why separate schemas?**
- `ItemCreate` - User provides these fields
- `Item` - Database adds ID and timestamps

---

## Hour 2 Checkpoint

### What should work:
- [ ] Database connection established
- [ ] ItemCreate schema defined
- [ ] Item schema with auto-generated fields
- [ ] Validation rules working

### Verification Steps:
1. Check no database connection errors in terminal
2. Try creating Item with invalid data in Python REPL

### Checkpoint Questions:

**Q1:** What does `Field(gt=0)` mean?
```
Answer: ___________________________________
```

**Q2:** Why do we use `Optional[str]` for description?
```
Answer: ___________________________________
```

**Q3:** What is the difference between ItemCreate and Item schemas?
```
Answer: ___________________________________
```

---

# Hour 3: CRUD Operations

## Learning Objectives
- Implement Create operation (POST)
- Implement Read operations (GET)
- Implement Update operation (PUT)
- Implement Delete operation (DELETE)
- Handle errors properly

## Theory: CRUD Operations

| Operation | HTTP Method | SQL Equivalent | MongoDB Method |
|-----------|-------------|----------------|----------------|
| Create | POST | INSERT | insert_one() |
| Read | GET | SELECT | find(), find_one() |
| Update | PUT | UPDATE | update_one() |
| Delete | DELETE | DELETE | delete_one() |

---

## Step 3.1: Create Item (POST)

```python
@app.post("/api/items", response_model=Item, status_code=201)
async def create_item(item: ItemCreate):
    # Create item with auto-generated fields
    item_obj = Item(**item.model_dump())
    
    # Prepare for database
    doc = item_obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc['updated_at'] = doc['updated_at'].isoformat()
    
    # Insert into database
    await db.items.insert_one(doc)
    
    return item_obj
```

**Code Explanation:**
1. `response_model=Item` - Validates response shape
2. `status_code=201` - Returns "Created" status
3. `item.model_dump()` - Converts Pydantic to dict
4. `await db.items.insert_one()` - Async database insert

---

## Step 3.2: List All Items (GET)

```python
@app.get("/api/items", response_model=List[Item])
async def get_items(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    skip = (page - 1) * page_size
    
    cursor = db.items.find({}, {"_id": 0}).skip(skip).limit(page_size)
    items = await cursor.to_list(length=page_size)
    
    return items
```

**Pagination Explained:**
- `page=1, page_size=10` → Skip 0, return items 1-10
- `page=2, page_size=10` → Skip 10, return items 11-20
- Formula: `skip = (page - 1) * page_size`

---

## Step 3.3: Get Single Item (GET by ID)

```python
from fastapi import HTTPException

@app.get("/api/items/{item_id}", response_model=Item)
async def get_item(item_id: str):
    item = await db.items.find_one({"id": item_id}, {"_id": 0})
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return item
```

**Error Handling:**
- `HTTPException` - Raises HTTP error response
- `status_code=404` - "Not Found" error
- `detail` - Error message to return

---

## Step 3.4: Update Item (PUT)

```python
@app.put("/api/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item_update: ItemUpdate):
    # Check if exists
    existing = await db.items.find_one({"id": item_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Update only provided fields
    update_data = {k: v for k, v in item_update.model_dump().items() if v is not None}
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    await db.items.update_one({"id": item_id}, {"$set": update_data})
    
    # Return updated item
    updated = await db.items.find_one({"id": item_id}, {"_id": 0})
    return updated
```

**Partial Update:**
- Only update fields that are provided
- `{k: v for k, v in ... if v is not None}` filters None values

---

## Step 3.5: Delete Item (DELETE)

```python
@app.delete("/api/items/{item_id}")
async def delete_item(item_id: str):
    result = await db.items.delete_one({"id": item_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return {"message": "Item deleted successfully"}
```

---

## Hour 3 Checkpoint

### What should work:
- [ ] POST /api/items creates new item
- [ ] GET /api/items returns paginated list
- [ ] GET /api/items/{id} returns single item
- [ ] PUT /api/items/{id} updates item
- [ ] DELETE /api/items/{id} removes item

### Verification Steps:
1. Create 3 items using POST
2. List all items using GET
3. Update one item's price
4. Delete one item
5. Verify deletion with GET

### Checkpoint Questions:

**Q1:** What status code should POST return on success?
```
Answer: ___________________________________
```

**Q2:** How do you handle "item not found" errors?
```
Answer: ___________________________________
```

**Q3:** What is the purpose of `{"_id": 0}` in MongoDB queries?
```
Answer: ___________________________________
```

---

# Hour 4: Testing, Validation & Mini-Assignment

## Learning Objectives
- Test all endpoints using Swagger UI
- Test using curl commands
- Understand validation errors
- Complete mini-assignment

## Step 4.1: Testing with Swagger UI

1. Open http://localhost:8001/api/docs
2. For each endpoint:
   - Click "Try it out"
   - Fill in required fields
   - Click "Execute"
   - Check response

**Testing Checklist:**

| Endpoint | Test Case | Expected Result | Pass? |
|----------|-----------|-----------------|-------|
| POST /api/items | Valid item | 201 Created | [ ] |
| POST /api/items | Negative price | 422 Error | [ ] |
| POST /api/items | Empty name | 422 Error | [ ] |
| GET /api/items | No params | List of items | [ ] |
| GET /api/items | With pagination | Correct page | [ ] |
| GET /api/items/{id} | Valid ID | Item returned | [ ] |
| GET /api/items/{id} | Invalid ID | 404 Error | [ ] |
| PUT /api/items/{id} | Valid update | 200 OK | [ ] |
| DELETE /api/items/{id} | Valid ID | 200 OK | [ ] |

---

## Step 4.2: Testing with curl

**Create Item:**
```bash
curl -X POST "http://localhost:8001/api/items" \
     -H "Content-Type: application/json" \
     -d '{"name": "Test Item", "price": 19.99, "quantity": 5}'
```

**List Items:**
```bash
curl "http://localhost:8001/api/items"
```

**Search Items:**
```bash
curl "http://localhost:8001/api/items?search=Test"
```

**Get Single Item:**
```bash
curl "http://localhost:8001/api/items/{PASTE_ID_HERE}"
```

**Update Item:**
```bash
curl -X PUT "http://localhost:8001/api/items/{PASTE_ID_HERE}" \
     -H "Content-Type: application/json" \
     -d '{"price": 24.99}'
```

**Delete Item:**
```bash
curl -X DELETE "http://localhost:8001/api/items/{PASTE_ID_HERE}"
```

---

## Step 4.3: Understanding Validation Errors

When validation fails, you get a 422 response:

```json
{
    "detail": [
        {
            "loc": ["body", "price"],
            "msg": "Input should be greater than 0",
            "type": "greater_than"
        }
    ]
}
```

**Error Fields:**
- `loc` - Location of the error (body → price)
- `msg` - Human-readable message
- `type` - Error type for programmatic handling

---

## Mini-Assignment Tasks

### Task 1: Add More Test Data

Create at least 10 items across different categories:

| Name | Category | Price | Quantity |
|------|----------|-------|----------|
| Laptop | Electronics | 999.99 | 5 |
| Mouse | Electronics | 29.99 | 50 |
| Keyboard | Electronics | 79.99 | 30 |
| Python Book | Books | 49.99 | 20 |
| JavaScript Book | Books | 44.99 | 15 |
| T-Shirt | Clothing | 19.99 | 100 |
| Jeans | Clothing | 59.99 | 40 |
| Coffee Mug | Home | 12.99 | 200 |
| Desk Lamp | Home | 34.99 | 25 |
| Backpack | Accessories | 69.99 | 35 |

### Task 2: Test Search Functionality

Search for items and record results:

| Search Term | Expected Results | Actual Count |
|-------------|------------------|--------------|
| "laptop" | 1 | ___ |
| "book" | 2 | ___ |
| "a" | Multiple | ___ |

### Task 3: Test Pagination

With 10 items, page_size=3:

| Page | Expected Items | Verified? |
|------|----------------|-----------|
| 1 | Items 1-3 | [ ] |
| 2 | Items 4-6 | [ ] |
| 3 | Items 7-9 | [ ] |
| 4 | Item 10 | [ ] |

### Task 4: Test Category Filter

| Category | Expected Count | Verified? |
|----------|----------------|-----------|
| Electronics | 3 | [ ] |
| Books | 2 | [ ] |
| Clothing | 2 | [ ] |

---

## Hour 4 Checkpoint

### What should work:
- [ ] All CRUD operations tested
- [ ] Validation errors handled correctly
- [ ] Search functionality working
- [ ] Pagination working
- [ ] Category filter working

### Final Verification:
1. All endpoints return correct status codes
2. Invalid data returns 422 errors
3. Non-existent items return 404
4. Search and pagination work together

### Checkpoint Questions:

**Q1:** What does status code 422 indicate?
```
Answer: ___________________________________
```

**Q2:** How do you combine search with pagination in the URL?
```
Answer: ___________________________________
```

**Q3:** What happens if you try to delete an item that doesn't exist?
```
Answer: ___________________________________
```

---

## Lab Completion Checklist

### Core Requirements:
- [ ] Server runs without errors
- [ ] All 5 CRUD endpoints implemented
- [ ] Swagger documentation accessible
- [ ] Data validation working
- [ ] Error handling implemented

### Bonus Features:
- [ ] Search by name implemented
- [ ] Pagination implemented
- [ ] Category filter implemented
- [ ] Statistics endpoint working

### Documentation:
- [ ] README.md complete
- [ ] Code comments added
- [ ] All curl examples tested

---

## Reflection Questions

Write brief answers:

**1. What was the most challenging part of this lab?**
```
_______________________________________________
_______________________________________________
```

**2. What concept do you understand better now?**
```
_______________________________________________
_______________________________________________
```

**3. How would you extend this API for a real project?**
```
_______________________________________________
_______________________________________________
```

---

## Submission

Submit the following:
1. All source code files
2. Screenshot of Swagger UI
3. Screenshot of successful API tests
4. This completed worksheet

---

**Congratulations on completing the FastAPI CRUD Lab!** 🎉

You have learned:
- REST API fundamentals
- FastAPI framework basics
- Database operations with MongoDB
- Data validation with Pydantic
- API testing techniques

**Next Steps:**
- Add authentication (JWT tokens)
- Deploy to cloud (Heroku, AWS, etc.)
- Add frontend (React, Vue, etc.)
- Learn about testing frameworks (pytest)
