import os
import random
import shutil
import uvicorn
from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from tools import create_folders, unpack_archive, generate_predict

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

path_to_storage = "save_data/"
file_extensions = ["mp4", "avi"]
imgs = os.listdir(path_to_storage)


@app.get("/get_img")
def get_img():
    index = random.randrange(0, len(imgs))
    return FileResponse(os.path.join(path_to_storage, imgs[index]))


@app.get("/get_predict")
def get_predict():
    return generate_predict()


@app.post("/save_to_analyze")
def save(file: UploadFile = File(...)):
    file_name = file.filename

    if file_name.endswith(".zip"):
        path_to_save = create_folders(path_to_storage, file_name.split(".")[0])

        with open(path_to_save + file_name, "wb") as archive:
            shutil.copyfileobj(file.file, archive)
        unpack_archive(file_name, path_to_save, file_extensions)

        return "Архив сохранён"

    else:
        return "Загруженный файл не архив"


if __name__ == "__main__":
    uvicorn.run(app)