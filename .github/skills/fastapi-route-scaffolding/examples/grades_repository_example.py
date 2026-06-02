"""
Example: Generated repository for grades management

This file shows what the route_scaffolder.py script generates
for database access layer when creating a grades module.

To reproduce this output, run:
    python scripts/route_scaffolder.py --name grades
"""

from typing import Dict, Any, Optional, List
from ..database import grades_collection
from bson import ObjectId


class GradesRepository:
    """Data access layer for grades"""
    
    def find_all(self, skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
        """Get all grades with pagination"""
        results = []
        for item in grades_collection.find().skip(skip).limit(limit):
            item["_id"] = str(item["_id"])
            results.append(item)
        return results
    
    def find_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Get grade by ID"""
        try:
            item = grades_collection.find_one({"_id": ObjectId(item_id)})
            if item:
                item["_id"] = str(item["_id"])
            return item
        except Exception:
            return None
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new grade"""
        from datetime import datetime
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()
        result = grades_collection.insert_one(data)
        data["_id"] = str(result.inserted_id)
        return data
    
    def update(self, item_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a grade"""
        from datetime import datetime
        data["updated_at"] = datetime.utcnow()
        try:
            result = grades_collection.update_one(
                {"_id": ObjectId(item_id)},
                {"$set": data}
            )
            if result.matched_count > 0:
                return self.find_by_id(item_id)
            return None
        except Exception:
            return None
    
    def delete(self, item_id: str) -> bool:
        """Delete a grade"""
        try:
            result = grades_collection.delete_one({"_id": ObjectId(item_id)})
            return result.deleted_count > 0
        except Exception:
            return False
    
    def count(self) -> int:
        """Get total count of grades"""
        return grades_collection.count_documents({})
    
    # Custom repository methods for grades-specific queries
    
    def find_by_student(self, student_id: str) -> List[Dict[str, Any]]:
        """Find all grades for a specific student"""
        results = []
        for item in grades_collection.find({"student_id": student_id}):
            item["_id"] = str(item["_id"])
            results.append(item)
        return results
    
    def find_by_activity(self, activity_id: str) -> List[Dict[str, Any]]:
        """Find all grades for a specific activity"""
        results = []
        for item in grades_collection.find({"activity_id": activity_id}):
            item["_id"] = str(item["_id"])
            results.append(item)
        return results
    
    def find_by_score_range(self, min_score: int, max_score: int) -> List[Dict[str, Any]]:
        """Find grades within a score range"""
        results = []
        for item in grades_collection.find({
            "score": {"$gte": min_score, "$lte": max_score}
        }):
            item["_id"] = str(item["_id"])
            results.append(item)
        return results
    
    def get_average_score(self, student_id: str) -> float:
        """Calculate average score for a student"""
        pipeline = [
            {"$match": {"student_id": student_id}},
            {"$group": {"_id": None, "avg_score": {"$avg": "$score"}}}
        ]
        result = list(grades_collection.aggregate(pipeline))
        return result[0]["avg_score"] if result else 0.0
