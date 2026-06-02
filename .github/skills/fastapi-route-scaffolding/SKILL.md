---
name: fastapi-route-scaffolding
description: Generate FastAPI routes, Pydantic models, and MongoDB repositories following project conventions.
---



# FastAPI Route and MongoDB Model Scaffolding

## Overview

This skill helps developers quickly create new API routes, Pydantic data models, and MongoDB repository code for the FastAPI-based Mergington High School Management System. It streamlines the creation of consistent, well-structured API endpoints following project conventions.

## Purpose

Creating new features in FastAPI requires writing several interconnected components:
- **Router files** with endpoint definitions
- **Pydantic models** for request/response validation
- **MongoDB repositories** for database operations
- **Error handling** with appropriate HTTP status codes

This skill automates the scaffolding of these components, ensuring consistency and reducing boilerplate code.

## When to Use This Skill

Use this skill when you need to:

✅ Create new API endpoints for a feature (e.g., grades module, notifications, student profiles)  
✅ Add new database models to MongoDB  
✅ Implement CRUD operations for a new resource  
✅ Generate request/response validation models  
✅ Set up repository methods with error handling  
✅ Ensure consistency across multiple related endpoints  

❌ Don't use if: You're modifying an existing small endpoint or fixing a bug in existing code  
❌ Don't use if: You need complex business logic that doesn't follow standard CRUD patterns

## Workflow

The skill follows this automated workflow:

1. **Analyze the Request**: Parse the user's intent for what route/feature to create
2. **Generate Models**: Create Pydantic models for request/response validation
3. **Generate Repository Code**: Create MongoDB query methods
4. **Generate Router Code**: Create FastAPI route handlers
5. **Generate Integration**: Create code to register the router in the main app
6. **Provide Examples**: Show usage examples and best practices

## Usage Examples

### Example 1: Creating a grades management endpoint

**User Request:**
```
Create a new FastAPI route for managing student grades with:
- Endpoint: /grades
- Operations: GET all grades, GET grade by ID, POST new grade, UPDATE grade
- Fields: student_id, activity_id, score (0-100), date_assigned
```

**Skill Generates:**
- `src/backend/routers/grades.py` - Route handlers
- `src/backend/models/grades.py` - Pydantic models
- `src/backend/repositories/grades.py` - MongoDB operations
- Integration snippet for `src/app.py`
- Unit test template

### Example 2: Creating a student reports endpoint

**User Request:**
```
Add a reports endpoint to track student participation and attendance.
Include generate report, list reports, and get report details.
```

**Skill Generates:**
- Complete router with all endpoints
- Request/response models with validation
- Database repository with queries
- Error handling for common scenarios
- API documentation comments

## Key Features

### 1. Consistent Project Structure
The skill maintains the project's directory structure:
```
src/backend/
  ├── routers/           # API endpoint definitions
  ├── models/            # Pydantic validation models
  ├── repositories/      # MongoDB data access layer
  └── database.py        # Database collections
```

### 2. Automatic Error Handling
Generated code includes proper HTTP error responses:
- `400 Bad Request` - Invalid input
- `404 Not Found` - Resource doesn't exist
- `409 Conflict` - Duplicate or constraint violation
- `500 Internal Server Error` - Database errors

### 3. Type Safety
Uses Pydantic models for:
- Input validation
- Response serialization
- IDE autocomplete support
- API documentation generation

### 4. MongoDB Integration
Generates repository methods that:
- Use proper MongoDB aggregation pipelines
- Handle ObjectId conversions
- Implement pagination and filtering
- Return typed responses

### 5. FastAPI Best Practices
- Clear endpoint documentation
- Proper HTTP status codes
- Response models with `response_model`
- Type hints on all parameters
- Query parameter validation

## Example Output

### Generated Router File
```python
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional, List
from ..database import grades_collection
from ..repositories.grades import GradesRepository
from ..models.grades import GradeCreate, GradeUpdate, GradeResponse

router = APIRouter(
    prefix="/grades",
    tags=["grades"]
)

grades_repo = GradesRepository()

@router.get("", response_model=List[Dict[str, Any]])
def get_all_grades(
    activity_id: Optional[str] = Query(None),
    student_id: Optional[str] = Query(None)
) -> List[Dict[str, Any]]:
    """
    Get all grades with optional filtering
    
    Query parameters:
    - activity_id: Filter by activity
    - student_id: Filter by student
    """
    return grades_repo.find_grades(activity_id=activity_id, student_id=student_id)

@router.post("", response_model=Dict[str, Any], status_code=201)
def create_grade(grade: GradeCreate) -> Dict[str, Any]:
    """Create a new grade record"""
    return grades_repo.create_grade(grade.dict())

@router.get("/{grade_id}", response_model=Dict[str, Any])
def get_grade(grade_id: str) -> Dict[str, Any]:
    """Get a specific grade by ID"""
    grade = grades_repo.get_grade_by_id(grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    return grade
```

