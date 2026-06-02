"""
Example: Generated FastAPI router for grades management

This file shows what the route_scaffolder.py script generates
for API endpoints when creating a grades module.

To reproduce this output, run:
    python scripts/route_scaffolder.py --name grades

Integration with app.py:
    1. Add to imports: from .backend.routers import grades
    2. Add after other routers: app.include_router(grades.router)
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional, List

from ..database import grades_collection
from ..repositories.grades import GradesRepository
from ..models.grades import GradeCreate, GradeUpdate, GradeResponse

router = APIRouter(
    prefix="/grades",
    tags=["grades"]
)

repository = GradesRepository()


@router.get("", response_model=List[Dict[str, Any]])
def list_grades(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return")
) -> List[Dict[str, Any]]:
    """Get all grades with pagination"""
    try:
        return repository.find_all(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve grades: {str(e)}")


@router.post("", response_model=Dict[str, Any], status_code=201)
def create_grade(item: GradeCreate) -> Dict[str, Any]:
    """Create a new grade"""
    try:
        return repository.create(item.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create grade: {str(e)}")


@router.get("/{grade_id}", response_model=Dict[str, Any])
def get_grade(grade_id: str) -> Dict[str, Any]:
    """Get a specific grade by ID"""
    try:
        item = repository.find_by_id(grade_id)
        if not item:
            raise HTTPException(
                status_code=404,
                detail=f"Grade with ID {grade_id} not found"
            )
        return item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve grade: {str(e)}")


@router.put("/{grade_id}", response_model=Dict[str, Any])
def update_grade(
    grade_id: str,
    item: GradeUpdate
) -> Dict[str, Any]:
    """Update a grade by ID"""
    try:
        updated_item = repository.update(grade_id, item.dict(exclude_unset=True))
        if not updated_item:
            raise HTTPException(
                status_code=404,
                detail=f"Grade with ID {grade_id} not found"
            )
        return updated_item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update grade: {str(e)}")


@router.delete("/{grade_id}", status_code=204)
def delete_grade(grade_id: str) -> None:
    """Delete a grade by ID"""
    try:
        if not repository.delete(grade_id):
            raise HTTPException(
                status_code=404,
                detail=f"Grade with ID {grade_id} not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete grade: {str(e)}")


# Custom endpoints specific to grades

@router.get("/student/{student_id}", response_model=List[Dict[str, Any]])
def get_grades_by_student(student_id: str) -> List[Dict[str, Any]]:
    """Get all grades for a specific student"""
    try:
        grades = repository.find_by_student(student_id)
        if not grades:
            raise HTTPException(
                status_code=404,
                detail=f"No grades found for student {student_id}"
            )
        return grades
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve student grades: {str(e)}")


@router.get("/activity/{activity_id}", response_model=List[Dict[str, Any]])
def get_grades_by_activity(activity_id: str) -> List[Dict[str, Any]]:
    """Get all grades for a specific activity"""
    try:
        grades = repository.find_by_activity(activity_id)
        if not grades:
            raise HTTPException(
                status_code=404,
                detail=f"No grades found for activity {activity_id}"
            )
        return grades
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve activity grades: {str(e)}")


@router.get("/student/{student_id}/average", response_model=Dict[str, Any])
def get_student_average(student_id: str) -> Dict[str, Any]:
    """Get average grade for a student"""
    try:
        avg_score = repository.get_average_score(student_id)
        return {
            "student_id": student_id,
            "average_score": avg_score,
            "total_grades": len(repository.find_by_student(student_id))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate average: {str(e)}")
