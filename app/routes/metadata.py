# app/routes/metadata.py

from fastapi import APIRouter, HTTPException, Query
from app.models import MetadataResponse
import os
import json
from shapely.geometry import Polygon, Point
import logging
import math

router = APIRouter()

# Path to the data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("/metadata", response_model=MetadataResponse)
def get_metadata(
    latitude: float = Query(
        ..., 
        example=34.0522, 
        description="Latitude of the target location."
    ),
    longitude: float = Query(
        ..., 
        example=-118.2437, 
        description="Longitude of the target location."
    )
):
    """
    Retrieves metadata for the closest Landsat satellite image based on latitude and longitude.

    Args:
        latitude (float): Latitude of the target location.
        longitude (float): Longitude of the target location.

    Returns:
        MetadataResponse: The metadata associated with the closest satellite image.

    Raises:
        HTTPException: If there is an error fetching or processing metadata.
    """
    try:
        # Log the start of the metadata search
        logger.info(f"Looking for metadata for location: ({latitude}, {longitude})")

        user_point = Point(longitude, latitude)

        closest_metadata = None
        min_distance = float('inf')

        # Iterate over all JSON files in the data directory
        for filename in os.listdir(DATA_DIR):
            if filename.endswith('.json'):
                filepath = os.path.join(DATA_DIR, filename)
                
                # Log which file is being processed
                logger.info(f"Processing file: {filepath}")
                
                with open(filepath, 'r') as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError as json_err:
                        logger.error(f"Error decoding JSON file {filename}: {json_err}")
                        continue

                # Extract corner coordinates
                corners = data.get('PROJECTION_ATTRIBUTES', {})
                if not corners:
                    logger.info(f"No projection attributes found in file: {filename}")
                    continue  # Skip if no projection attributes

                ul_lat = corners.get('CORNER_UL_LAT_PRODUCT')
                ul_lon = corners.get('CORNER_UL_LON_PRODUCT')
                ur_lat = corners.get('CORNER_UR_LAT_PRODUCT')
                ur_lon = corners.get('CORNER_UR_LON_PRODUCT')
                ll_lat = corners.get('CORNER_LL_LAT_PRODUCT')
                ll_lon = corners.get('CORNER_LL_LON_PRODUCT')
                lr_lat = corners.get('CORNER_LR_LAT_PRODUCT')
                lr_lon = corners.get('CORNER_LR_LON_PRODUCT')

                if None in [ul_lat, ul_lon, ur_lat, ur_lon, ll_lat, ll_lon, lr_lat, lr_lon]:
                    logger.warning(f"Missing corner coordinates in file: {filename}")
                    continue  # Skip if any coordinate is missing

                # Create a polygon from corner coordinates
                polygon = Polygon([
                    (ul_lon, ul_lat),
                    (ur_lon, ur_lat),
                    (lr_lon, lr_lat),
                    (ll_lon, ll_lat)
                ])

                # Calculate centroid of the polygon
                centroid = polygon.centroid

                # Calculate the great-circle distance between user location and centroid
                def haversine(lon1, lat1, lon2, lat2):
                    R = 6371  # Earth radius in kilometers
                    phi1 = math.radians(lat1)
                    phi2 = math.radians(lat2)
                    delta_phi = math.radians(lat2 - lat1)
                    delta_lambda = math.radians(lon2 - lon1)
                    a = math.sin(delta_phi / 2) ** 2 + \
                        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
                    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                    return R * c  # Distance in kilometers

                distance_km = haversine(
                    user_point.x, user_point.y, centroid.x, centroid.y)

                logger.info(f"Distance to {filename}: {distance_km:.2f} km")

                if distance_km < min_distance:
                    min_distance = distance_km
                    closest_metadata = data

        if closest_metadata is not None:
            # Extract metadata and return it
            image_attributes = closest_metadata.get('IMAGE_ATTRIBUTES', {})
            projection_attributes = closest_metadata.get('PROJECTION_ATTRIBUTES', {})
            level1_processing_record = closest_metadata.get('LEVEL1_PROCESSING_RECORD', {})
            level2_processing_record = closest_metadata.get('LEVEL2_PROCESSING_RECORD', {})

            # Map fields to the MetadataResponse model
            metadata = MetadataResponse(
                satellite=image_attributes.get('SPACECRAFT_ID', 'Unknown'),
                acquisition_date=image_attributes.get('DATE_ACQUIRED', 'Unknown'),
                acquisition_time=image_attributes.get('SCENE_CENTER_TIME', 'Unknown'),
                latitude=latitude,
                longitude=longitude,
                wrs_path=image_attributes.get('WRS_PATH'),
                wrs_row=image_attributes.get('WRS_ROW'),
                cloud_coverage=image_attributes.get('CLOUD_COVER', 0.0),
                image_quality=str(image_attributes.get('IMAGE_QUALITY_OLI', 'Unknown')),
                sun_elevation=image_attributes.get('SUN_ELEVATION'),
                sun_azimuth=image_attributes.get('SUN_AZIMUTH'),
                ground_sampling_distance=projection_attributes.get('GRID_CELL_SIZE_REFLECTIVE'),
                projection=projection_attributes.get('MAP_PROJECTION'),
                processing_level=level2_processing_record.get('PROCESSING_LEVEL', level1_processing_record.get('PROCESSING_LEVEL', 'Unknown')),
                scene_id=level2_processing_record.get('LANDSAT_PRODUCT_ID', level1_processing_record.get('LANDSAT_PRODUCT_ID', 'Unknown')),
                orbit_number=None,  # Not available in the JSON
                sensor_type=image_attributes.get('SENSOR_ID', 'Unknown'),
                cloud_mask=None,  # Not available in the JSON
                distance_km=round(min_distance, 2)  # Include distance in the response
            )
            logger.info(f"Returning metadata from closest location at distance: {min_distance:.2f} km")
            return metadata

        else:
            logger.error("No metadata found for any location.")
            raise HTTPException(status_code=404, detail="No metadata available.")

    except Exception as e:
        # Log the error and return a 500 Internal Server Error
        logger.error(f"Error during metadata retrieval: {e}")
        raise HTTPException(status_code=500, detail=str(e))
