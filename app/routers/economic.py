from typing import Optional, List
from fastapi import APIRouter, Query, HTTPException
from app.database.db import MongoDB
from app.models.economic import EconomicModel
from app.utils.alert import logger
from app.utils.clear import sanitize_floats
from app.utils.query import build_query

router = APIRouter()

@router.get("", response_model=List[EconomicModel])
async def get_economic_data(
    country: Optional[str] = Query(None),
    metric: Optional[str] = Query(None),
    sub_sector: Optional[str] = Query(None),
    sub_sub_sector: Optional[str] = Query(None),
    year: Optional[int] = Query(None, ge=1900, le=2100),
    start_year: Optional[int] = Query(None, ge=1900, le=2100),
    end_year: Optional[int] = Query(None, ge=1900, le=2100),
    limit: int = Query(50, ge=1, le=1000),
    skip: int = Query(0, ge=0),
    sort_by: Optional[str] = Query(None),
    sort_order: int = Query(1)
):
    try:
        collection = MongoDB.get_collection("social_collection")
        query = build_query(country, metric, sub_sector, sub_sub_sector, year, start_year, end_year)

        projection = {
            "_id": 0,
            "country": 1,
            "country_serial": 1,
            "metric": 1,
            "unit": 1,
            "sector": 1,
            "sub_sector": 1,
            "sub_sub_sector": 1,
            "source_link": 1,
            "source": 1
        }

        if year:
            projection[str(year)] = 1
        elif start_year or end_year:
            start = start_year or 2000
            end = end_year or 2024
            for y in range(start, end + 1):
                projection[str(y)] = 1
        else:
            for y in range(2000, 2022+1):
                projection[str(y)] = 1

        cursor = collection.find(query, projection).skip(skip).limit(limit)
        if sort_by:
            cursor = cursor.sort(sort_by, sort_order)

        results = []
        async for doc in cursor:
            clean_doc = sanitize_floats(doc)
            results.append(EconomicModel.from_db(clean_doc))

        if not results:
            raise HTTPException(status_code=404, detail="No records found for given filters")

        return results
    except HTTPException as http_error:
        raise http_error

    except ValueError as ve:
        logger(ve)
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        logger(e)
        raise HTTPException(status_code=500, detail=str(e))