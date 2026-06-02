"""
Example: Generated models for grades management

This file shows what the route_scaffolder.py script generates
when requested to create a grades module.

To reproduce this output, run:
    python scripts/route_scaffolder.py --name grades --fields "student_id:str,activity_id:str,score:int,date_assigned:str"
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class GradeCreate(BaseModel):
    """Model for creating a new grade"""
    student_id: str = Field(..., description="student_id")
    activity_id: str = Field(..., description="activity_id")
    score: int = Field(..., description="score")
    date_assigned: str = Field(..., description="date_assigned")


class GradeUpdate(BaseModel):
    """Model for updating a grade"""
    student_id: Optional[str] = Field(None, description="student_id")
    activity_id: Optional[str] = Field(None, description="activity_id")
    score: Optional[int] = Field(None, description="score")
    date_assigned: Optional[str] = Field(None, description="date_assigned")


class GradeResponse(GradeCreate):
    """Model for grade responses"""
    id: str = Field(..., description="Unique identifier")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        """Pydantic config"""
        json_schema_extra = {
            "example": {
                "id": "65a1b2c3d4e5f6g7h8i9j0k1",
                "student_id": "example",
                "activity_id": "example",
                "score": "example",
                "date_assigned": "example"
            }
        }
