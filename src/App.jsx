import React, {useEffect, useState} from "react";


export default function App() {

    const [predict, setPredict] = useState("predict")

    useEffect(() => {
        fetch("https://teachingquality.onti.actcognitive.org/get_predict")
            .then(res => res.json())
            .then(out => { setPredict(out); console.log(out) })
    }, [])

    return (
        <div>
            <div>
                <img src="https://teachingquality.onti.actcognitive.org/get_img" alt="Не удалось загрузить">
                </img>
            </div>
            <div>
                {predict}
            </div>
        </div>
    )
}