# FastAPI Route Scaffolding - Technical Reference

## Skill Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Copilot User Request                                      │
│  "Create attendance tracking API"                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  Copilot Reads Skill Documentation (SKILL.md)             │
│  - Understands conventions                                  │
│  - Identifies use cases that match                         │
│  - Plans approach                                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  Execute Scaffolding Script                                │
│  python route_scaffolder.py \                              │
│    --name attendance \                                      │
│    --fields "student_id:str,activity_id:str,..."          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  Script Generates Four Components:                         │
│  1. Pydantic Models (models/attendance.py)                │
│  2. MongoDB Repository (repositories/attendance.py)        │
│  3. FastAPI Router (routers/attendance.py)                │
│  4. Integration Instructions                               │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  Copilot Creates Files and Guides Integration             │
│  - Writes generated code to correct locations             │
│  - Updates app.py with router registration               │
│  - Updates database.py with collection setup             │
│  - Provides next steps and customization options         │
└─────────────────────────────────────────────────────────────┘
```

## Script Internals

### RouteScaffolder Class

The `RouteScaffolder` class handles all code generation:

```python
class RouteScaffolder:
    def __init__(self, module_name: str)
        # Initialize with module name (e.g., "attendance")
        # Derives singular form for route parameters
        # Sets up collection name
    
    def add_field(self, field_name: str, field_type: str, required: bool)
        # Registers a field to be included in generated models
        # Tracks type and requirement status
    
    def generate_model() -> str
        # Creates Pydantic BaseModel classes:
        #   - {Module}Create - for POST requests
        #   - {Module}Update - for PUT/PATCH requests  
        #   - {Module}Response - for GET responses
    
    def generate_repository() -> str
        # Creates data access layer with methods:
        #   - find_all() - list with pagination
        #   - find_by_id() - retrieve single item
        #   - create() - insert new document
        #   - update() - modify existing
        #   - delete() - remove document
        #   - count() - get total count
    
    def generate_router() -> str
        # Creates FastAPI router with endpoints:
        #   - GET / - list all items
        #   - POST / - create new item
        #   - GET /{id} - get single item
        #   - PUT /{id} - update item
        #   - DELETE /{id} - delete item
    
    def generate_app_integration() -> str
        # Instructions for app.py modification
    
    def generate_database_init() -> str
        # Instructions for database.py modification
    
    def generate_test_template() -> str
        # Unit test skeleton using FastAPI TestClient
```

## Code Generation Patterns

### 1. Pydantic Model Generation

**Input:**
```
Fields: student_id:str, activity_id:str, attended:bool, date:str
```

**Generated Create Model:**
```python
class AttendanceCreate(BaseModel):
    """Model for creating a new attendance"""
    student_id: str = Field(..., description="student_id")
    activity_id: str = Field(..., description="activity_id")
    attended: bool = Field(..., description="attended")
    date: str = Field(..., description="date")
```

**Generated Update Model:**
```python
class AttendanceUpdate(BaseModel):
    """Model for updating a attendance"""
    student_id: Optional[str] = Field(None, description="student_id")
    activity_id: Optional[str] = Field(None, description="activity_id")
    attended: Optional[bool] = Field(None, description="attended")
    date: Optional[str] = Field(None, description="date")
```

**Generated Response Model:**
```python
class AttendanceResponse(AttendanceCreate):
    """Model for attendance responses"""
    id: str = Field(..., description="Unique identifier")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
```

### 2. Repository Generation Pattern

**Base CRUD Operations:**
```python
class {Module}Repository:
    # find_all(skip, limit) - SELECT with pagination
    # find_by_id(id) - SELECT single document
    # create(data) - INSERT new document
    # update(id, data) - UPDATE document
    # delete(id) - DELETE document
    # count() - SELECT COUNT
```

**Error Handling Pattern:**
- try/except blocks around ObjectId conversions
- Returns None on failed lookups
- Returns False on failed deletions
- Returns modified count for updates

**Timestamp Management:**
- Auto-adds created_at on insert
- Auto-adds updated_at on insert/update
- Uses datetime.utcnow() for consistency

### 3. Router Generation Pattern

**Each Endpoint Includes:**
```
- HTTPException handling with appropriate status codes
  - 200 OK (GET successful)
  - 201 Created (POST successful)
  - 204 No Content (DELETE successful)
  - 400 Bad Request (invalid input)
  - 404 Not Found (resource missing)
  - 500 Internal Server Error (database error)

- Type hints for all parameters and returns
  - Query parameters with descriptions
  - Status code specification
  - Response models

- Comprehensive docstrings
  - Endpoint purpose
  - Parameter descriptions
  - Optional error conditions
```

**Route Structure:**
```python
@router.{METHOD}("{path}", response_model={Model}, status_code={code})
def {endpoint_name}({parameters}) -> {ReturnType}:
    """Docstring"""
    try:
        # Call repository method
        # Handle result
        return result
    except HTTPException:
        raise  # Re-raise HTTP errors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Integration Points

### How Copilot Coordinates Integration

1. **Read this skill** (`SKILL.md`)
   - Understand project conventions
   - Identify where files should go
   - Learn about error handling patterns

2. **Run the script** (optional, Copilot can generate directly)
   ```bash
   python .github/skills/fastapi-route-scaffolding/scripts/route_scaffolder.py \
     --name {module} \
     --fields "{field_definitions}"
   ```

