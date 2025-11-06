from typing import Any
from sqlalchemy import ColumnElement, func

EARTH_RADIUS_KM = 6371.0088


def haversine_km(lat1, lon1, lat_col, lon_col) -> ColumnElement[Any]:
    dlat = func.radians(lat_col - lat1)
    dlon = func.radians(lon_col - lon1)
    lat1_rad = func.radians(lat1)
    lat2_rad = func.radians(lat_col)
    a = func.pow(func.sin(dlat / 2.0), 2) + func.cos(lat1_rad) * func.cos(
        lat2_rad
    ) * func.pow(func.sin(dlon / 2.0), 2)
    c = 2 * func.asin(func.sqrt(a))
    return EARTH_RADIUS_KM * c
