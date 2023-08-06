from typing import Annotated

import os
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from pwnic.exploits import PythonExploit, exploits
from pwnic.utils import install_package

try:
    from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

app = FastAPI()


@app.get("/")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}


@app.post("/upload")
def upload(
    type: Annotated[str, Form()],
    name: Annotated[str, Form()],
    files: Annotated[list[UploadFile], File()],
) -> dict[str | None, int | None]:
    valid_types = ["python", "docker", "executable"]
    if type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"{type} is not a valid exploit type. It must be one of {valid_types}",
        )

    path = "exploits/" + name
    if not Path(path).exists():
        os.makedirs(path)
        ic()
    for f in files:
        with open(f"{path}/{f.filename}", "wb") as fs:
            fs.write(f.file.read())
    if type == "python":
        ic()
        PythonExploit(name)

    return {f.filename: f.size for f in files}


@app.get("/install")
def api_install_package(package: str) -> dict[str, str]:
    if install_package(package):
        return {package: "installed"}
    else:
        return {package: "error"}


@app.get("/run")
def run(exploit: str) -> None:
    if exploit not in exploits:
        raise HTTPException(
            status_code=400,
            detail=f"{exploit} is not a valid exploit. It must be one of {exploits.keys()}",
        )

    # exploits[exploit].run(Target)
