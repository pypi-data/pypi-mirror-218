from datetime import datetime
from typing import Any, List, Optional, Tuple

import numpy as np
import xarray as xr


def subset(
    ds,
    variables: Optional[List[str]] = None,
    geographical_subset: Optional[
        Tuple[
            Optional[float], Optional[float], Optional[float], Optional[float]
        ]
    ] = None,
    temporal_subset: Optional[
        Tuple[Optional[datetime], Optional[datetime]]
    ] = None,
    depth_range: Optional[Tuple[Optional[float], Optional[float]]] = None,
) -> xr.Dataset:

    if variables:
        ds = ds[np.array(variables)]

    if geographical_subset is not None and any(geographical_subset):
        (
            minimal_latitude,
            maximal_latitude,
            minimal_longitude,
            maximal_longitude,
        ) = geographical_subset
        latitude_subset = (minimal_latitude, maximal_latitude)
        longitude_subset = (minimal_longitude, maximal_longitude)

        if any(latitude_subset):
            latitude_selection = (
                minimal_latitude
                if minimal_latitude == maximal_latitude
                else slice(minimal_latitude, maximal_latitude)
            )
            latitude_method = (
                "nearest" if minimal_latitude == maximal_latitude else None
            )
            if "latitude" in ds.coords:
                ds = ds.sel(
                    latitude=latitude_selection, method=latitude_method
                )
            if "nav_lat" in ds.coords:
                ds = ds.sel(nav_lat=latitude_selection, method=latitude_method)
            if "x" in ds.coords:
                ds = ds.sel(x=latitude_selection, method=latitude_method)

        if any(longitude_subset):
            longitude_selection = (
                minimal_longitude
                if minimal_longitude == maximal_longitude
                else slice(minimal_longitude, maximal_longitude)
            )
            longitude_method = (
                "nearest" if minimal_longitude == maximal_longitude else None
            )
            if "longitude" in ds.coords:
                ds = ds.sel(
                    longitude=longitude_selection, method=longitude_method
                )
            if "nav_lon" in ds.coords:
                ds = ds.sel(
                    nav_lat=longitude_selection, method=longitude_method
                )
            if "y" in ds.coords:
                ds = ds.sel(y=longitude_selection, method=longitude_method)

    if temporal_subset is not None and any(temporal_subset):
        temporal_kwargs: dict[str, Any] = {}
        (start_datetime, end_datetime) = temporal_subset
        if "time_counter" in ds.coords:
            temporal_kwargs["time_counter"] = (
                start_datetime
                if start_datetime == end_datetime
                else slice(start_datetime, end_datetime)
            )
        else:
            temporal_kwargs["time"] = (
                start_datetime
                if start_datetime == end_datetime
                else slice(start_datetime, end_datetime)
            )

        temporal_kwargs["method"] = (
            "nearest" if start_datetime == end_datetime else None
        )

        ds = ds.sel(**temporal_kwargs)

    if depth_range is not None and any(depth_range):
        depth_kwargs: dict[str, Any] = {}
        minimal_depth, maximal_depth = depth_range

        if "depth" in ds.dims:
            depth_kwargs["depth"] = (
                minimal_depth
                if minimal_depth == maximal_depth
                else slice(minimal_depth, maximal_depth)
            )
        elif "deptht" in ds.dims:
            depth_kwargs["deptht"] = (
                minimal_depth
                if minimal_depth == maximal_depth
                else slice(minimal_depth, maximal_depth)
            )
        elif "elevation" in ds.dims:
            minimal_depth = minimal_depth * -1.0 if minimal_depth else None
            maximal_depth = maximal_depth * -1.0 if maximal_depth else None
            depth_kwargs["elevation"] = (
                minimal_depth
                if minimal_depth == maximal_depth
                else slice(maximal_depth, minimal_depth)
            )

        depth_kwargs["method"] = (
            "nearest" if minimal_depth == maximal_depth else None
        )

        ds = ds.sel(**depth_kwargs)

    return ds
