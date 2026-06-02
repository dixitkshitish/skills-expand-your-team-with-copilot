# FastAPI Route Scaffolding - Usage Guide

## Quick Start

### For Developers

When you need to create a new API feature in the Mergington High School application:

1. **Use Copilot Chat** with a request like:
   ```
   Create a new API route for student attendance tracking with these fields:
   - student_id (string)
   - activity_id (string)  
   - attended (boolean)
   - date (ISO timestamp)
   - notes (optional string)
   ```

2. **Copilot will**:
   - Run the scaffolding script with your specifications
   - Generate Pydantic models, repository, and router code
   - Provide integration instructions
   - Create test templates

3. **You customize**:
   - Add business logic and validators
   - Integrate with authentication if needed
   - Write comprehensive tests
   - Document domain-specific behavior

### For Copilot Agents

The scaffolding skill can be invoked programmatically:

```bash
# Generate scaffolding for a new module
python .github/skills/fastapi-route-scaffolding/scripts/route_scaffolder.py \
  --name attendance \
  --fields "student_id:str,activity_id:str,attended:bool,date:str,notes:str"
```

## Common Use Cases

### 1. Student Attendance Management

**Request to Copilot:**
```
Create an attendance tracking API with:
- Endpoint: /attendance
- Fields: student_id, activity_id, attended (bool), date, notes (optional)
- Include filtering by activity and date range
```

**Generated Outputs:**
- Models with validation
- Repository with date filtering
- Router with list/create/update/delete endpoints
- Boolean validation for attendance flag

**Additional Customization Needed:**
```python
# In models/attendance.py, add validators:
@validator('date')
def validate_date(cls, v):
    from datetime import datetime
    try:
        datetime.fromisoformat(v)
    except ValueError:
        raise ValueError('Invalid date format, use ISO 8601')
    return v

@validator('attended')
def validate_attended(cls, v):
    if not isinstance(v, bool):
        raise ValueError('attended must be true or false')
    return v
```

### 2. Staff Member Profiles

**Request to Copilot:**
```
Create an API for managing staff/advisor profiles including:
- name, email, department, phone
- role (staff, teacher, counselor)
- office_location, availability
- Include search by department and role
```

**Generated Outputs:**
- Models with role enum
- Repository with filtering
- Router with search endpoints
- Integration with database

**Customization:**
```python
# Add enum for roles
from enum import Enum

class StaffRole(str, Enum):
    STAFF = "staff"
    TEACHER = "teacher"
    COUNSELOR = "counselor"
    DIRECTOR = "director"

# Update model
class StaffCreate(BaseModel):
    name: str
    role: StaffRole
    email: str
    ...
```

### 3. Permission and Role-Based Access

**Request to Copilot:**
```
Create an RBAC endpoint that:
- Manages permissions for different user roles
- Tracks who can access what features
- Includes audit logging of permission changes
```

**Generated Outputs:**
- Models for permissions
- Repository for permission storage
- Router with permission endpoints
- Basic audit trail structure

**Customization:**
```python
# Add permission checks to routes
from .auth import get_current_user, check_permission

@router.post("/permissions")
def grant_permission(
    permission: PermissionCreate,
    current_user = Depends(get_current_user)
):
    # Check if user has admin role
    if not check_permission(current_user, "manage_permissions"):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    # Log the change
    audit_log.create({
        "user": current_user.id,
        "action": "grant_permission",
        "data": permission.dict()
    })
    
    return repository.create(permission.dict())
```

## Script Usage Reference

### Basic Usage

```bash
# Generate code for a simple module
python scripts/route_scaffolder.py --name activities

# Generate with specific fields
python scripts/route_scaffolder.py \
  --name reports \
  --fields "title:str,description:str,date:str,status:str"
```

### Advanced Usage

```bash
# Generate all components and save to directory
python scripts/route_scaffolder.py \
  --name student_records \
  --fields "gpa:float,grade_level:int,enrollment_status:str" \
  --output ./generated \
  --all
```

### Script Output

The script outputs:

1. **Pydantic Models**
   - CreateModel with required fields
   - UpdateModel with optional fields
   - ResponseModel with metadata

2. **Repository Class**
   - CRUD methods (Create, Read, Update, Delete)
   - List with pagination
   - Count operation
   - Skeleton for custom queries

3. **FastAPI Router**
   - GET endpoints (list, get by id)
   - POST endpoint (create)
   - PUT endpoint (update)
   - DELETE endpoint (delete)
   - Proper status codes and error handling

4. **Integration Instructions**
   - How to update app.py
   - How to initialize database.py
   - Where to create files

5. **Test Template**
   - Unit test skeleton
   - Test for each CRUD operation
   - FastAPI TestClient usage

## Project Structure Reference

