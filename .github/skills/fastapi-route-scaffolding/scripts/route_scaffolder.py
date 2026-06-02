#!/usr/bin/env python3
"""
FastAPI Route and MongoDB Model Scaffolding Script

This script generates FastAPI routers, Pydantic models, and MongoDB repositories
based on user specifications. It can be used by Copilot to automatically create
new API endpoints following project conventions.

Usage:
    python route_scaffolder.py --name activities --fields id:str,name:str,description:str
    python route_scaffolder.py --name grades --interactive
    python route_scaffolder.py --config grades_config.json
"""

import json
import sys
import os
from typing import Dict, List, Optional, Any
from pathlib import Path
import argparse
from datetime import datetime


class RouteScaffolder:
    """Generates FastAPI route scaffolding code"""
    
    def __init__(self, module_name: str):
        """
        Initialize scaffolder
        
        Args:
            module_name: Name of the module (e.g., 'grades', 'reports')
        """
        self.module_name = module_name
        self.module_singular = self._singularize(module_name)
        self.collection_name = f"{module_name}_collection"
        self.fields: Dict[str, str] = {}
        
    def _singularize(self, word: str) -> str:
        """Simple singularization - remove 's' if plural"""
        if word.endswith('ies'):
            return word[:-3] + 'y'
        elif word.endswith('s'):
            return word[:-1]
        return word
    
    def add_field(self, field_name: str, field_type: str, required: bool = True) -> None:
        """Add a field to the model"""
        self.fields[field_name] = {
            'type': field_type,
            'required': required
        }
    
    def generate_model(self) -> str:
        """Generate Pydantic model file content"""
        class_name = ''.join(word.capitalize() for word in self.module_name.split('_'))
        create_class = f"{class_name}Create"
        update_class = f"{class_name}Update"
        response_class = f"{class_name}Response"
        
        # Build create model fields
        create_fields = []
        for field_name, field_info in self.fields.items():
            if field_name == 'id' or field_name == '_id':
                continue  # Skip ID fields, they're auto-generated
            
            field_type = field_info['type']
            required = field_info['required']
            
            if required:
                create_fields.append(f"    {field_name}: {field_type} = Field(..., "
                                   f"description=\"{field_name}\")")
            else:
                create_fields.append(f"    {field_name}: Optional[{field_type}] = Field(None, "
                                   f"description=\"{field_name}\")")
        
        # Build update model fields (all optional)
        update_fields = []
        for field_name, field_info in self.fields.items():
            if field_name == 'id' or field_name == '_id':
                continue
            
            field_type = field_info['type']
            update_fields.append(f"    {field_name}: Optional[{field_type}] = Field(None, "
                               f"description=\"{field_name}\")")
        
        code = f'''from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class {create_class}(BaseModel):
    """Model for creating a new {self.module_singular}"""
{chr(10).join(create_fields)}


class {update_class}(BaseModel):
    """Model for updating a {self.module_singular}"""
{chr(10).join(update_fields)}


class {response_class}({create_class}):
    """Model for {self.module_singular} responses"""
    id: str = Field(..., description="Unique identifier")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        """Pydantic config"""
        json_schema_extra = {{
            "example": {{
                "id": "65a1b2c3d4e5f6g7h8i9j0k1",
{chr(10).join([f"                \"{k}\": \"example\"," for k in self.fields.keys() if k not in ['id', '_id']])[:-1]}
            }}
        }}
'''
        return code
    
    def generate_repository(self) -> str:
        """Generate repository class for database operations"""
        class_name = ''.join(word.capitalize() for word in self.module_name.split('_'))
        repo_name = f"{class_name}Repository"
        
        code = f'''from typing import Dict, Any, Optional, List
from ..database import {self.collection_name}
from bson import ObjectId


class {repo_name}:
    """Data access layer for {self.module_name}"""
    
    def find_all(self, skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
        """Get all {self.module_name} with pagination"""
        results = []
        for item in {self.collection_name}.find().skip(skip).limit(limit):
            item["_id"] = str(item["_id"])
            results.append(item)
        return results
    
    def find_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Get {self.module_singular} by ID"""
        try:
            item = {self.collection_name}.find_one({{"_id": ObjectId(item_id)}})
            if item:
                item["_id"] = str(item["_id"])
            return item
        except Exception:
            return None
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new {self.module_singular}"""
        from datetime import datetime
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()
        result = {self.collection_name}.insert_one(data)
        data["_id"] = str(result.inserted_id)
        return data
    
    def update(self, item_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a {self.module_singular}}"""
        from datetime import datetime
        data["updated_at"] = datetime.utcnow()
        try:
            result = {self.collection_name}.update_one(
                {{"_id": ObjectId(item_id)}},
                {{"$set": data}}
            )
            if result.matched_count > 0:
                return self.find_by_id(item_id)
            return None
        except Exception:
            return None
    
    def delete(self, item_id: str) -> bool:
        """Delete a {self.module_singular}}"""
        try:
            result = {self.collection_name}.delete_one({{"_id": ObjectId(item_id)}})
            return result.deleted_count > 0
        except Exception:
            return False
    
    def count(self) -> int:
        """Get total count of {self.module_name}"""
        return {self.collection_name}.count_documents({{}})
'''
        return code
    
    def generate_router(self) -> str:
        """Generate FastAPI router file"""
        class_name = ''.join(word.capitalize() for word in self.module_name.split('_'))
        repo_class = f"{class_name}Repository"
        create_model = f"{class_name}Create"
        update_model = f"{class_name}Update"
        response_model = f"{class_name}Response"
        
        code = f'''"""
API endpoints for {self.module_name} management
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional, List

from ..database import {self.collection_name}
from ..repositories.{self.module_name} import {repo_class}
from ..models.{self.module_name} import {create_model}, {update_model}, {response_model}

router = APIRouter(
    prefix="/{self.module_name}",
    tags=["{self.module_name}"]
)

repository = {repo_class}()


@router.get("", response_model=List[Dict[str, Any]])
def list_{self.module_name}(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return")
) -> List[Dict[str, Any]]:
    """Get all {self.module_name} with pagination"""
    try:
        return repository.find_all(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve {self.module_name}: {{str(e)}}")


@router.post("", response_model=Dict[str, Any], status_code=201)
def create_{self.module_singular}(item: {create_model}) -> Dict[str, Any]:
    """Create a new {self.module_singular}}"""
    try:
        return repository.create(item.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create {self.module_singular}: {{str(e)}}")


@router.get("/{{{self.module_singular}_id}}", response_model=Dict[str, Any])
def get_{self.module_singular}({self.module_singular}_id: str) -> Dict[str, Any]:
    """Get a specific {self.module_singular}} by ID"""
    try:
        item = repository.find_by_id({self.module_singular}_id)
        if not item:
            raise HTTPException(
                status_code=404,
                detail=f"{class_name} with ID {{{self.module_singular}_id}} not found"
            )
        return item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve {self.module_singular}: {{str(e)}}")


@router.put("/{{{self.module_singular}_id}}", response_model=Dict[str, Any])
def update_{self.module_singular}(
    {self.module_singular}_id: str,
    item: {update_model}
) -> Dict[str, Any]:
    """Update a {self.module_singular}} by ID"""
    try:
        updated_item = repository.update({self.module_singular}_id, item.dict(exclude_unset=True))
        if not updated_item:
            raise HTTPException(
                status_code=404,
                detail=f"{class_name} with ID {{{self.module_singular}_id}} not found"
            )
        return updated_item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update {self.module_singular}: {{str(e)}}")


@router.delete("/{{{self.module_singular}_id}}", status_code=204)
def delete_{self.module_singular}({self.module_singular}_id: str) -> None:
    """Delete a {self.module_singular}} by ID"""
    try:
        if not repository.delete({self.module_singular}_id):
            raise HTTPException(
                status_code=404,
                detail=f"{class_name} with ID {{{self.module_singular}_id}} not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete {self.module_singular}: {{str(e)}}")
'''
        return code
    
    def generate_app_integration(self) -> str:
        """Generate code to add to app.py"""
        code = f"""# Add to src/app.py in the imports section:
from .backend.routers import {self.module_name}

# Add to src/app.py after other app.include_router() calls:
app.include_router({self.module_name}.router)
"""
        return code
    
    def generate_database_init(self) -> str:
        """Generate code to add to database.py"""
        class_name = ''.join(word.capitalize() for word in self.module_name.split('_'))
        
        code = f"""# Add to src/backend/database.py in the collections section:
{self.collection_name} = db['{self.module_name}']

# Add to src/backend/database.py in the init_database() function:
# Initialize {self.module_name} if empty
if {self.collection_name}.count_documents({{}}) == 0:
    # Add initial {self.module_name} data here if needed
    pass

# Create indexes for common queries (optional but recommended):
# {self.collection_name}.create_index("created_at")
# {self.collection_name}.create_index([("type", 1), ("status", 1)])
"""
        return code
    
    def generate_test_template(self) -> str:
        """Generate unit test template"""
        class_name = ''.join(word.capitalize() for word in self.module_name.split('_'))
        
        code = f'''import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


class Test{class_name}:
    """Tests for {self.module_name} endpoints"""
    
    def test_list_{self.module_name}(self):
        """Test listing all {self.module_name}"""
        response = client.get("/{self.module_name}")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_create_{self.module_singular}(self):
        """Test creating a new {self.module_singular}}"""
        {self.module_singular}_data = {{
            # Add fields from your {class_name}Create model
        }}
        response = client.post("/{self.module_name}", json={self.module_singular}_data)
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        return data["id"]
    
    def test_get_{self.module_singular}(self):
        """Test getting a single {self.module_singular}}"""
        # First create a {self.module_singular}
        {self.module_singular}_id = self.test_create_{self.module_singular}()
        
        response = client.get(f"/{self.module_name}/{{self.module_singular}_id}}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == {self.module_singular}_id
    
    def test_update_{self.module_singular}(self):
        """Test updating a {self.module_singular}}"""
        {self.module_singular}_id = self.test_create_{self.module_singular}()
        
        update_data = {{
            # Add fields you want to update
        }}
        response = client.put(f"/{self.module_name}/{{self.module_singular}_id}}", json=update_data)
        assert response.status_code == 200
    
    def test_delete_{self.module_singular}(self):
        """Test deleting a {self.module_singular}}"""
        {self.module_singular}_id = self.test_create_{self.module_singular}()
        
        response = client.delete(f"/{self.module_name}/{{self.module_singular}_id}}")
        assert response.status_code == 204
        
        # Verify it's deleted
        response = client.get(f"/{self.module_name}/{{self.module_singular}_id}}")
        assert response.status_code == 404
'''
        return code


