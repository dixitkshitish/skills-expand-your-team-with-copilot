# FastAPI Route and MongoDB Model Scaffolding Skill

## Overview

This is a **GitHub Copilot Agent Skill** that automates the creation of FastAPI routes, Pydantic data models, and MongoDB repository code for the Mergington High School Management System.

When you ask Copilot to create a new API feature, this skill generates a complete, production-ready scaffolding that follows project conventions and best practices.

## 📁 Folder Structure

```
fastapi-route-scaffolding/
├── SKILL.md                          # Main skill documentation
├── USAGE.md                          # Usage guide and examples  
├── TECHNICAL.md                      # Technical reference for developers
├── README.md                         # This file
├── scripts/
│   └── route_scaffolder.py          # The scaffolding generation script
└── examples/
    ├── README.md                    # How to use examples
    ├── grades_models_example.py     # Example generated Pydantic models
    ├── grades_repository_example.py # Example generated repository
    └── grades_router_example.py     # Example generated router
```

## 🎯 Purpose

Creating a new FastAPI feature requires writing several interconnected components:
- **Pydantic models** for request/response validation
- **MongoDB repository** with database operations
- **FastAPI router** with HTTP endpoints
- **Proper error handling** and status codes
- **Type hints** for IDE support and documentation

This skill automates the scaffolding, ensuring consistency and dramatically reducing boilerplate code.

## ⚡ Quick Start

### For Users

1. **Ask Copilot to create a new route**:
   ```
   Can you create an API endpoint for managing student attendance?
   Include fields: student_id, activity_id, attended (boolean), date, and notes.
   ```

2. **Copilot will**:
   - Generate Pydantic validation models
   - Create MongoDB repository code
   - Create FastAPI router with endpoints
   - Provide integration instructions
   - Write test templates

3. **You customize**:
   - Add business logic and validators
   - Integrate authentication if needed
   - Write comprehensive tests
   - Deploy!

### For Copilot Agents

The scaffolding script can be run directly:

```bash
python .github/skills/fastapi-route-scaffolding/scripts/route_scaffolder.py \
  --name attendance \
  --fields "student_id:str,activity_id:str,attended:bool,date:str,notes:str"
```

## 📚 Documentation Structure

| Document | Purpose | Audience |
|----------|---------|----------|
| **SKILL.md** | Main skill documentation with examples | Everyone |
| **USAGE.md** | Practical guide with use cases | Developers & Copilot |
| **TECHNICAL.md** | Architecture and implementation details | Developers & Copilot agents |
| **examples/README.md** | How to use code examples | Developers |

## ✨ Key Features

✅ **Consistent Project Structure** - Maintains the project's directory layout  
✅ **Automatic Error Handling** - Proper HTTP status codes and error responses  
✅ **Type Safety** - Full Pydantic validation and type hints  
✅ **MongoDB Integration** - Handles ObjectId conversion and collections  
✅ **FastAPI Best Practices** - Clear documentation, proper status codes, validation  
✅ **Test Templates** - Unit test skeleton for new features  
✅ **Fully Customizable** - Generated code is easily extended with business logic  

## 🚀 Example Output

When you request "Create a grades API", the skill generates:

**1. Pydantic Models** (`models/grades.py`)
```python
class GradeCreate(BaseModel):
    student_id: str
    activity_id: str
    score: int
    date_assigned: str

class GradeUpdate(BaseModel):
    # Optional fields for updates

class GradeResponse(GradeCreate):
    id: str
    created_at: datetime
```

**2. Repository Layer** (`repositories/grades.py`)
```python
class GradesRepository:
    def find_all(self, skip=0, limit=10) -> List[Dict]:
    def find_by_id(self, grade_id: str) -> Dict:
    def create(self, data: Dict) -> Dict:
    def update(self, grade_id: str, data: Dict) -> Dict:
    def delete(self, grade_id: str) -> bool:
```

**3. API Routes** (`routers/grades.py`)
```python
@router.get("/grades")
def list_grades(skip: int = 0, limit: int = 10):

@router.post("/grades", status_code=201)
def create_grade(grade: GradeCreate):

@router.get("/grades/{grade_id}")
def get_grade(grade_id: str):

@router.put("/grades/{grade_id}")
def update_grade(grade_id: str, grade: GradeUpdate):

@router.delete("/grades/{grade_id}", status_code=204)
def delete_grade(grade_id: str):
```

