import React, { useState, useEffect } from "react";


export default function App() {
    const upload_url = "https://dev.exclusive.onti.actcognitive.org/study/upload"
    const get_img_url = "https://dev.exclusive.onti.actcognitive.org/study/get_img"
    const predict_url = "https://dev.exclusive.onti.actcognitive.org/study/get_predict"

    // const upload_url = "http://127.0.0.1:8000/upload"
    // const get_img_url = "http://127.0.0.1:8000/get_img"
    // const predict_url = "http://127.0.0.1:8000/get_predict"
    
    const [predict, setPredict] = useState()

    useEffect(() => {
        fetch(predict_url)
            .then(res => res.json())
            .then(out => setPredict(out))
    }, [])

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

        fetch(predict_url)
            .then(res => res.json())
            .then(out => setPredict(out))
    }

    return (
        <div>
            <div>
                <input type="file" onChange={onImageChange}/>
            </div>
            <div>
                {predict && <img src={get_img_url} alt="Не удалось загрузить"></img>}
            </div>
            <div>
                {predict}
            </div>
        </div>
    )
}