3. **Create files**:
   - `src/backend/models/{module}.py` - Copilot generates models
   - `src/backend/repositories/{module}.py` - Copilot generates repository
   - `src/backend/routers/{module}.py` - Copilot generates router

4. **Update existing files**:
   - `src/backend/database.py` - Add collection initialization
   - `src/app.py` - Import and register router
   - `src/backend/__init__.py` - Export new modules if needed

5. **Verify integration**:
   - Check imports resolve correctly
   - Confirm collection is accessible
   - Test endpoints are available

## Naming Conventions

| Element | Pattern | Example |
|---------|---------|---------|
| Module Name | plural, snake_case | `attendance`, `student_records` |
| Class Name | PascalCase | `Attendance`, `StudentRecords` |
| Collection Name | module_collection | `attendance_collection` |
| Router Prefix | /{module} | `/attendance` |
| Singular Path Param | {singular_id} | `/{attendance_id}` |
| Create Model | {Module}Create | `AttendanceCreate` |
| Update Model | {Module}Update | `AttendanceUpdate` |
| Response Model | {Module}Response | `AttendanceResponse` |
| Repository Class | {Module}Repository | `AttendanceRepository` |
| Repository File | module.py | `attendance.py` |

## Type Mapping

**Supported Field Types:**

| Python Type | Pydantic Type | MongoDB Representation |
|------------|---------------|----------------------|
| str | str | String |
| int | int | Integer 32-bit |
| float | float | Double |
| bool | bool | Boolean |
| list | List[T] | Array |
| dict | Dict[str, Any] | Object |
| datetime | datetime | Date |
| Optional[T] | Optional[T] | Nullable |

## Example: Complete Generation Trace

### Input
```
User Request: "Create an API for managing staff profiles"
Script invocation: 
  --name staff_profiles
  --fields "full_name:str,email:str,department:str,phone:str"
```

### Execution Flow

1. **Initialize**
   - module_name = "staff_profiles"
   - module_singular = "staff_profile"
   - collection_name = "staff_profiles_collection"

2. **Add Fields**
   - full_name: str (required)
   - email: str (required)
   - department: str (required)
   - phone: str (required)

3. **Generate Models**
   - StaffProfileCreate - all fields required
   - StaffProfileUpdate - all fields optional
   - StaffProfileResponse - includes id, created_at, updated_at

4. **Generate Repository**
   - StaffProfilesRepository class
   - All CRUD methods with error handling
   - MongoDB ObjectId handling
   - Timestamp management

5. **Generate Router**
   - Prefix: /staff_profiles
   - GET / - list all staff profiles with pagination
   - POST / - create new staff profile
   - GET /{staff_profile_id} - get single profile
   - PUT /{staff_profile_id} - update profile
   - DELETE /{staff_profile_id} - delete profile

6. **Output**
   - All code is printed to stdout
   - Integration instructions provided
   - File locations specified

### Generated Files Locations

```
src/
├── backend/
│   ├── models/
│   │   └── staff_profiles.py          ← Generated
│   ├── repositories/
│   │   └── staff_profiles.py          ← Generated
│   └── routers/
│       └── staff_profiles.py          ← Generated
├── app.py                             ← Needs update
└── backend/database.py                ← Needs update
```

## Performance Optimizations

The generated code includes:

1. **Pagination Support**
   - Skip/limit on list endpoints
   - Prevents loading entire collections

2. **ObjectId Conversion**
   - Efficient handling of MongoDB IDs
   - Error handling for invalid IDs

3. **Timestamp Indexing**
   - Pre-calculated UTC timestamps
   - Can be indexed for efficient sorting

4. **Lazy Loading**
   - Database queries only when needed
   - No unnecessary aggregations

## Security Considerations

Generated code should be customized with:

1. **Authentication/Authorization**
   ```python
   from .auth import get_current_user
   
   @router.post("/")
   def create(item: Model, user=Depends(get_current_user)):
       # Verify user has permission
       if not user.can_create_items:
           raise HTTPException(status_code=403)
   ```

2. **Input Validation**
   ```python
   @validator('email')
   def validate_email(cls, v):
       # Additional email validation
       return v
   ```

3. **Field Permissions**
   - Only expose necessary fields in responses
   - Use Pydantic field exclusion for sensitive data

## Extending the Scaffolder

To add new features:

1. **New field types** - Add to type_mapping in script
2. **New query patterns** - Add methods to repository template
3. **New endpoints** - Extend router template
4. **Custom validators** - Generate validator stubs

Edit `scripts/route_scaffolder.py` to extend functionality.

## Troubleshooting for Copilot

### Issue: Script not found
**Solution**: Ensure path is relative to workspace root:
```
.github/skills/fastapi-route-scaffolding/scripts/route_scaffolder.py
```

### Issue: Import errors after generation
**Solution**: Ensure `__init__.py` files exist in:
- `src/backend/models/`
- `src/backend/repositories/`
- `src/backend/routers/`

### Issue: Collection not found at runtime
**Solution**: Verify collection is initialized in `database.py`:
```python
staff_profiles_collection = db['staff_profiles']
```

### Issue: Validation errors in tests
**Solution**: Ensure generated models match actual field requirements, add custom validators for domain rules

## Related Documentation

- [FastAPI Official Docs](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [PyMongo Guide](https://pymongo.readthedocs.io/)
- [Project README](../../README.md)
