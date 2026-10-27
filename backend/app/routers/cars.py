"""Wyszukiwanie samochodów i identyfikacja wariantów."""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.matching import (
    fuzzy_ratio,
    match_variant_by_features,
    normalize_toy_number,
    parse_series_number,
)
from app.models import (
    Car, CarSchema, IdentifyResponse, Variant, VariantSchema, get_db,
)

router = APIRouter()


def build_car_response(db: Session, car_id: UUID) -> IdentifyResponse:
    car = db.exec(select(Car).where(Car.id == car_id)).first()
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    variants = db.exec(select(Variant).where(Variant.car_id == car_id)).all()
    car_data = car.model_dump()
    car_data["variants"] = [VariantSchema.model_validate(item.model_dump()) for item in variants]
    return IdentifyResponse(car=CarSchema.model_validate(car_data))


@router.get("/identify/{code}", response_model=IdentifyResponse)
async def identify_car(
    code: str,
    db: Session = Depends(get_db),
    year: Optional[int] = None,
    series: Optional[str] = None,
    color: Optional[str] = None,
    series_number: Optional[str] = None
):
    """
    Identify car by toy_number with optional variant matching.

    Optional query parameters help narrow down matching variants:
    - year: release_year (int)
    - series: series_name
    - color: body_color
    - series_number: series_number w formacie "238/250" (pozycja/całkowita)
    """
    code_normalized = normalize_toy_number(code)

    if '-' in code_normalized:
        code_normalized = code_normalized.split('-')[0]

    statement = select(Variant).where(Variant.toy_number == code_normalized)
    variants = db.exec(statement).all()

    if not variants:
        raise HTTPException(status_code=404, detail=f"Car with toy_number '{code_normalized}' not found")

    if len(variants) == 1:
        return build_car_response(db, variants[0].car_id)

    series_position = None
    series_total = None
    if series_number:
        series_position, series_total = parse_series_number(series_number)

    best_match = match_variant_by_features(
        variants, year, series, color, series_position, series_total
    )

    if best_match and best_match['score'] > 0.8:
        return build_car_response(db, best_match['variant'].car_id)

    unique_car_ids = {v.car_id for v in variants}

    if len(unique_car_ids) == 1:
        return build_car_response(db, list(unique_car_ids)[0])
    else:
        return build_car_response(db, variants[0].car_id)


@router.get("/identify/by-name", response_model=IdentifyResponse)
async def identify_by_name(
    model_name: str,
    db: Session = Depends(get_db),
    year: Optional[int] = None,
    series: Optional[str] = None,
    color: Optional[str] = None,
    series_number: Optional[str] = None
):
    """
    Identify a car by model_name (text search) with optional variant matching.
    """
    query = model_name.strip()
    if not query:
        raise HTTPException(status_code=400, detail="model_name must not be empty")

    statement = (
        select(Car)
        .where(
            (Car.model_name.ilike(f"%{query}%")) |
            (Car.page_title.ilike(f"%{query}%"))
        )
        .options(selectinload(Car.variants))
    )
    cars = db.exec(statement).all()
    if not cars:
        raise HTTPException(status_code=404, detail="No cars match model_name")

    series_position = None
    series_total = None
    if series_number:
        series_position, series_total = parse_series_number(series_number)

    best_car_id = None
    best_score = -1.0

    for car in cars:
        if not car.variants:
            continue
        variant_match = match_variant_by_features(
            car.variants, year, series, color, series_position, series_total
        )
        name_score = fuzzy_ratio(query.lower(), (car.model_name or "").lower())
        score = name_score
        if variant_match:
            score += variant_match['score']
        if score > best_score:
            best_score = score
            best_car_id = car.id

    if not best_car_id:
        best_car_id = cars[0].id

    return build_car_response(db, best_car_id)

@router.get("/cars/search", response_model=List[CarSchema])
async def search_cars(
    model_name: str,
    db: Session = Depends(get_db),
    limit: int = 50,
    offset: int = 0
):
    """
    Search cars by model_name (case-insensitive).
    """
    query = model_name.strip()
    if not query:
        raise HTTPException(status_code=400, detail="model_name must not be empty")

    statement = (
        select(Car)
        .where(Car.model_name.ilike(f"%{query}%"))
        .order_by(Car.model_name)
        .offset(offset)
        .limit(limit)
        .options(selectinload(Car.variants))
    )
    cars = db.exec(statement).all()

    result = []
    for car in cars:
        car_data = car.model_dump()
        car_data['variants'] = [VariantSchema.model_validate(v.model_dump()) for v in car.variants]
        result.append(CarSchema.model_validate(car_data))

    return result
