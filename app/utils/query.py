from typing import Optional, Dict, Any

def build_query(
    country: Optional[str] = None,
    metric: Optional[str] = None,
    sub_sector: Optional[str] = None,
    sub_sub_sector: Optional[str] = None,
    year: Optional[int] = None,
    start_year: Optional[int] = None,
    end_year: Optional[int] = None
) -> Dict[str, Any]:
    q: Dict[str, Any] = {}

    if country:
        q["country"] = {"$regex": f"^{country}$", "$options": "i"}
    if metric:
        q["metric"] = {"$regex": metric, "$options": "i"}
    if sub_sector:
        q["sub_sector"] = {"$regex": sub_sector, "$options": "i"}
    if sub_sub_sector:
        q["sub_sub_sector"] = {"$regex": sub_sub_sector, "$options": "i"}

    # multiple year filter
    if year:
        q[str(year)] = {"$exists": True, "$ne": None}

    # year range filter
    if start_year or end_year:
        exist_filters = []
        start = start_year or 2000
        end = end_year or 2022
        for y in range(start, end + 1):
            exist_filters.append({str(y): {"$exists": True, "$ne": None}})
        q["$or"] = exist_filters

    return q
