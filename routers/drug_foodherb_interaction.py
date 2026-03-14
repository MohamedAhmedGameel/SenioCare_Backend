from fastapi import APIRouter, HTTPException
from typing import Any, Dict, List, Optional
from bson import ObjectId
from database import get_ai_db
from schemas.drug_foodherb_interaction import DrugFoodHerbInteractionCreate, DrugFoodHerbInteractionUpdate, DrugFoodHerbInteraction, DeleteResponse
from utils.pydantic_utils import map_document

router = APIRouter()

@router.post("/", status_code=201, response_model=DrugFoodHerbInteraction)
async def create_interaction(interaction: DrugFoodHerbInteractionCreate):
    """Create a new drug-food/herb interaction record"""
    db = get_ai_db()
    interaction_dict = interaction.model_dump(exclude_unset=True)
    result = await db.drug_foodherb_interaction.insert_one(interaction_dict)
    created = await db.drug_foodherb_interaction.find_one({"_id": result.inserted_id})
    return map_document(created)

@router.get("/", response_model=List[Dict[str, Any]])
async def list_interactions(
    fhdi_drug_id: Optional[str] = None,
    food_herb_id: Optional[str] = None,
    type: Optional[str] = None,
    page: int = 1,
    limit: int = 30
):
    """List all drug-food/herb interaction records with optional filters and pagination"""
    db = get_ai_db()
    
    skip = (page - 1) * limit
    
    # Build filter query
    query = {}
    if fhdi_drug_id:
        query["fhdi_drug_id"] = fhdi_drug_id
    if food_herb_id:
        query["food_herb_id"] = food_herb_id
    if type:
        query["type"] = type
    
    # Create aggregation pipeline with lookups
    pipeline = [
        {"$match": query} if query else {"$match": {}},
        # Lookup drug information
        {
            "$lookup": {
                "from": "drug_information",
                "localField": "fhdi_drug_id",
                "foreignField": "fhdi_drug_id",
                "as": "drug_details"
            }
        },
        {
            "$unwind": {
                "path": "$drug_details",
                "preserveNullAndEmptyArrays": True
            }
        },
        # Conditional lookup for food or herb
        {
            "$lookup": {
                "from": "food_information",
                "let": {"fh_id": "$food_herb_id", "fh_type": "$type"},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$and": [
                                    {"$eq": ["$fhdi_food_id", "$$fh_id"]},
                                    {"$eq": ["$$fh_type", "food"]}
                                ]
                            }
                        }
                    }
                ],
                "as": "food_details"
            }
        },
        {
            "$lookup": {
                "from": "herb_information",
                "let": {"fh_id": "$food_herb_id", "fh_type": "$type"},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$and": [
                                    {"$eq": ["$fhdi_herb_id", "$$fh_id"]},
                                    {"$eq": ["$$fh_type", "herb"]}
                                ]
                            }
                        }
                    }
                ],
                "as": "herb_details"
            }
        },
        {
            "$addFields": {
                "food_herb_details": {
                    "$cond": {
                        "if": {"$eq": ["$type", "food"]},
                        "then": {"$arrayElemAt": ["$food_details", 0]},
                        "else": {"$arrayElemAt": ["$herb_details", 0]}
                    }
                }
            }
        },
        {
            "$project": {
                "food_details": 0,
                "herb_details": 0
            }
        },
        {"$skip": skip},
        {"$limit": limit}
    ]
    
    interactions = await db.drug_foodherb_interaction.aggregate(pipeline).to_list(length=None)
    
    for interaction in interactions:
        map_document(interaction)
        if "drug_details" in interaction and interaction["drug_details"]:
            map_document(interaction["drug_details"])
        if "food_herb_details" in interaction and interaction["food_herb_details"]:
            map_document(interaction["food_herb_details"])
    
    return interactions

@router.get("/{id}", response_model=Dict[str, Any])
async def get_interaction(id: str):
    """Get a specific drug-food/herb interaction record by ID"""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")
    
    db = get_ai_db()
    
    # Create aggregation pipeline with lookups
    pipeline = [
        {"$match": {"_id": ObjectId(id)}},
        # Lookup drug information
        {
            "$lookup": {
                "from": "drug_information",
                "localField": "fhdi_drug_id",
                "foreignField": "fhdi_drug_id",
                "as": "drug_details"
            }
        },
        {
            "$unwind": {
                "path": "$drug_details",
                "preserveNullAndEmptyArrays": True
            }
        },
        # Conditional lookup for food or herb
        {
            "$lookup": {
                "from": "food_information",
                "let": {"fh_id": "$food_herb_id", "fh_type": "$type"},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$and": [
                                    {"$eq": ["$fhdi_food_id", "$$fh_id"]},
                                    {"$eq": ["$$fh_type", "food"]}
                                ]
                            }
                        }
                    }
                ],
                "as": "food_details"
            }
        },
        {
            "$lookup": {
                "from": "herb_information",
                "let": {"fh_id": "$food_herb_id", "fh_type": "$type"},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$and": [
                                    {"$eq": ["$fhdi_herb_id", "$$fh_id"]},
                                    {"$eq": ["$$fh_type", "herb"]}
                                ]
                            }
                        }
                    }
                ],
                "as": "herb_details"
            }
        },
        {
            "$addFields": {
                "food_herb_details": {
                    "$cond": {
                        "if": {"$eq": ["$type", "food"]},
                        "then": {"$arrayElemAt": ["$food_details", 0]},
                        "else": {"$arrayElemAt": ["$herb_details", 0]}
                    }
                }
            }
        },
        {
            "$project": {
                "food_details": 0,
                "herb_details": 0
            }
        }
    ]
    
    result = await db.drug_foodherb_interaction.aggregate(pipeline).to_list(length=1)
    
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    
    interaction = result[0]
    map_document(interaction)
    if "drug_details" in interaction and interaction["drug_details"]:
        map_document(interaction["drug_details"])
    if "food_herb_details" in interaction and interaction["food_herb_details"]:
        map_document(interaction["food_herb_details"])
    
    return interaction

@router.put("/{id}", response_model=DrugFoodHerbInteraction)
async def update_interaction(id: str, interaction: DrugFoodHerbInteractionUpdate):
    """Update a drug-food/herb interaction record"""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")
    
    db = get_ai_db()
    existing = await db.drug_foodherb_interaction.find_one({"_id": ObjectId(id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Not found")
    
    updates = interaction.model_dump(exclude_unset=True)
    if updates:
        await db.drug_foodherb_interaction.update_one({"_id": ObjectId(id)}, {"$set": updates})
    
    updated = await db.drug_foodherb_interaction.find_one({"_id": ObjectId(id)})
    return map_document(updated)

@router.delete("/{id}", response_model=DeleteResponse)
async def delete_interaction(id: str):
    """Delete a drug-food/herb interaction record"""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid id")
    
    db = get_ai_db()
    result = await db.drug_foodherb_interaction.find_one_and_delete({"_id": ObjectId(id)})
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    
    return {"message": "Deleted successfully"}
