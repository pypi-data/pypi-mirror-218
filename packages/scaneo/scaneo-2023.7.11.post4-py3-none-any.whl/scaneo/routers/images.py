from fastapi import APIRouter, HTTPException, status
from typing import List
import os
from starlette.responses import StreamingResponse

from .image import get_image_data, get_tile_data, ready_image, get_bbox
from .image.errors import ImageOutOfBounds

router = APIRouter(prefix="/images", tags=["images"])


@router.get("")
def get_images():
    try:
        data = os.environ.get("DATA")
        images = [f for f in os.listdir(data) if f.endswith(".tif")]
        bboxes = [get_bbox(data + "/" + image) for image in images]
        return [{"name": image, "bbox": bbox} for image, bbox in zip(images, bboxes)]
    except Exception as e:
        return HTTPException(status_code=500, detail="Could not get images")


@router.get("/{image:path}/{z}/{x}/{y}.png")
def retrieve_image_tile(
    image: str,
    z: int,
    x: int,
    y: int,
    bands: str = "4,3,2",
    stretch: str = "0,3000",
    palette: str = "viridis",
):
    data = os.environ.get("DATA")
    image_path = data + "/" + image
    tile_size = (256, 256)
    if len(bands) == 1:
        bands = int(bands)
    else:
        bands = tuple([int(band) for band in bands.split(",")])
    stretch = tuple([float(v) for v in stretch.split(",")])
    try:
        tile = get_tile_data(image_path, (x, y, z), bands, tile_size)
        tile = get_image_data(tile, stretch, palette)
        image = ready_image(tile)
        return StreamingResponse(image, media_type="image/png")
    except ImageOutOfBounds as error:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
        return None
    except Exception as e:
        # raise HTTPException(status_code=500, detail="Could not retrieve tile")
        return None
