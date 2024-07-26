from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import json
import os
import shutil

app = FastAPI()

# Create a directory to save uploaded images
UPLOAD_DIRECTORY = "./uploaded_images"

# exist_ok=True means if dir exist don't change anything
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# Mount the static files directory
app.mount("/uploaded_images", StaticFiles(directory=UPLOAD_DIRECTORY), name="uploaded_images")

class Drawing(BaseModel):
    r: int
    s: list

class ImageObject(BaseModel):
    order_id: str
    damageNr: int
    filesize: int
    type: int
    active: bool
    isPub: int
    realname: str
    drawings: Drawing
    recordDate: str
    id: Optional[int] = None
    base64: str
    synced: bool

@app.post("/upload/")
async def upload_image(
    order_id: str = Form(...),
    damageNr: int = Form(...),
    filesize: int = Form(...),
    type: int = Form(...),
    active: bool = Form(...),
    isPub: int = Form(...),
    realname: str = Form(...),
    drawings: str = Form(...),
    recordDate: str = Form(...),
    id: Optional[int] = Form(None),
    base64: str = Form(...),
    synced: bool = Form(...),
    file: UploadFile = File(...)
):
    # Parse the drawings string to a JSON object
    drawings_json = json.loads(drawings)
    drawing_object = Drawing(**drawings_json)
    
    # Create the ImageObject
    image_object = ImageObject(
        order_id=order_id,
        damageNr=damageNr,
        filesize=filesize,
        type=type,
        active=active,
        isPub=isPub,
        realname=realname,
        drawings=drawing_object,
        recordDate=recordDate,
        id=id,
        base64=base64,
        synced=synced
    )

    # Save the uploaded file
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    # Return the image URL in the response
    image_url = f"/uploaded_images/{file.filename}"
    return JSONResponse(content={"message": "File uploaded successfully", "image_url": image_url, "imageObject": image_object.dict()})

# Optional: add a health check endpoint
@app.get("/health")
def health_check():
    return {"status": "OK"}
