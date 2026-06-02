#!/usr/bin/env python3
"""
Quick Reference: FastAPI Route Scaffolding Skill

Print this file or use it as a reference while developing new API features.
"""

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║         FastAPI Route & MongoDB Model Scaffolding: Quick Reference         ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 WHAT THIS SKILL DOES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Automatically generates FastAPI routes, Pydantic models, and MongoDB repositories
for new API features, following project conventions and best practices.

📋 HOW TO USE IT
━━━━━━━━━━━━━━━━
1. Ask Copilot: "Create an API for [feature name]"
2. Copilot generates all necessary code
3. You customize with business logic
4. Everything integrates automatically

🚀 QUICK EXAMPLES
━━━━━━━━━━━━━━━━

Example 1: Attendance Tracking
  Ask Copilot: "Create attendance tracking API with student_id, activity_id, 
               attended (bool), date, notes fields"
  
  Copilot generates:
    - Pydantic models in src/backend/models/attendance.py
    - Repository in src/backend/repositories/attendance.py
    - Router in src/backend/routers/attendance.py
    - Integration code for app.py and database.py

Example 2: Grade Management
  Ask Copilot: "Build grades management with student_id, activity_id, 
               score (0-100), date fields"
  
  Copilot generates complete CRUD API with validation

Example 3: Student Profiles
  Ask Copilot: "Create student profile API with name, email, grade_level, gpa"
  
  Copilot generates searchable profile management system

📝 FILE STRUCTURE CREATED
━━━━━━━━━━━━━━━━━━━━━━━

src/backend/
├── models/
│   └── {module}.py              ← Pydantic validation models
├── repositories/
│   └── {module}.py              ← Database access layer (CRUD)
└── routers/
    └── {module}.py              ← FastAPI endpoints

tests/
└── test_{module}.py             ← Unit tests

app.py                            ← Update: import and register router
database.py                       ← Update: add collection initialization

🔧 NAMING CONVENTIONS
━━━━━━━━━━━━━━━━━━

Module Name:       attendance, grades, student_profiles (snake_case)
Class Names:       Attendance, GradesRepository (PascalCase)
Route Prefix:      /attendance, /grades (slash + module name)
Parameter:         {attendance_id}, {grade_id} (singular + _id)

📊 GENERATED ENDPOINTS
━━━━━━━━━━━━━━━━━━━

For each module, Copilot creates:

GET    /module              → List all (with pagination)
POST   /module              → Create new (returns 201)
GET    /module/{id}         → Get single
PUT    /module/{id}         → Update
DELETE /module/{id}         → Delete (returns 204)

Example for attendance:
  GET    /attendance
  POST   /attendance
  GET    /attendance/{attendance_id}
  PUT    /attendance/{attendance_id}
  DELETE /attendance/{attendance_id}

🛡️ HTTP STATUS CODES
━━━━━━━━━━━━━━━━━

200 ✓  OK               GET, PUT successful
201 ✓  Created          POST successful
204 ✓  No Content       DELETE successful
400 ✗  Bad Request      Invalid input
404 ✗  Not Found        Resource doesn't exist
500 ✗  Server Error     Database error

💾 DATABASE INTEGRATION
━━━━━━━━━━━━━━━━━━━

Update src/backend/database.py:

  # Add collection
  attendance_collection = db['attendance']
  
  # Initialize if empty (in init_database())
  if attendance_collection.count_documents({}) == 0:
      pass  # Add sample data if needed

Copilot shows you exactly what to add!

🔗 ROUTER REGISTRATION
━━━━━━━━━━━━━━━━━━━━

Update src/app.py:

  # Add import
  from .backend.routers import attendance
  
  # Register router
  app.include_router(attendance.router)

Copilot shows you the exact code to add!

🧪 TESTING YOUR NEW API
━━━━━━━━━━━━━━━━━━━━━

Start the server:
  python -m uvicorn src.app:app --reload

View API docs:
  http://localhost:8000/docs

Test endpoints:
  curl http://localhost:8000/attendance
  
  curl -X POST http://localhost:8000/attendance \\
    -H "Content-Type: application/json" \\
    -d '{
      "student_id": "alice",
      "activity_id": "chess",
      "attended": true,
      "date_assigned": "2024-06-02",
      "notes": "Great participation"
    }'

🎨 CUSTOMIZATION POINTS
━━━━━━━━━━━━━━━━━━━━━

After generation, customize with:

1. VALIDATORS - Add business logic
   @validator('score')
   def validate_score(cls, v):
       if v < 0 or v > 100:
           raise ValueError('Score must be 0-100')
       return v