## 🔧 How It Works

1. **Copilot reads this skill** to understand conventions
2. **Copilot parses your request** to extract module name and fields
3. **Copilot runs the script** to generate code templates
4. **Copilot creates the necessary files** with generated code
5. **Copilot provides integration instructions** for app.py and database.py
6. **You customize the generated code** with business logic

## 📝 Naming Conventions

| Component | Pattern | Example |
|-----------|---------|---------|
| Module Name | plural_snake_case | `attendance_records` |
| Router Class | PascalCase | `class GradesRepository` |
| Route Prefix | /module | `/attendance_records` |
| Parameter | {singular_id} | `/{grade_id}` |

## 🛠️ How Copilot Uses This Skill

When Copilot encounters a request to create a new API route:

1. **Matches intent** - Recognizes the request falls under "create new API feature"
2. **Reads SKILL.md** - Understands the project's API conventions
3. **Parses requirements** - Extracts module name and fields from your request
4. **Generates code** - Runs `route_scaffolder.py` with your specifications
5. **Creates files** - Places generated code in correct directories
6. **Updates integrations** - Modifies app.py and database.py
7. **Provides guidance** - Explains next steps and customization points

## 📋 Use Cases

This skill is ideal for:

✅ Creating new API modules for features  
✅ Adding CRUD operations for new resources  
✅ Rapidly prototyping backend APIs  
✅ Maintaining code consistency across the project  
✅ Enforcing best practices in code structure  

## ❌ When NOT to Use

❌ Modifying existing small endpoints  
❌ Fixing bugs in existing code  
❌ Creating complex business logic (after scaffolding, yes!)  
❌ Non-standard API patterns  

## 🔗 Integration

After generation, integrate the new route by updating:

**1. `src/app.py`**
```python
from .backend.routers import attendance_records
app.include_router(attendance_records.router)
```

**2. `src/backend/database.py`**
```python
attendance_records_collection = db['attendance_records']
```

## 📖 Script Reference

The scaffolding script (`scripts/route_scaffolder.py`) is a standalone Python utility:

```bash
# Basic usage
python scripts/route_scaffolder.py --name students

# With fields
python scripts/route_scaffolder.py \
  --name grades \
  --fields "student_id:str,score:int,date:str"

# Output to directory
python scripts/route_scaffolder.py \
  --name reports \
  --output ./generated \
  --all
```

## 🎓 Examples

See `examples/` folder for:
- **grades_models_example.py** - Generated Pydantic models
- **grades_repository_example.py** - Generated repository code
- **grades_router_example.py** - Generated API endpoints

Run the script yourself to see more examples:
```bash
python scripts/route_scaffolder.py --name your_module --fields "field1:str,field2:int"
```

## 🚦 Status Codes Generated

The scaffolded endpoints return proper HTTP status codes:

| Method | Status | Meaning |
|--------|--------|---------|
| GET | 200 | Success |
| POST | 201 | Created |
| PUT | 200 | Updated |
| DELETE | 204 | Deleted (no content) |
| Error | 400 | Bad request |
| Error | 404 | Not found |
| Error | 500 | Server error |

## 🔒 Security Notes

Generated code includes structure for:
- Input validation via Pydantic
- Error handling with safe messages
- Type checking

You should add:
- Authentication/authorization checks
- Custom validators for business rules
- Rate limiting if needed
- Audit logging for sensitive operations

## 🎯 Next Steps

1. **Try it out** - Ask Copilot to create a new route
2. **Review generated code** - See how it follows conventions
3. **Customize** - Add validators, business logic, permissions
4. **Test** - Use generated test templates
5. **Deploy** - Your new feature is ready!

## 📞 Support

For issues or questions:
1. Check [TECHNICAL.md](TECHNICAL.md) for architecture details
2. Review [USAGE.md](USAGE.md) for practical examples
3. See [examples/README.md](examples/README.md) for working code
4. Check [SKILL.md](SKILL.md) for comprehensive documentation

## 🤝 Contributing

To improve this skill:
1. Edit `scripts/route_scaffolder.py`
2. Add new field types, query patterns, or endpoints
3. Update documentation to reflect changes
4. Test with Copilot

## 📄 License

This skill is part of the Mergington High School Management System project.

---

**Created:** June 2024  
**Version:** 1.0  
**Status:** Production-Ready  

For the latest updates, see the GitHub repository.
