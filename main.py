from tools import Img, generate_predict
from fastapi.responses import Response
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

img = Img()


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    contents = await file.read()
    img.img_bytes = contents
    predict = generate_predict(contents)
    print(predict)
    img.predict = predict
    return {"Filename": file.filename}


@app.get("/get_img")
def get_img():
    return Response(content=img.img_bytes, media_type="image/png")


@app.get("/get_predict")
def get_predict():
    return img.predict