def main():
    """Main entry point for the scaffolder"""
    parser = argparse.ArgumentParser(
        description="Generate FastAPI route scaffolding code"
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Module name (e.g., 'grades', 'reports')"
    )
    parser.add_argument(
        "--fields",
        help="Comma-separated field definitions (e.g., 'score:int,date:str,notes:str')"
    )
    parser.add_argument(
        "--output",
        default=".",
        help="Output directory for generated files"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate all files (models, repository, router, tests)"
    )
    
    args = parser.parse_args()
    
    # Create scaffolder
    scaffolder = RouteScaffolder(args.name)
    
    # Parse fields if provided
    if args.fields:
        for field_def in args.fields.split(','):
            parts = field_def.strip().split(':')
            if len(parts) == 2:
                field_name, field_type = parts
                scaffolder.add_field(field_name.strip(), field_type.strip())
    else:
        # Default fields
        scaffolder.add_field("name", "str", required=True)
        scaffolder.add_field("description", "str", required=False)
    
    # Generate and print all code
    print("=" * 80)
    print(f"FASTAPI ROUTE SCAFFOLDING FOR: {args.name}")
    print("=" * 80)
    
    print("\n### PYDANTIC MODELS (models/{}.py) ###\n".format(args.name))
    print(scaffolder.generate_model())
    
    print("\n### REPOSITORY CLASS (repositories/{}.py) ###\n".format(args.name))
    print(scaffolder.generate_repository())
    
    print("\n### FASTAPI ROUTER (routers/{}.py) ###\n".format(args.name))
    print(scaffolder.generate_router())
    
    print("\n### INTEGRATION STEPS ###\n")
    print(scaffolder.generate_app_integration())
    
    print("\n### DATABASE INITIALIZATION ###\n")
    print(scaffolder.generate_database_init())
    
    print("\n### TEST TEMPLATE (tests/test_{}.py) ###\n".format(args.name))
    print(scaffolder.generate_test_template())
    
    print("\n" + "=" * 80)
    print("CODE GENERATION COMPLETE")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Create models/{}.py with the Pydantic models above".format(args.name))
    print("2. Create repositories/{}.py with the repository class".format(args.name))
    print("3. Create routers/{}.py with the router endpoints".format(args.name))
    print("4. Update database.py with the collection initialization")
    print("5. Update app.py with the router import and include_router() call")
    print("6. Create tests/test_{}.py with the test template".format(args.name))
    print("7. Customize validators and business logic in models and repositories")
    print("8. Run tests: pytest tests/test_{}.py".format(args.name))


if __name__ == "__main__":
    main()
