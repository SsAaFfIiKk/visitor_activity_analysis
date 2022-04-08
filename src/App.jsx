import React, { useState, useEffect } from "react";
import "./App.css"

export default function App() {
    // const upload_url = "https://dev.exclusive.onti.actcognitive.org/study/upload"
    // const get_img_url = "https://dev.exclusive.onti.actcognitive.org/study/get_img"
    // const predict_url = "https://dev.exclusive.onti.actcognitive.org/study/get_predict"

    const upload_url = "http://127.0.0.1:8000/upload"
    const get_img_url = "http://127.0.0.1:8000/get_img"
    const predict_url = "http://127.0.0.1:8000/get_predict"

    const [uploadStatus, setUploadStatus] = useState("фото не отпралялось")
    const [predict, setPredict] = useState()
    const [img, setImg] = useState();

    useEffect(() => {
        fetch(predict_url)
            .then(res => res.json())
            .then(out => setPredict(out))
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


    return (
        <div>
            <div className="image">
                {predict && <img src={img} alt="Не удалось загрузить" />}
            </div>
            <div className="predict">
                Предсказание модели: {predict}
            </div>
            <div className="upload">
                <input type="file" onChange={onImageChange} />
            </div>
            <div className="uploadStatus">
                {uploadStatus}
            </div>
        </div>
    )
}