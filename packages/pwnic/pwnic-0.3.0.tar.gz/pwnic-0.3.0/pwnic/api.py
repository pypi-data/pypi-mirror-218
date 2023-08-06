from typing import Annotated, Any

import os
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/upload")
def upload(
    type: Annotated[str, Form()],
    name: Annotated[str, Form()],
    files: Annotated[list[UploadFile], File()],
):
    valid_types = ["python", "docker", "executable"]
    if type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"{type} is not a valid exploit type. It must be one of {valid_types}",
        )

    path = "exploits/" + name
    if not Path(path).exists():
        os.makedirs(path)
    for f in files:
        with open(f"{path}/{f.filename}", "wb") as fs:
            fs.write(f.file.read())

    return {f.filename: f.size for f in files}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=7070)
