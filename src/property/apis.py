from fastapi import APIRouter, status, HTTPException, Path, Depends
from src.property.models import PropertyRequest
from src.database import engine
from src.property.models import Property
import src.property.models as property_models
from src.database import db_context
from typing import Annotated
from src.property.router import PropertyRouter

property_models.Base.metadata.create_all(bind=engine)


@PropertyRouter.get("", status_code=status.HTTP_200_OK)
async def all_Property(db: db_context):
    return db.query(Property).all()


@PropertyRouter.post("", status_code=status.HTTP_201_CREATED)
async def create_property(db: db_context, data: PropertyRequest):
    property = Property(**data.dict())
    db.add(property)
    db.commit()
    db.refresh(property)
    return property


@PropertyRouter.get("/{property_id}", status_code=status.HTTP_200_OK)
async def get_property(db: db_context, property_id: int = Path(...)):
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    return property


@PropertyRouter.put("/{property_id}", status_code=status.HTTP_200_OK)
async def update_property(
    db: db_context,
    property_id: int,
    data: PropertyRequest,
):
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")

    for key, value in data.dict().items():
        setattr(property, key, value)

    db.commit()
    db.refresh(property)
    return property


@PropertyRouter.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_property(db: db_context, property_id: int):
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")

    db.delete(property)
    db.commit()
    return None
