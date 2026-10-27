"""Operacje na kolekcji użytkownika."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlmodel import Session, desc, select

from app.models import (
    AddToCollectionRequest, CarSchema, CollectionItemSchema, Variant,
    VariantSchema, UserCollection, get_db,
)

router = APIRouter()

@router.post("/collection", response_model=CollectionItemSchema)
async def add_to_collection(
    request: AddToCollectionRequest,
    db: Session = Depends(get_db)
):
    """
    Add a variant to the user's collection.
    Sprawdza czy użytkownik już ma ten wariant (zapobiega duplikatom).
    """
    statement = select(Variant).where(Variant.id == request.variant_id)
    variant = db.exec(statement).first()

    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")

    existing_collection = select(UserCollection).where(
        UserCollection.variant_id == request.variant_id
    ).options(
        selectinload(UserCollection.variant).selectinload(Variant.car)
    )
    existing_item = db.exec(existing_collection).first()

    if existing_item:
        return CollectionItemSchema(
            id=existing_item.id,
            variant_id=existing_item.variant_id,
            added_at=existing_item.added_at,
            variant=VariantSchema.model_validate(existing_item.variant.model_dump()),
            car=CarSchema.model_validate(existing_item.variant.car.model_dump())
        )

    collection_item = UserCollection(variant_id=request.variant_id)
    db.add(collection_item)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        existing_item = db.exec(existing_collection).first()
        if existing_item:
            return CollectionItemSchema(
                id=existing_item.id,
                variant_id=existing_item.variant_id,
                added_at=existing_item.added_at,
                variant=VariantSchema.model_validate(existing_item.variant.model_dump()),
                car=CarSchema.model_validate(existing_item.variant.car.model_dump())
            )
        raise HTTPException(status_code=500, detail="Could not save collection item")

    created_item = db.exec(
        select(UserCollection).where(UserCollection.id == collection_item.id).options(
            selectinload(UserCollection.variant).selectinload(Variant.car)
        )
    ).first()
    if not created_item or not created_item.variant:
        raise HTTPException(status_code=500, detail="Could not load collection item")

    result = CollectionItemSchema(
        id=created_item.id,
        variant_id=created_item.variant_id,
        added_at=created_item.added_at,
        variant=VariantSchema.model_validate(created_item.variant.model_dump()),
        car=CarSchema.model_validate(created_item.variant.car.model_dump())
    )

    return result

@router.get("/collection", response_model=List[CollectionItemSchema])
async def get_collection(
    db: Session = Depends(get_db),
    limit: int = 200,
    offset: int = 0
):
    """
    Get all items in the user's collection.
    """
    statement = (
        select(UserCollection)
        .order_by(desc(UserCollection.added_at))
        .offset(offset)
        .limit(limit)
        .options(selectinload(UserCollection.variant).selectinload(Variant.car))
    )
    collection_items = db.exec(statement).all()

    result = []
    for item in collection_items:
        variant = item.variant
        if not variant:
            continue
        car = variant.car
        result.append(CollectionItemSchema(
            id=item.id,
            variant_id=item.variant_id,
            added_at=item.added_at,
            variant=VariantSchema.model_validate(variant.model_dump()),
            car=CarSchema.model_validate(car.model_dump()) if car else None
        ))

    return result
