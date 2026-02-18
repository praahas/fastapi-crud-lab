# FastAPI CRUD Lab - Local Setup Manual

## Complete Guide to Running the Lab on Your Laptop

This manual provides step-by-step instructions to set up and run the FastAPI CRUD Lab on your local machine.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installing Python](#installing-python)
3. [Installing MongoDB](#installing-mongodb)
4. [Project Setup](#project-setup)
5. [Running the Application](#running-the-application)
6. [Testing the API](#testing-the-api)
7. [Troubleshooting](#troubleshooting)
8. [Quick Reference Commands](#quick-reference-commands)

---

## Prerequisites

Before starting, ensure you have:

| Requirement | Minimum Version | Check Command |
|-------------|-----------------|---------------|
| Python | 3.9+ | `python --version` |
| pip | 21.0+ | `pip --version` |
| MongoDB | 4.4+ | `mongod --version` |
| Git (optional) | 2.0+ | `git --version` |

---

## Installing Python

### Windows

1. **Download Python**
   - Go to: https://www.python.org/downloads/
   - Download Python 3.11 or later

2. **Run Installer**
   - ✅ Check "Add Python to PATH" (IMPORTANT!)
   - Click "Install Now"

3. **Verify Installation**
   ```cmd
   python --version
   pip --version
   ```

### macOS

1. **Using Homebrew (Recommended)**
   ```bash
   # Install Homebrew if not installed
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Install Python
   brew install python@3.11
   ```

2. **Verify Installation**
   ```bash
   python3 --version
   pip3 --version
   ```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
```

---

## Installing MongoDB

### Windows

1. **Download MongoDB Community Server**
   - Go to: https://www.mongodb.com/try/download/community
   - Select Windows, MSI package

2. **Run Installer**
   - Choose "Complete" installation
   - ✅ Check "Install MongoDB as a Service"
   - ✅ Check "Install MongoDB Compass" (GUI tool)

3. **Verify Installation**
   ```cmd
   # MongoDB should start automatically as a service
   # Open MongoDB Compass to verify connection
   ```

### macOS

```bash
# Using Homebrew
brew tap mongodb/brew
brew install mongodb-community@7.0

# Start MongoDB
brew services start mongodb-community@7.0

# Verify
mongosh --eval "db.version()"
```

### Linux (Ubuntu/Debian)

```bash
# Import MongoDB GPG key
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor

# Add repository
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
   sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Install
sudo apt update
sudo apt install -y mongodb-org

# Start service
sudo systemctl start mongod
sudo systemctl enable mongod

# Verify
mongosh --eval "db.version()"
```

---

## Project Setup

### Step 1: Create Project Directory

```bash
# Create and enter project folder
mkdir fastapi-crud-lab
cd fastapi-crud-lab
```

### Step 2: Create Virtual Environment

**Why?** Virtual environments isolate project dependencies.

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the beginning of your terminal prompt.

### Step 3: Create Project Files

Create the following file structure:

```
fastapi-crud-lab/
├── server.py          # Main application
├── requirements.txt   # Dependencies
├── .env              # Configuration
└── README.md         # Documentation
```

### Step 4: Create requirements.txt

Create a file named `requirements.txt`:

```txt
fastapi==0.110.1
uvicorn==0.25.0
motor==3.3.1
pydantic==2.6.4
python-dotenv==1.0.1
pymongo==4.5.0
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Create .env File

Create a file named `.env`:

```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=crud_lab_db
CORS_ORIGINS=*
```

### Step 7: Create server.py

Copy the `server.py` file from the project. The file contains:
- FastAPI application setup
- Pydantic models for data validation
- CRUD endpoints for Item management
- MongoDB connection handling

---

## Running the Application

### Step 1: Ensure MongoDB is Running

```bash
# Windows (if not running as service)
mongod

# macOS
brew services start mongodb-community@7.0

# Linux
sudo systemctl start mongod
```

### Step 2: Activate Virtual Environment

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Step 3: Start the Server

```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

**Command Explanation:**
- `server:app` - File name (server.py) : FastAPI instance name (app)
- `--reload` - Auto-restart on code changes (development mode)
- `--host 0.0.0.0` - Accept connections from any IP
- `--port 8001` - Port number

### Step 4: Access the Application

Open your browser and visit:

| URL | Description |
|-----|-------------|
| http://localhost:8001 | Landing page |
| http://localhost:8001/api/docs | Swagger UI (Interactive API docs) |
| http://localhost:8001/api/redoc | ReDoc (Alternative docs) |
| http://localhost:8001/api/health | Health check endpoint |

---

## Testing the API

### Using Swagger UI (Recommended for Beginners)

1. Open http://localhost:8001/api/docs
2. Click on any endpoint to expand it
3. Click "Try it out"
4. Fill in the required fields
5. Click "Execute"
6. View the response

### Using curl (Command Line)

**Health Check:**
```bash
curl http://localhost:8001/api/health
```

**Create Item:**
```bash
curl -X POST "http://localhost:8001/api/items" \
     -H "Content-Type: application/json" \
     -d '{
         "name": "Laptop",
         "description": "High-performance laptop",
         "price": 999.99,
         "quantity": 10,
         "category": "Electronics"
     }'
```

**List All Items:**
```bash
curl http://localhost:8001/api/items
```

**Search Items:**
```bash
curl "http://localhost:8001/api/items?search=laptop"
```

**Get Item by ID:**
```bash
curl http://localhost:8001/api/items/{item_id}
```

**Update Item:**
```bash
curl -X PUT "http://localhost:8001/api/items/{item_id}" \
     -H "Content-Type: application/json" \
     -d '{"price": 899.99}'
```

**Delete Item:**
```bash
curl -X DELETE "http://localhost:8001/api/items/{item_id}"
```

### Using Python (requests library)

```python
import requests

BASE_URL = "http://localhost:8001/api"

# Create item
response = requests.post(f"{BASE_URL}/items", json={
    "name": "Test Item",
    "price": 29.99,
    "quantity": 5
})
print(response.json())

# List items
response = requests.get(f"{BASE_URL}/items")
print(response.json())
```

---

## Troubleshooting

### Problem: "Module not found" Error

**Solution:**
```bash
# Make sure virtual environment is activated
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Problem: MongoDB Connection Error

**Error:** `ServerSelectionTimeoutError: localhost:27017`

**Solution:**
```bash
# Check if MongoDB is running

# Windows - Open Services, find MongoDB, ensure it's "Running"

# macOS
brew services list
brew services start mongodb-community@7.0

# Linux
sudo systemctl status mongod
sudo systemctl start mongod
```

### Problem: Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Find process using port 8001

# Windows
netstat -ano | findstr :8001
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8001
kill -9 <PID>

# Or use a different port
uvicorn server:app --reload --port 8002
```

### Problem: Python/pip Not Found

**Solution:**
```bash
# Windows - Add Python to PATH
# 1. Search "Environment Variables" in Start Menu
# 2. Edit "Path" variable
# 3. Add Python installation path (e.g., C:\Python311\)

# macOS/Linux - Use python3/pip3
python3 --version
pip3 install -r requirements.txt
```

### Problem: Permission Denied (Linux/macOS)

**Solution:**
```bash
# Don't use sudo with pip in virtual environment
# Make sure venv is activated first

source venv/bin/activate
pip install -r requirements.txt
```

### Problem: .env File Not Loading

**Solution:**
```bash
# Ensure .env file is in the same directory as server.py
# Check file name (not .env.txt)
# Verify no extra spaces in .env values

# Debug by printing environment variables
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.environ.get('MONGO_URL'))"
```

---

## Quick Reference Commands

### Daily Workflow

```bash
# 1. Open terminal in project directory
cd fastapi-crud-lab

# 2. Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# 3. Start MongoDB (if not running)
brew services start mongodb-community@7.0  # macOS
sudo systemctl start mongod                 # Linux

# 4. Run server
uvicorn server:app --reload --port 8001

# 5. Open browser
# http://localhost:8001/api/docs
```

### Useful Commands

| Task | Command |
|------|---------|
| Activate venv (macOS/Linux) | `source venv/bin/activate` |
| Activate venv (Windows) | `venv\Scripts\activate` |
| Deactivate venv | `deactivate` |
| Install dependencies | `pip install -r requirements.txt` |
| Start server | `uvicorn server:app --reload --port 8001` |
| Check MongoDB status | `mongosh --eval "db.version()"` |
| Freeze dependencies | `pip freeze > requirements.txt` |

### MongoDB Shell Commands

```bash
# Connect to MongoDB
mongosh

# Show databases
show dbs

# Use database
use crud_lab_db

# Show collections
show collections

# View items
db.items.find().pretty()

# Clear all items
db.items.deleteMany({})

# Exit
exit
```

---

## Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Pydantic Documentation**: https://docs.pydantic.dev/
- **MongoDB Documentation**: https://docs.mongodb.com/
- **Python Virtual Environments**: https://docs.python.org/3/tutorial/venv.html

---

## Support

If you encounter issues not covered in this manual:

1. Check the error message carefully
2. Search the error on Google/Stack Overflow
3. Review FastAPI and MongoDB documentation
4. Ask your instructor for help

---

**Happy Coding!** 🚀
