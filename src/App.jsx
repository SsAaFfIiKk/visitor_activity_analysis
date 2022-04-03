import React, {useState} from "react";


export default function App() {
    const upload_url = "https://dev.exclusive.onti.actcognitive.org/study/upload"
    const get_img_url = "https://dev.exclusive.onti.actcognitive.org/study/get_img"
    const predict_url = "https://dev.exclusive.onti.actcognitive.org/study/get_predict"
    
    const [selectedImage, setSelectedImage] = useState(null);
    const [predict, setPredict] = useState()

    const sendImg =() => {
        const data = new FormData()
        data.append("file", selectedImage)
        fetch(upload_url, { method: "post", body: data })
        setTimeout(1000)
        fetch(predict_url)
            .then(res => res.json())
            .then(out => setPredict(out))
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
                <img src={get_img_url} alt="Не удалось загрузить">
                </img>
            </div>
            <div>
                {predict}
            </div>
        </div>
    )
}