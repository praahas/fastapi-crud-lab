# FastAPI CRUD Lab - Product Requirements Document

## Original Problem Statement
Design and generate a step-by-step, teaching-oriented backend REST API project using Python, suitable for a 4-hour hands-on laboratory session for undergraduate students.

## User Choices
- **Frontend**: Backend only with Swagger UI documentation
- **Documentation**: Both markdown files and integrated docs
- **Database**: MongoDB (adapted from SQLite)

## Architecture
- **Backend**: FastAPI with Motor (async MongoDB driver)
- **Database**: MongoDB
- **Validation**: Pydantic v2
- **Documentation**: Swagger UI + ReDoc

## User Personas
1. **Undergraduate Students** - Learning backend development for the first time
2. **Lab Instructors** - Need comprehensive teaching materials

## Core Requirements (Static)
| Requirement | Status |
|-------------|--------|
| Item CRUD endpoints | ✅ Implemented |
| Data validation | ✅ Implemented |
| Swagger UI documentation | ✅ Implemented |
| Search by name | ✅ Implemented |
| Pagination | ✅ Implemented |
| Category filter | ✅ Implemented |
| Teaching documentation | ✅ Implemented |
| Lab worksheet | ✅ Implemented |

## What's Been Implemented

### Feb 18, 2026
- Created comprehensive FastAPI backend with all CRUD operations
- Implemented Item model with: id, name, description, price, quantity, category
- Added validation rules (price > 0, quantity >= 0, name required)
- Search functionality (case-insensitive name search)
- Pagination (page, page_size parameters)
- Category filter
- Statistics endpoint (/api/items/stats/summary)
- Health check endpoint
- Swagger UI with rich documentation
- README.md with installation, curl examples, viva questions, MCQs, rubric
- LAB_WORKSHEET.md with step-by-step instructions for 4-hour lab

### API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/ | Welcome message |
| GET | /api/health | Health check |
| POST | /api/items | Create item |
| GET | /api/items | List items (paginated) |
| GET | /api/items/{id} | Get item by ID |
| PUT | /api/items/{id} | Update item |
| DELETE | /api/items/{id} | Delete item |
| GET | /api/items/stats/summary | Statistics |

## Prioritized Backlog

### P0 (Critical) - DONE
- ✅ All CRUD operations
- ✅ Data validation
- ✅ Search & pagination
- ✅ Documentation

### P1 (High Priority) - Future
- Add authentication (JWT)
- Add unit tests with pytest
- Add rate limiting

### P2 (Medium Priority) - Future
- Add bulk operations
- Add export to CSV
- Add sorting options
- Add tags field to items

## Next Tasks
1. User may want to add authentication
2. User may want to deploy to production
3. Could add more comprehensive pytest tests
