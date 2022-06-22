import React, { useState, useEffect } from "react";
import "./App.css"

export default function App() {

    const upload_url = "http://127.0.0.1:8000/upload"
    const get_img_url = "http://127.0.0.1:8000/get_img"
    const predict_url = "http://127.0.0.1:8000/get_predict"

    const [uploadStatus, setUploadStatus] = useState("фото не отпралялось")
    const [img, setImg] = useState();
    const [type, setType] = useState("upload");

    useEffect(() => {
        fetch(predict_url)
            .then(res => res.json())
        fetchImage();
    }, [uploadStatus])

    const onImageChange = (event) => {
        if (event.target.files && event.target.files[0]) {
            sendImg(event.target.files[0])
        }
    }

    const sendImg = (img) => {
        let formData = new FormData()
        formData.append("file", img)

        fetch(upload_url, {
            method: "POST",
            body: formData
        })
            .then(setUploadStatus("фото загружено"))
    }

    const fetchImage = async () => {
        const res = await fetch(get_img_url);
        const imageBlob = await res.blob();
        const imageObjectURL = URL.createObjectURL(imageBlob);
        setImg(imageObjectURL);
        setUploadStatus("фото не отпраялялось")
    };

    let content;

    switch (type) {
        default:
        case "upload":
            content = (
                <div>
                    <div className="title">
                        GI tract Image Segmentation
                    </div>
                    <div className="upload">
                        <div >
                            <div>
                                Upload image file for segmentation:
                            </div>
                            <input type="file" onChange={onImageChange} />
                        </div>
                    </div>
                    <div className="uploadStatus">
                        {uploadStatus}
                    </div>
                    <div className="mask">
                        <button onClick={() => { setType("mask") }}>Получить маску</button>
                    </div>
                </div>
            )
            break
        case "mask":
            content = (
                <div>
                    <div className="image">
                        <img src={img} alt="Не удалось загрузить" />
                    </div>
                    <div className="back">
                        <button onClick={() => { setType("upload") }}>Назад</button>
                    </div>
                </div>
            )
            break
    }

    return content
}