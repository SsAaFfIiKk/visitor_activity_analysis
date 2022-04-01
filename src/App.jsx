import React, {useEffect, useState} from "react";


export default function App() {
    const upload_url = "https://dev.exclusive.onti.actcognitive.org/study/upload"
    const get_img = "https://dev.exclusive.onti.actcognitive.org/study/get_img"
    const predict_url = "https://dev.exclusive.onti.actcognitive.org/study/get_predict"
    
    const [selectedImage, setSelectedImage] = useState(null);
    const [predict, setPredict] = useState("predict")

    const sendImg =() => {
        const data = new FormData()
        data.append("file", selectedImage)
        fetch(upload_url, { method: "post", body: data })
        
        fetch("https://dev.exclusive.onti.actcognitive.org/study/get_predict")
            .then(res => res.json())
            .then(out => { setPredict(out); console.log(out) })
    }

    return (
        <div>
            <div>
                <input
                    type="file"
                    name="myImage"
                    onChange={(event) => {
                        setSelectedImage(event.target.files[0]);
                        sendImg()
                    }}
                />
            </div>
            <div>
                {predict}
            </div>
        </div>
    )
}