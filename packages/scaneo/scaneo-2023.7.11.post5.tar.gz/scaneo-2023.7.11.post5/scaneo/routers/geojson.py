from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import json
import os
import shutil

router = APIRouter(prefix="/geojson", tags=["geojson"])


class GeoJSONFeature(BaseModel):
    type: str
    geometry: dict
    properties: dict


class GeoJSON(BaseModel):
    type: str
    features: List[GeoJSONFeature]


class Body(BaseModel):
    name: str
    geojson: GeoJSON


maskPrefix = "mask_"
promptsPrefix = "prompts_"
geojsonAppendix = ".geojson"


@router.post("")
def save_geojson(
    body: Body,
):
    data = os.environ.get("DATA")
    file_name = os.path.splitext(body.name)[0]
    sam_path = data + "/sam/"
    prompts_geojson_file = sam_path + "prompts" + "_" + file_name + ".geojson"

    try:
        with open(data + "/" + maskPrefix + file_name + geojsonAppendix, "w") as f:
            geojson = body.geojson.json()
            f.write(geojson)
        if os.path.isfile(prompts_geojson_file):
            shutil.copy(prompts_geojson_file, data)
        return {"status": "201 Created", "geojson": geojson, "imageName": body.name}

    except Exception as e:
        return HTTPException(status_code=500, detail="Could not save geojson")


@router.get("/{name}")
def get_geojson(name: str):
    data = os.environ.get("DATA")
    file_name = os.path.splitext(name)[0]

    try:
        with open(data + "/" + maskPrefix + file_name + geojsonAppendix, "r") as f:
            geojson = json.load(f)
        return geojson

    except Exception as e:
        return HTTPException(status_code=500, detail="Could not get geojson")



