"""
================================================================================
                    FASTAPI CRUD LAB - MAIN APPLICATION
================================================================================
This is the main entry point for our REST API application.
Students will learn how all components work together here.

LEARNING OBJECTIVES:
- Understand FastAPI application structure
- Learn about routers and middleware
- Connect to MongoDB database
- Configure CORS for API access
================================================================================
"""

from fastapi import FastAPI, APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, validator
from typing import List, Optional
import uuid
from datetime import datetime, timezone

# ============================================================================
# CONFIGURATION SETUP
# ============================================================================
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection - Using environment variables (BEST PRACTICE!)
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# ============================================================================
# FASTAPI APPLICATION SETUP
# ============================================================================
app = FastAPI(
    title="FastAPI CRUD Lab - Item Management API",
    description="""
## Welcome to the FastAPI CRUD Lab! 🚀

This is a **teaching-oriented REST API** designed for undergraduate students 
to learn backend development concepts.

### What You'll Learn:
- **REST API Concepts**: HTTP methods, endpoints, status codes
- **CRUD Operations**: Create, Read, Update, Delete
- **Data Validation**: Using Pydantic schemas
- **Database Operations**: MongoDB with Motor async driver

### Lab Duration: 4 Hours
- Hour 1: Environment Setup & Hello API
- Hour 2: Database, Models & Schemas  
- Hour 3: CRUD Operations
- Hour 4: Testing, Validation & Mini-Assignment

### Quick Start:
1. Use the interactive docs below to test endpoints
2. Try creating an item with POST /api/items
3. Retrieve all items with GET /api/items

**Happy Learning!** 📚
    """,
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Create API router with prefix
api_router = APIRouter(prefix="/api")

# ============================================================================
# PYDANTIC MODELS (SCHEMAS)
# ============================================================================
# These define the structure and validation rules for our data

class ItemBase(BaseModel):
    """
    Base Item Schema - Contains common fields
    
    TEACHING NOTE:
    - BaseModel from Pydantic provides automatic validation
    - Field() allows us to add constraints and descriptions
    - Optional[] means the field can be None
    """
    name: str = Field(
        ...,  # ... means required
        min_length=1,
        max_length=100,
        description="Name of the item (required, 1-100 characters)",
        json_schema_extra={"example": "Laptop"}
    )
    description: Optional[str] = Field(
        None,  # None means optional with default None
        max_length=500,
        description="Description of the item (optional, max 500 characters)",
        json_schema_extra={"example": "High-performance laptop for coding"}
    )
    price: float = Field(
        ...,
        gt=0,  # Greater than 0
        description="Price of the item (must be greater than 0)",
        json_schema_extra={"example": 999.99}
    )
    quantity: int = Field(
        ...,
        ge=0,  # Greater than or equal to 0
        description="Quantity in stock (must be >= 0)",
        json_schema_extra={"example": 10}
    )
    category: Optional[str] = Field(
        None,
        max_length=50,
        description="Category of the item (optional)",
        json_schema_extra={"example": "Electronics"}
    )


class ItemCreate(ItemBase):
    """
    Schema for creating a new item
    
    TEACHING NOTE:
    - Inherits all fields from ItemBase
    - Used for POST requests
    - No ID field - database will generate it
    """
    pass


class ItemUpdate(BaseModel):
    """
    Schema for updating an existing item
    
    TEACHING NOTE:
    - All fields are Optional for partial updates
    - Only provided fields will be updated
    - This is called a "PATCH-style" update
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)
    category: Optional[str] = Field(None, max_length=50)


class Item(ItemBase):
    """
    Complete Item Schema - Includes database-generated fields
    
    TEACHING NOTE:
    - This is the response model
    - Includes 'id' which is auto-generated
    - Includes timestamps for auditing
    """
    model_config = ConfigDict(extra="ignore")  # Ignore MongoDB's _id field
    
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier (auto-generated UUID)"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when item was created"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when item was last updated"
    )


class PaginatedItems(BaseModel):
    """
    Schema for paginated response
    
    TEACHING NOTE:
    - Pagination prevents loading too much data at once
    - 'total' tells us how many items exist
    - 'items' contains the actual data
    """
    items: List[Item]
    total: int
    page: int
    page_size: int
    total_pages: int


class MessageResponse(BaseModel):
    """Simple message response schema"""
    message: str
    detail: Optional[str] = None


# ============================================================================
# HELPER FUNCTIONS (CRUD OPERATIONS)
# ============================================================================

async def serialize_item(item_dict: dict) -> dict:
    """
    Convert MongoDB document to API response format
    
    TEACHING NOTE:
    - MongoDB stores datetime as strings, we need to convert them
    - We exclude MongoDB's _id field from responses
    """
    if isinstance(item_dict.get('created_at'), str):
        item_dict['created_at'] = datetime.fromisoformat(item_dict['created_at'])
    if isinstance(item_dict.get('updated_at'), str):
        item_dict['updated_at'] = datetime.fromisoformat(item_dict['updated_at'])
    return item_dict


# ============================================================================
# API ENDPOINTS
# ============================================================================

# -----------------------------------------------------------------------------
# ROOT ENDPOINT
# -----------------------------------------------------------------------------
@api_router.get("/", response_model=MessageResponse, tags=["General"])
async def root():
    """
    Root endpoint - Returns welcome message
    
    **HTTP Method:** GET
    **Purpose:** Health check and welcome message
    
    This is typically the first endpoint you create to verify
    your API is running correctly.
    """
    return {
        "message": "Welcome to FastAPI CRUD Lab!",
        "detail": "Visit /api/docs for interactive documentation"
    }


@api_router.get("/health", response_model=MessageResponse, tags=["General"])
async def health_check():
    """
    Health check endpoint
    
    **HTTP Method:** GET
    **Purpose:** Verify API and database connectivity
    
    This endpoint is useful for:
    - Load balancers to check if service is healthy
    - Monitoring systems
    - Debugging connectivity issues
    """
    try:
        # Test database connection
        await db.command('ping')
        return {
            "message": "API is healthy!",
            "detail": "Database connection: OK"
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Database connection failed: {str(e)}"
        )


# -----------------------------------------------------------------------------
# CREATE ITEM (POST)
# -----------------------------------------------------------------------------
@api_router.post(
    "/items",
    response_model=Item,
    status_code=201,
    tags=["Items"],
    summary="Create a new item",
    response_description="The created item with generated ID"
)
async def create_item(item: ItemCreate):
    """
    Create a new item in the database
    
    **HTTP Method:** POST  
    **Status Code:** 201 Created (on success)
    
    ## Request Body:
    - **name** (required): Item name (1-100 characters)
    - **description** (optional): Item description (max 500 characters)
    - **price** (required): Item price (must be > 0)
    - **quantity** (required): Stock quantity (must be >= 0)
    - **category** (optional): Item category (max 50 characters)
    
    ## Example:
    ```json
    {
        "name": "Laptop",
        "description": "High-performance laptop",
        "price": 999.99,
        "quantity": 10,
        "category": "Electronics"
    }
    ```
    
    ## Teaching Notes:
    1. POST is used for creating new resources
    2. Request body contains the data to create
    3. Response includes auto-generated ID and timestamps
    4. Status 201 indicates successful creation
    """
    # Create Item object with auto-generated fields
    item_obj = Item(**item.model_dump())
    
    # Prepare document for MongoDB
    doc = item_obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc['updated_at'] = doc['updated_at'].isoformat()
    
    # Insert into database
    await db.items.insert_one(doc)
    
    logger.info(f"Created item: {item_obj.id} - {item_obj.name}")
    return item_obj


# -----------------------------------------------------------------------------
# READ ALL ITEMS (GET with Pagination & Search)
# -----------------------------------------------------------------------------
@api_router.get(
    "/items",
    response_model=PaginatedItems,
    tags=["Items"],
    summary="List all items with pagination and search"
)
async def get_items(
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page (1-100)"),
    search: Optional[str] = Query(None, description="Search by item name"),
    category: Optional[str] = Query(None, description="Filter by category")
):
    """
    Retrieve all items with pagination and optional filtering
    
    **HTTP Method:** GET  
    **Status Code:** 200 OK
    
    ## Query Parameters:
    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 10, max: 100)
    - **search**: Search items by name (case-insensitive)
    - **category**: Filter by category
    
    ## Example Requests:
    - `GET /api/items` - Get first 10 items
    - `GET /api/items?page=2&page_size=5` - Get 5 items from page 2
    - `GET /api/items?search=laptop` - Search for "laptop"
    - `GET /api/items?category=Electronics` - Filter by category
    
    ## Teaching Notes:
    1. GET is used for retrieving data
    2. Query parameters allow filtering without changing endpoint
    3. Pagination prevents loading too much data at once
    4. Always return structured response with metadata
    """
    # Build query filter
    query_filter = {}
    
    if search:
        # Case-insensitive search using regex
        query_filter["name"] = {"$regex": search, "$options": "i"}
    
    if category:
        query_filter["category"] = {"$regex": f"^{category}$", "$options": "i"}
    
    # Get total count for pagination
    total = await db.items.count_documents(query_filter)
    
    # Calculate pagination
    skip = (page - 1) * page_size
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    
    # Fetch items with pagination
    cursor = db.items.find(query_filter, {"_id": 0}).skip(skip).limit(page_size)
    items_list = await cursor.to_list(length=page_size)
    
    # Serialize items
    serialized_items = [await serialize_item(item) for item in items_list]
    
    return PaginatedItems(
        items=serialized_items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


# -----------------------------------------------------------------------------
# READ SINGLE ITEM (GET by ID)
# -----------------------------------------------------------------------------
@api_router.get(
    "/items/{item_id}",
    response_model=Item,
    tags=["Items"],
    summary="Retrieve a single item by ID"
)
async def get_item(item_id: str):
    """
    Retrieve a specific item by its ID
    
    **HTTP Method:** GET  
    **Status Code:** 200 OK (found) / 404 Not Found
    
    ## Path Parameters:
    - **item_id**: The unique identifier of the item
    
    ## Example:
    `GET /api/items/550e8400-e29b-41d4-a716-446655440000`
    
    ## Teaching Notes:
    1. Path parameters are part of the URL
    2. Use for retrieving specific resources
    3. Return 404 if resource doesn't exist
    4. Always validate the ID format
    """
    # Find item in database
    item = await db.items.find_one({"id": item_id}, {"_id": 0})
    
    if not item:
        raise HTTPException(
            status_code=404,
            detail=f"Item with ID '{item_id}' not found"
        )
    
    return await serialize_item(item)


# -----------------------------------------------------------------------------
# UPDATE ITEM (PUT)
# -----------------------------------------------------------------------------
@api_router.put(
    "/items/{item_id}",
    response_model=Item,
    tags=["Items"],
    summary="Update an existing item"
)
async def update_item(item_id: str, item_update: ItemUpdate):
    """
    Update an existing item (partial update supported)
    
    **HTTP Method:** PUT  
    **Status Code:** 200 OK (success) / 404 Not Found
    
    ## Path Parameters:
    - **item_id**: The unique identifier of the item to update
    
    ## Request Body:
    Only include fields you want to update:
    ```json
    {
        "price": 899.99,
        "quantity": 15
    }
    ```
    
    ## Teaching Notes:
    1. PUT/PATCH is used for updating existing resources
    2. Only provided fields are updated (partial update)
    3. updated_at timestamp is automatically refreshed
    4. Return 404 if item doesn't exist
    """
    # Check if item exists
    existing_item = await db.items.find_one({"id": item_id}, {"_id": 0})
    
    if not existing_item:
        raise HTTPException(
            status_code=404,
            detail=f"Item with ID '{item_id}' not found"
        )
    
    # Prepare update data (only non-None fields)
    update_data = {k: v for k, v in item_update.model_dump().items() if v is not None}
    
    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No valid fields provided for update"
        )
    
    # Add updated timestamp
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    # Update in database
    await db.items.update_one(
        {"id": item_id},
        {"$set": update_data}
    )
    
    # Fetch and return updated item
    updated_item = await db.items.find_one({"id": item_id}, {"_id": 0})
    logger.info(f"Updated item: {item_id}")
    
    return await serialize_item(updated_item)


# -----------------------------------------------------------------------------
# DELETE ITEM (DELETE)
# -----------------------------------------------------------------------------
@api_router.delete(
    "/items/{item_id}",
    response_model=MessageResponse,
    tags=["Items"],
    summary="Delete an item"
)
async def delete_item(item_id: str):
    """
    Delete an item from the database
    
    **HTTP Method:** DELETE  
    **Status Code:** 200 OK (success) / 404 Not Found
    
    ## Path Parameters:
    - **item_id**: The unique identifier of the item to delete
    
    ## Example:
    `DELETE /api/items/550e8400-e29b-41d4-a716-446655440000`
    
    ## Teaching Notes:
    1. DELETE removes resources permanently
    2. Return confirmation message on success
    3. Return 404 if item doesn't exist
    4. Consider soft-delete for production (mark as deleted instead)
    """
    # Check if item exists
    existing_item = await db.items.find_one({"id": item_id}, {"_id": 0})
    
    if not existing_item:
        raise HTTPException(
            status_code=404,
            detail=f"Item with ID '{item_id}' not found"
        )
    
    # Delete from database
    result = await db.items.delete_one({"id": item_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=500,
            detail="Failed to delete item"
        )
    
    logger.info(f"Deleted item: {item_id}")
    
    return {
        "message": "Item deleted successfully",
        "detail": f"Item ID: {item_id}"
    }


# -----------------------------------------------------------------------------
# STATISTICS ENDPOINT (Bonus)
# -----------------------------------------------------------------------------
@api_router.get(
    "/items/stats/summary",
    tags=["Items"],
    summary="Get inventory statistics"
)
async def get_item_statistics():
    """
    Get summary statistics for all items
    
    **HTTP Method:** GET  
    **Purpose:** Demonstrates aggregation queries
    
    ## Teaching Notes:
    1. Aggregation pipelines perform complex calculations
    2. Useful for dashboards and reporting
    3. MongoDB's aggregation framework is very powerful
    """
    # Get total items count
    total_items = await db.items.count_documents({})
    
    if total_items == 0:
        return {
            "total_items": 0,
            "total_quantity": 0,
            "total_value": 0,
            "average_price": 0,
            "categories": []
        }
    
    # Aggregation for statistics
    pipeline = [
        {
            "$group": {
                "_id": None,
                "total_quantity": {"$sum": "$quantity"},
                "total_value": {"$sum": {"$multiply": ["$price", "$quantity"]}},
                "average_price": {"$avg": "$price"},
                "min_price": {"$min": "$price"},
                "max_price": {"$max": "$price"}
            }
        }
    ]
    
    stats_cursor = db.items.aggregate(pipeline)
    stats_list = await stats_cursor.to_list(length=1)
    stats = stats_list[0] if stats_list else {}
    
    # Get unique categories
    categories = await db.items.distinct("category")
    categories = [c for c in categories if c]  # Remove None values
    
    return {
        "total_items": total_items,
        "total_quantity": stats.get("total_quantity", 0),
        "total_value": round(stats.get("total_value", 0), 2),
        "average_price": round(stats.get("average_price", 0), 2),
        "min_price": stats.get("min_price", 0),
        "max_price": stats.get("max_price", 0),
        "categories": categories
    }


# ============================================================================
# MIDDLEWARE & APP CONFIGURATION
# ============================================================================

# Include the API router
app.include_router(api_router)

# CORS Middleware - Allows cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# STARTUP & SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """
    Runs when the application starts
    - Create database indexes for better performance
    """
    logger.info("FastAPI CRUD Lab starting up...")
    # Create index on 'name' field for faster searches
    await db.items.create_index("name")
    await db.items.create_index("category")
    logger.info("Database indexes created")


@app.on_event("shutdown")
async def shutdown_db_client():
    """
    Runs when the application shuts down
    - Close database connection properly
    """
    logger.info("Shutting down FastAPI CRUD Lab...")
    client.close()


# ============================================================================
# HTML LANDING PAGE (Bonus for students)
# ============================================================================

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def landing_page():
    """Serve a simple landing page directing to docs"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FastAPI CRUD Lab</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', system-ui, sans-serif;
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #e0e0e0;
            }
            .container {
                max-width: 800px;
                padding: 3rem;
                text-align: center;
            }
            h1 {
                font-size: 3rem;
                margin-bottom: 1rem;
                background: linear-gradient(90deg, #00d4ff, #7c3aed);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            .subtitle {
                font-size: 1.2rem;
                color: #94a3b8;
                margin-bottom: 2rem;
            }
            .card {
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 16px;
                padding: 2rem;
                margin: 1.5rem 0;
                backdrop-filter: blur(10px);
            }
            .links {
                display: flex;
                gap: 1rem;
                justify-content: center;
                flex-wrap: wrap;
                margin-top: 2rem;
            }
            a {
                display: inline-block;
                padding: 1rem 2rem;
                background: linear-gradient(135deg, #7c3aed, #00d4ff);
                color: white;
                text-decoration: none;
                border-radius: 12px;
                font-weight: 600;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            a:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(124, 58, 237, 0.3);
            }
            .secondary {
                background: rgba(255,255,255,0.1);
                border: 1px solid rgba(255,255,255,0.2);
            }
            .hours {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 1rem;
                margin-top: 1.5rem;
            }
            .hour {
                background: rgba(124, 58, 237, 0.1);
                border: 1px solid rgba(124, 58, 237, 0.3);
                border-radius: 8px;
                padding: 1rem;
            }
            .hour h4 { color: #7c3aed; margin-bottom: 0.5rem; }
            code {
                background: rgba(0,0,0,0.3);
                padding: 0.2rem 0.5rem;
                border-radius: 4px;
                font-family: 'Fira Code', monospace;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>FastAPI CRUD Lab</h1>
            <p class="subtitle">A Teaching-Oriented REST API for Learning Backend Development</p>
            
            <div class="card">
                <h3>Lab Duration: 4 Hours</h3>
                <div class="hours">
                    <div class="hour">
                        <h4>Hour 1</h4>
                        <p>Environment Setup & Hello API</p>
                    </div>
                    <div class="hour">
                        <h4>Hour 2</h4>
                        <p>Database, Models & Schemas</p>
                    </div>
                    <div class="hour">
                        <h4>Hour 3</h4>
                        <p>CRUD Operations</p>
                    </div>
                    <div class="hour">
                        <h4>Hour 4</h4>
                        <p>Testing & Mini-Assignment</p>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h3>Quick Start</h3>
                <p>Test the API using interactive documentation</p>
                <div class="links">
                    <a href="/api/docs">Swagger UI</a>
                    <a href="/api/redoc" class="secondary">ReDoc</a>
                </div>
            </div>
            
            <div class="card">
                <h3>API Endpoints</h3>
                <p style="text-align: left; margin-top: 1rem;">
                    <code>POST /api/items</code> - Create item<br><br>
                    <code>GET /api/items</code> - List items (with pagination)<br><br>
                    <code>GET /api/items/{id}</code> - Get single item<br><br>
                    <code>PUT /api/items/{id}</code> - Update item<br><br>
                    <code>DELETE /api/items/{id}</code> - Delete item
                </p>
            </div>
        </div>
    </body>
    </html>
    """
