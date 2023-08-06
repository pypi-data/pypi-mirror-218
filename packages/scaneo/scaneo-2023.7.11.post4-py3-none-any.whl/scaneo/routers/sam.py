from fastapi import APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from samgeo import SamGeo
import rasterio as rio
import json
from .image.image_utils import to_uint8
from shapely.geometry import shape, MultiPolygon

router = APIRouter(prefix="/sam", tags=["sam"])

sam = SamGeo(
    checkpoint="sam_vit_h_4b8939.pth",
    model_type="vit_h",
    automatic=False,
    sam_kwargs=None,
)


class Body(BaseModel):
    points: list
    pointsLabel: list
    image: str
    label: str
    bands: dict


@router.post("")
def sam_points(body: Body):
    data = os.environ.get("DATA")
    # try:
    image_name = os.path.splitext(body.image)[0]
    image_path = data + "/" + body.image
    sam_path = data + "/sam/"
    os.makedirs(sam_path, exist_ok=True)
    rgb_file = sam_path + "rgb" + "_" + image_name + ".tif"
    mask_tif_file = sam_path + "mask" + "_" + image_name + ".tif"
    mask_geojson_file = sam_path + "mask" + "_" + image_name + ".geojson"
    prompts_geojson_file = sam_path + "prompts" + "_" + image_name + ".geojson"

    bands = body.bands
    red = int(bands["bands"]["red"])
    green = int(bands["bands"]["green"])
    blue = int(bands["bands"]["blue"])
    stretch_maximum = int(bands["stretch"]["maximum"])
    stretch_minimum = int(bands["stretch"]["minimum"])
    # generate RGB image
    ds = rio.open(image_path)
    bands = ds.read((red, green, blue))
    rgb = to_uint8(bands, stretch_minimum, stretch_maximum)
    # sabe RGB as tif
    profile = ds.profile
    profile.update(count=3, dtype="uint8")
    if not os.path.exists(rgb_file):
        with rio.open(rgb_file, "w", **profile) as dst:
            dst.write(rgb)
    # generate mask
    sam.set_image(rgb_file)
    sam.predict(
        body.points,
        point_labels=body.pointsLabel,
        point_crs="EPSG:4326",
        output=mask_tif_file,
    )
    sam.raster_to_vector(
        mask_tif_file,
        mask_geojson_file,
    )
    # adapt reponse to the format expected by the front-end
    with open(mask_geojson_file, "r") as f:
        geojson_data = json.load(f)
    geometries = []
    for feature in geojson_data["features"]:
        geometries.append(feature["geometry"]["coordinates"])
    # merged_geometry = MultiPolygon(geometries).buffer(0)
    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "MultiPolygon", "coordinates": geometries},
                "properties": {"label": body.label},
            }
        ],
    }

    prompt_object = {"type": "FeatureCollection", "features": []}

    for i, point in enumerate(body.points):
        prompt_object["features"].append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [point[0], point[1]]},
                "properties": {
                    "label": body.label,
                    "background": body.pointsLabel[i],
                },
            }
        )

    with open(prompts_geojson_file, "w") as f:
        json.dump(prompt_object, f)

    with open(mask_geojson_file, "w") as f:
        json.dump(geojson_data, f)
    return FileResponse(mask_geojson_file)
    # except Exception as e:
    #     return HTTPException(status_code=500, detail="Could not save new label")