### Generated Pydantic Model
```python
from pydantic import BaseModel, Field
from typing import Optional

class GradeCreate(BaseModel):
    """Model for creating a new grade"""
    student_id: str = Field(..., description="Student ID")
    activity_id: str = Field(..., description="Activity ID")
    score: int = Field(..., ge=0, le=100, description="Score 0-100")
    date_assigned: str = Field(..., description="ISO format date")

class GradeUpdate(BaseModel):
    """Model for updating a grade"""
    score: Optional[int] = Field(None, ge=0, le=100)
    date_assigned: Optional[str] = None

class GradeResponse(GradeCreate):
    """Model for grade responses"""
    grade_id: str
    created_at: str
```

### Generated Repository
```python
from typing import Dict, Any, Optional, List
from ..database import grades_collection
from bson import ObjectId

class GradesRepository:
    """Data access layer for grades"""
    
    def find_grades(self, activity_id: Optional[str] = None, 
                   student_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Find grades with optional filters"""
        query = {}
        if activity_id:
            query["activity_id"] = activity_id
        if student_id:
            query["student_id"] = student_id
        
        grades = []
        for grade in grades_collection.find(query):
            grade["_id"] = str(grade["_id"])
            grades.append(grade)
        return grades
    
    def create_grade(self, grade_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new grade record"""
        result = grades_collection.insert_one(grade_data)
        grade_data["_id"] = str(result.inserted_id)
        return grade_data
    
    def get_grade_by_id(self, grade_id: str) -> Optional[Dict[str, Any]]:
        """Get grade by ID"""
        try:
            grade = grades_collection.find_one({"_id": ObjectId(grade_id)})
            if grade:
                grade["_id"] = str(grade["_id"])
            return grade
        except Exception:
            return None
```

## Best Practices

### 1. Naming Conventions
- **Routers**: `plural_module.py` (e.g., `grades.py`, `reports.py`)
- **Models**: `module_name.py` (e.g., `grades.py` in models folder)
- **Repositories**: `module_name.py` (e.g., `grades.py` in repositories folder)
- **Collections**: Use snake_case, plural (e.g., `grades_collection`)

### 2. Error Handling
Always include error handlers:
```python
try:
    result = grades_collection.insert_one(grade_data)
except Exception as e:
    raise HTTPException(status_code=400, detail=f"Failed to create grade: {str(e)}")
```

### 3. Validation
Use Pydantic's validators for business logic:
```python
from pydantic import validator

class GradeCreate(BaseModel):
    score: int
    
    @validator('score')
    def validate_score(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Score must be between 0 and 100')
        return v
```

### 4. Documentation
Every endpoint should have clear docstrings:
```python
@router.get("/{grade_id}")
def get_grade(grade_id: str) -> Dict[str, Any]:
    """
    Get a specific grade record
    
    - grade_id: The grade's unique identifier
    """
```

### 5. Filtering and Pagination
For LIST endpoints, include filtering and pagination:
```python
@router.get("", response_model=List[Dict[str, Any]])
def get_grades(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    activity_id: Optional[str] = None
) -> List[Dict[str, Any]]:
```

## How Copilot Uses This Skill

When the user requests to create a new route:

1. **Copilot reads this skill** to understand the project's conventions
2. **Copilot runs the scaffolding script** to generate code templates
3. **Copilot creates the necessary files**:
   - Pydantic models in `src/backend/models/`
   - Repository class in `src/backend/repositories/`
   - Router in `src/backend/routers/`
4. **Copilot updates `src/app.py`** to register the new router
5. **Copilot generates tests** (optional)
6. **Copilot provides guidance** on where to customize business logic

## Supported Operations

The skill automatically generates CRUD scaffolding for:

- **C** - Create (POST endpoint)
- **R** - Read (GET single/list endpoints)
- **U** - Update (PUT/PATCH endpoints)
- **D** - Delete (DELETE endpoint)

Each operation includes:
- Proper URL path design
- Request/response validation
- Error handling
- HTTP status codes
- Docstrings

## Customization

After generation, developers should:

1. **Add business logic** - The repository methods provide the data layer skeleton
2. **Implement validators** - Add Pydantic validators for domain rules
3. **Add permissions** - Implement role-based access control if needed
4. **Add tests** - Use generated test template as a starting point
5. **Document APIs** - FastAPI auto-generates docs at `/docs`

## Integration with Main App

The skill generates:
```python
# Add to src/app.py
from .backend.routers import grades

app.include_router(grades.router)
```

This makes the endpoint available at the specified prefix.

## Learning Resource

For developers learning FastAPI:
- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Models](https://docs.pydantic.dev/)
- [MongoDB with PyMongo](https://pymongo.readthedocs.io/)
- Project examples in `.github/skills/fastapi-route-scaffolding/examples/`

## Troubleshooting

### Issue: Generated code doesn't import correctly
**Solution**: Ensure the new router file is in `src/backend/routers/` and `src/backend/routers/__init__.py` is updated

### Issue: MongoDB operations failing
**Solution**: Check that collections are initialized in `src/backend/database.py`

### Issue: Pydantic validation errors
**Solution**: Verify field types match database schema and add custom validators if needed

## Related Skills and Tools

- **API Documentation Generation** - Once routes are created, generate OpenAPI specs
- **Test Generation** - Auto-generate unit tests for new endpoints
- **Database Validation Review** - Review schema changes and constraints
- **Permission and Authorization** - Add role-based access control to routes