2. INDEXES - Speed up queries
   attendance_collection.create_index("student_id")
   attendance_collection.create_index("activity_id")

3. PERMISSIONS - Restrict access
   @router.get("/")
   def list_items(user=Depends(get_current_user)):
       if not user.is_admin:
           raise HTTPException(status_code=403)

4. CUSTOM QUERIES - Add special operations
   @router.get("/student/{student_id}/records")
   def get_student_records(student_id: str):
       return repository.find_by_student(student_id)

5. TESTS - Verify functionality
   pytest tests/test_attendance.py -v

🔑 KEY FEATURES
━━━━━━━━━━━━━

✓ Automatic CRUD generation        ✓ Type-safe validation
✓ Pagination support               ✓ MongoDB ObjectId handling
✓ Error handling                   ✓ Auto-generated API docs
✓ Timestamp management             ✓ Test templates
✓ Consistent project structure     ✓ Integration ready

⚡ FIELD TYPES SUPPORTED
━━━━━━━━━━━━━━━━━━━━

str              String values
int              Integer numbers
float            Decimal numbers
bool             True/False
datetime         Date and time
date             Date only
list             Arrays/Lists
dict             Objects/Dictionaries

Example: student_name:str, gpa:float, attended:bool

📖 DOCUMENTATION FILES
━━━━━━━━━━━━━━━━━━
.github/skills/fastapi-route-scaffolding/

- SKILL.md       Main documentation with examples
- USAGE.md       Practical usage guide
- TECHNICAL.md  Architecture and implementation
- README.md     Overview
- examples/     Working code examples

🤖 RUNNING SCRIPT MANUALLY
━━━━━━━━━━━━━━━━━━━━━━━

If needed, run scaffolder directly:

python .github/skills/fastapi-route-scaffolding/scripts/route_scaffolder.py \\
  --name attendance \\
  --fields "student_id:str,activity_id:str,attended:bool,date_assigned:str"

Output shows all generated code!

✅ INTEGRATION CHECKLIST
━━━━━━━━━━━━━━━━━━━━

- [ ] Create src/backend/models/{module}.py
- [ ] Create src/backend/repositories/{module}.py
- [ ] Create src/backend/routers/{module}.py
- [ ] Add collection to src/backend/database.py
- [ ] Import and register router in src/app.py
- [ ] Run: python -m uvicorn src.app:app --reload
- [ ] Test endpoints at http://localhost:8000/docs
- [ ] Create tests/test_{module}.py
- [ ] Add custom validators
- [ ] Add permissions if needed

🎯 COMMON PATTERNS
━━━━━━━━━━━━━━━

FILTERING:
  @router.get("/")
  def list_items(
      skip: int = Query(0),
      limit: int = Query(10),
      status: Optional[str] = None
  ):
      ...

SEARCHING:
  @router.get("/search")
  def search(q: str = Query(...)):
      ...

RELATIONSHIPS:
  @router.get("/student/{student_id}/grades")
  def get_student_grades(student_id: str):
      ...

BULK OPERATIONS:
  @router.post("/bulk")
  def bulk_create(items: List[ItemCreate]):
      ...

📚 LEARNING RESOURCES
━━━━━━━━━━━━━━━━━

FastAPI:    https://fastapi.tiangolo.com/
Pydantic:   https://docs.pydantic.dev/
PyMongo:    https://pymongo.readthedocs.io/
MongoDB:    https://docs.mongodb.com/

🐛 TROUBLESHOOTING
━━━━━━━━━━━━━━

Q: Import errors after generation?
A: Ensure __init__.py exists in models/, repositories/, routers/

Q: Collection not found at runtime?
A: Verify collection initialized in database.py

Q: Tests fail with validation errors?
A: Check Pydantic model field types match expected data

Q: Routes not available?
A: Confirm router imported and registered in app.py

Q: Script not generating code?
A: Ensure Python 3.7+, correct field syntax

💡 TIPS
━━━━━━

• Always add custom validators for business rules
• Create database indexes on frequently queried fields
• Use pagination on list endpoints
• Write tests for critical paths
• Document domain-specific endpoints
• Keep models focused on single resources
• Use repositories for data access, not routers
• Validate input at every layer

🚀 GET STARTED NOW
━━━━━━━━━━━━━━━

1. Ask Copilot: "Create a student profiles API"
2. Review generated code
3. Customize with your business logic
4. Test with curl or Postman
5. Deploy!

═══════════════════════════════════════════════════════════════════════════════

For detailed documentation, see: .github/skills/fastapi-route-scaffolding/SKILL.md
""")

if __name__ == "__main__":
    pass
