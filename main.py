from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import json

app = FastAPI()

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

    # Process the uploaded file
    contents = await file.read()

    # Here you can save the file, process the image, etc.
    # For this example, we'll just return a confirmation message
    return JSONResponse(content={"message": "File uploaded successfully", "imageObject": image_object.dict()})
