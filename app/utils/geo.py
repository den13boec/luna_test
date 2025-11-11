from typing import Any
from sqlalchemy import ColumnElement, func
from sqlalchemy import and_, or_

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


def _wrap_lon(lon: float) -> float:
    # нормализуем в диапазон [-180, 180)
    return ((lon + 180.0) % 360.0) - 180.0


def bbox_condition(
    lon_col: ColumnElement,
    lat_col: ColumnElement,
    min_lon: float,
    min_lat: float,
    max_lon: float,
    max_lat: float,
) -> ColumnElement[bool]:
    """
    WHERE-условие для bbox c учётом антимеридиана.
    - широты обычные: min_lat <= lat <= max_lat
    - долготы: либо обычный интервал, либо wrap (OR)
    """
    min_lon = _wrap_lon(min_lon)
    max_lon = _wrap_lon(max_lon)

    # нормализуем порядок широт (на всякий случай)
    if min_lat > max_lat:
        min_lat, max_lat = max_lat, min_lat

    lat_ok = and_(lat_col >= min_lat, lat_col <= max_lat)

    if min_lon <= max_lon:
        # обычный прямоугольник
        lon_ok = and_(lon_col >= min_lon, lon_col <= max_lon)
    else:
        # пересекает антимеридиан: 170…-170 → (lon >= 170) OR (lon <= -170)
        lon_ok = or_(lon_col >= min_lon, lon_col <= max_lon)

    return and_(lat_ok, lon_ok)