```
.github/
└── skills/
    └── fastapi-route-scaffolding/
        ├── SKILL.md                          # This skill documentation
        ├── scripts/
        │   └── route_scaffolder.py           # The scaffolding script
        ├── examples/
        │   ├── README.md                     # Examples overview
        │   ├── grades_models_example.py      # Example Pydantic models
        │   ├── grades_repository_example.py  # Example repository
        │   └── grades_router_example.py      # Example router
        └── usage/                            # Additional guides
            └── USAGE.md                      # This file

src/
├── app.py                                   # Main FastAPI app
├── backend/
│   ├── database.py                          # Database setup
│   ├── models/                              # Pydantic models
│   │   ├── __init__.py
│   │   └── grades.py                        # Example generated model
│   ├── repositories/                        # Data access layer
│   │   ├── __init__.py
│   │   └── grades.py                        # Example generated repository
│   └── routers/                             # API endpoints
│       ├── __init__.py
│       ├── activities.py
│       ├── auth.py
│       └── grades.py                        # Example generated router
└── static/                                  # Frontend files

tests/
└── test_grades.py                          # Example generated tests
```

## Integration Checklist

After generating scaffolding:

- [ ] Create `src/backend/models/{module}.py`
- [ ] Create `src/backend/repositories/{module}.py`
- [ ] Create `src/backend/routers/{module}.py`
- [ ] Add collection to `src/backend/database.py`
- [ ] Import and register router in `src/app.py`
- [ ] Run `pip install -r src/requirements.txt` if dependencies changed
- [ ] Run app and test at `http://localhost:8000/docs`
- [ ] Create `tests/test_{module}.py`
- [ ] Run tests: `pytest tests/test_{module}.py -v`
- [ ] Add validators for business logic
- [ ] Document any custom endpoints

## Example: Complete Integration

### 1. Generate scaffolding
```bash
python .github/skills/fastapi-route-scaffolding/scripts/route_scaffolder.py \
  --name attendance \
  --fields "student_id:str,activity_id:str,attended:bool,date_assigned:str"
```

### 2. Create models file: `src/backend/models/attendance.py`
```python
# Copy generated GradeCreate, GradeUpdate, GradeResponse classes
# Rename to AttendanceCreate, AttendanceUpdate, AttendanceResponse
# Adjust field names and types
```

### 3. Create repository: `src/backend/repositories/attendance.py`
```python
# Copy generated GradesRepository
# Rename to AttendanceRepository
# Add attendance-specific queries like find_by_date_range()
```

### 4. Create router: `src/backend/routers/attendance.py`
```python
# Copy generated router
# Update prefix to "/attendance"
# Add bulk upload endpoint if needed
```

### 5. Update `src/backend/database.py`
```python
# Add after other collections
attendance_collection = db['attendance']

# Add to init_database():
if attendance_collection.count_documents({}) == 0:
    pass  # No initial data needed
```

### 6. Update `src/app.py`
```python
# Add to imports
from .backend.routers import attendance

# Add after other routers
app.include_router(attendance.router)
```

### 7. Test endpoints
```bash
# Start app
python -m uvicorn src.app:app --reload

# In another terminal
curl http://localhost:8000/attendance
curl -X POST http://localhost:8000/attendance \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "alice",
    "activity_id": "chess",
    "attended": true,
    "date_assigned": "2024-06-02"
  }'
```

## Troubleshooting

### Import Errors
**Problem**: `ModuleNotFoundError: No module named '...repositories...'`

**Solution**: 
- Ensure `src/backend/repositories/__init__.py` exists
- Confirm repository file is in the correct directory
- Check import path matches actual file location

### Script Errors
**Problem**: Script fails to generate code

**Solution**:
- Verify Python 3.7+ is installed
- Check script has execute permissions: `chmod +x scripts/route_scaffolder.py`
- Ensure field definitions are correct: `--fields "field1:str,field2:int"`

### Type Validation Issues
**Problem**: FastAPI returns validation error for valid requests

**Solution**:
- Check Pydantic model field types match your data
- Add custom validators for complex validation
- Review error message in response for specifics

## Performance Considerations

For better performance when many routes are scaffolded:

1. **Add database indexes**:
   ```python
   # In database.py init_database()
   attendance_collection.create_index("student_id")
   attendance_collection.create_index("date_assigned")
   attendance_collection.create_index([("student_id", 1), ("date_assigned", -1)])
   ```

2. **Use pagination**:
   ```python
   # In routers, always include skip/limit for list endpoints
   @router.get("")
   def list_items(
       skip: int = Query(0, ge=0),
       limit: int = Query(10, ge=1, le=100)
   ):
   ```

3. **Batch operations**:
   ```python
   # For bulk creates, use insert_many()
   def create_batch(self, items: List[Dict]) -> List[str]:
       result = collection.insert_many(items)
       return [str(id) for id in result.inserted_ids]
   ```

## Contributing Improvements

To improve this skill:

1. Add new field types to the scaffolder
2. Add more complex query patterns to repository template
3. Add authentication examples
4. Add pagination helpers
5. Add caching strategies

Edit `scripts/route_scaffolder.py` and submit improvements!
