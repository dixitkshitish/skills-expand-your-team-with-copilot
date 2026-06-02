# FastAPI Route Scaffolding Examples

This folder contains example output from the `route_scaffolder.py` script. These examples show how Copilot generates code for new API routes.

## Example: Grades Module

The following files show a complete example of what gets generated for a grades management feature:

- **grades_models_example.py** - Pydantic models for validation
- **grades_repository_example.py** - Database access layer
- **grades_router_example.py** - FastAPI endpoints
- **grades_integration_example.md** - Integration steps

### Running the Example

To generate this same code structure, run:

```bash
python scripts/route_scaffolder.py --name grades --fields "student_id:str,activity_id:str,score:int,date_assigned:str"
```

### Integration with Your Project

1. **Create the models file** - `src/backend/models/grades.py`
   - Copy code from `grades_models_example.py`

2. **Create the repository file** - `src/backend/repositories/grades.py`
   - Copy code from `grades_repository_example.py`
   - Add any domain-specific query methods

3. **Create the router file** - `src/backend/routers/grades.py`
   - Copy code from `grades_router_example.py`
   - Customize endpoints as needed

4. **Update database.py** - Add to `src/backend/database.py`
   ```python
   grades_collection = db['grades']
   ```

5. **Update app.py** - Add to `src/app.py`
   ```python
   from .backend.routers import grades
   app.include_router(grades.router)
   ```

6. **Create tests** - `tests/test_grades.py`
   - Use the test template from the scaffolder

### What Each File Does

#### Models (grades_models_example.py)
- Defines Pydantic models for request/response validation
- Ensures type safety and automatic API documentation
- Provides JSON schema examples

#### Repository (grades_repository_example.py)
- Handles all MongoDB database operations
- Provides clean separation between routes and data layer
- Includes CRUD operations and custom queries
- Handles error cases gracefully

#### Router (grades_router_example.py)
- Exposes HTTP endpoints for the grades feature
- Validates requests using Pydantic models
- Returns proper HTTP status codes
- Includes comprehensive error handling

### Customizing Generated Code

After scaffolding, you'll need to:

1. **Add validators** - Use Pydantic `@validator` decorators for business rules:
   ```python
   @validator('score')
   def validate_score(cls, v):
       if v < 0 or v > 100:
           raise ValueError('Score must be between 0 and 100')
       return v
   ```

2. **Add indexes** - For frequently queried fields:
   ```python
   grades_collection.create_index("student_id")
   grades_collection.create_index("activity_id")
   ```

3. **Add permissions** - In router, check user roles:
   ```python
   from .auth import get_current_teacher
   
   @router.get("/{grade_id}")
   def get_grade(grade_id: str, teacher = Depends(get_current_teacher)):
       # Validate authorization
   ```

4. **Add tests** - Use FastAPI's TestClient:
   ```python
   client = TestClient(app)
   response = client.get("/grades")
   assert response.status_code == 200
   ```

## Example Output Structure

```
src/backend/
├── models/
│   └── grades.py                    # From grades_models_example.py
├── repositories/
│   └── grades.py                    # From grades_repository_example.py
├── routers/
│   └── grades.py                    # From grades_router_example.py
└── database.py                      # Updated with grades_collection

tests/
└── test_grades.py                   # New unit tests

app.py                              # Updated with router registration
```

## Running the Project

Once integrated:

```bash
# Install dependencies
pip install -r src/requirements.txt

# Run the app
python -m uvicorn src.app:app --reload

# Test the endpoints
curl http://localhost:8000/grades
curl -X POST http://localhost:8000/grades -H "Content-Type: application/json" \
  -d '{"student_id":"alice","activity_id":"chess","score":92,"date_assigned":"2024-06-02"}'

# View API documentation
# Navigate to http://localhost:8000/docs
```

## Best Practices Applied

- ✅ Clear separation of concerns (router, repository, models)
- ✅ Type safety with Pydantic validation
- ✅ Consistent error handling and HTTP status codes
- ✅ MongoDB ObjectId handling
- ✅ Pagination support on list endpoints
- ✅ RESTful API design
- ✅ Comprehensive docstrings
- ✅ Database efficiency with skip/limit
