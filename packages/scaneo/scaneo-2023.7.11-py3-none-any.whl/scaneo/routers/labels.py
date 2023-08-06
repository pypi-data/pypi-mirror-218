from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import json
import os

router = APIRouter(prefix="/labels", tags=["labels"])


class Body(BaseModel):
    labels: list


@router.post("")
def save_labels(body: Body):
    data = os.environ.get("DATA")
    try:
        with open(data + "/labels.json", "w") as f:
            allLabels = body.json()
            f.write(allLabels)

        return {"status": "201 Created", "labels": body.labels}

    except Exception as e:
        return HTTPException(status_code=500, detail="Could not save new label")


@router.get("")
def get_labels():
    data = os.environ.get("DATA")
    labels_file = os.path.join(data, "labels.json")
    try:
        if os.path.exists(labels_file):
            with open(labels_file, "r") as f:
                labels = json.load(f)
            return labels
        else:
            return HTTPException(status_code=404, detail="Labels file not found")

    except Exception as e:
        return HTTPException(status_code=500, detail="Could not get labels")
