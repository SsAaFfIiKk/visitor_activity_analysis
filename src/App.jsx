import React, {useEffect, useState} from "react";


export default function App() {

    const [predict, setPredict] = useState("predict")

    useEffect(() => {
        fetch("https://dev.exclusive.onti.actcognitive.org/study/get_predict")
            .then(res => res.json())
            .then(out => { setPredict(out); console.log(out) })
    }, [])

    return (
        <div>
            <div>
                <img src="https://dev.exclusive.onti.actcognitive.org/study/get_img" alt="Не удалось загрузить">
                </img>
            </div>
            <div>
                {predict}
            </div>
        </div>
    )
}