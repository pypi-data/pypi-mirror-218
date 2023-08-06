import logging
import os
from datetime import datetime
from os import path
from typing import Optional

import click
import xarray as xr
import zarr

from copernicus_marine_client.catalogue_parser.request_structure import (
    SubsetRequest,
)
from copernicus_marine_client.download_functions.subset_xarray import subset


def get_optimized_chunking(subset_request: SubsetRequest) -> str:
    """Function to calculate the optimized type of chunking,
    based on a subset_request.
    Returns a str: "map" if time-chunking is optimized,
    "timeserie" if geo-chunking is optimized
    """
    logging.info(
        "THIS CHUNKING OPTIMIZATION FUNCTION IS "
        + "A PLACEHOLDER, DO NOT RELY ON IT!!"
    )
    chunking_selected = "map"
    if (
        isinstance(subset_request.minimal_latitude, float)
        and isinstance(subset_request.maximal_latitude, float)
        and isinstance(subset_request.minimal_longitude, float)
        and isinstance(subset_request.maximal_longitude, float)
    ):
        surface = abs(
            subset_request.maximal_longitude - subset_request.minimal_longitude
        ) * abs(
            subset_request.maximal_latitude - subset_request.minimal_latitude
        )

        if surface < 20:
            chunking_selected = "timeserie"
    return chunking_selected


def download_dataset(
    username: str,
    password: str,
    geographical_subset: Optional[
        tuple[
            Optional[float], Optional[float], Optional[float], Optional[float]
        ]
    ],
    temporal_subset: Optional[tuple[Optional[datetime], Optional[datetime]]],
    depth_range: Optional[tuple[Optional[float], Optional[float]]],
    dataset_url: str,
    output_directory: str,
    output_filename: str,
    variables: Optional[list[str]],
    assume_yes: bool = False,
):

    dataset = xr.open_zarr(dataset_url)
    dataset = subset(
        dataset, variables, geographical_subset, temporal_subset, depth_range
    )
    dataset = dataset.chunk(chunks="auto")

    if not assume_yes:
        logger = logging.getLogger("blank_logger")
        logger.warn(dataset)
        click.confirm("Do you want to continue?", abort=True, default=True)

    if output_filename.endswith(".nc"):
        if not os.path.isdir(output_directory):
            os.makedirs(output_directory)
        dataset.to_netcdf(path.join(output_directory, output_filename))
    else:
        store = zarr.DirectoryStore(
            path.join(output_directory, output_filename)
        )
        dataset.to_zarr(store)

    logging.info(
        f"Successfully downloaded to {path.join(output_directory, output_filename)}"
    )


def download_zarr(
    username: str,
    password: str,
    subset_request: SubsetRequest,
):

    geographical_subset = (
        subset_request.minimal_latitude,
        subset_request.maximal_latitude,
        subset_request.minimal_longitude,
        subset_request.maximal_longitude,
    )
    temporal_subset = (
        subset_request.start_datetime,
        subset_request.end_datetime,
    )
    depth_range = (subset_request.minimal_depth, subset_request.maximal_depth)
    dataset_url = str(subset_request.dataset_url)
    output_directory = (
        subset_request.output_directory
        if subset_request.output_directory
        else "."
    )
    output_filename = (
        subset_request.output_filename
        if subset_request.output_filename
        else "data.zarr"
    )
    variables = subset_request.variables
    assume_yes = subset_request.assume_yes

    download_dataset(
        username=username,
        password=password,
        geographical_subset=geographical_subset,
        temporal_subset=temporal_subset,
        depth_range=depth_range,
        dataset_url=dataset_url,
        output_directory=output_directory,
        output_filename=output_filename,
        variables=variables,
        assume_yes=assume_yes,
    )
    return path.join(output_directory, output_filename)
