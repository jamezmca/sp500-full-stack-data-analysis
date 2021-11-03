import React, { useState, useEffect } from 'react'
import { useQuery } from "@apollo/client"
import { GET_PNGS, GET_RISK_REWARD } from '../GraphQL/Queries'
import BarChart from './BarChart'
//introduction / description / aim and intent or explanantion | stocks on sale
// investigaton exact
// background - other variables such as searches
// analytical methodology
// assumptions
// initial findings
// processed findings
// interpretation and conclusion
// opportuninities for additional research
export default function Report() {
    const [hehe, setHehe] = useState(false)
    const [img1, setImg1] = useState()
    const [img2, setImg2] = useState()
    const { loading: loadingPngs, error, data } = useQuery(GET_PNGS)
    const { loading: loadingRisk, error: errorRisk, data: dataRisk } = useQuery(GET_RISK_REWARD)

    useEffect(() => {
        if (!loadingPngs && !loadingRisk) {
            const contentType = 'image/png';
            let png1 = data.getPngs[0]['encode'].split("'")[1]
            let png2 = data.getPngs[1]['encode'].split("'")[1]

            const b64toBlob = (b64Data, contentType = '', sliceSize = 512) => {
                const byteCharacters = atob(b64Data)
                const byteArrays = []

                for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
                    const slice = byteCharacters.slice(offset, offset + sliceSize)

                    const byteNumbers = new Array(slice.length)
                    for (let i = 0; i < slice.length; i++) {
                        byteNumbers[i] = slice.charCodeAt(i)
                    }

                    const byteArray = new Uint8Array(byteNumbers)
                    byteArrays.push(byteArray)
                }

                const blob = new Blob(byteArrays, { type: contentType })
                return blob
            }

            const blob1 = b64toBlob(png1, contentType)
            const blob2 = b64toBlob(png2, contentType)

            setImg1(() => URL.createObjectURL(blob1))
            setImg2(() => URL.createObjectURL(blob2))
            setHehe(true)
        }
    }, [data, loadingPngs, loadingRisk])
    console.log(dataRisk)

    return (
        <div className="">
            <p>Investing is complicated; Desciphering the good opportunities from the less good opportuninities
            is like trying to the guess the murderer whilst watching the first episode of your new True Crime
            TV show. So to better understand the confusing investment world, I have investigated the idea
            that stock devaluations are stock sales, making them prime investment opportuninities.
            </p>
            <p>Stock sales revolves around the idea that there is a temporary price reduction of a stock - an individual has a lower buy in opportuninity. Surifically, this makes sense, but what if the stock price has dropped because the business unviable? This
            </p>
            {!loadingRisk && <BarChart data={dataRisk}/>}

            <h2>Interconnectedness As A Metric To Reveal Stock Investment Opportunties Following A 20% Reduction In Stock Price </h2>
            <h2>Definition of Terms: </h2>

            {hehe && (<div className="my-6">
                <h3 className="text-center mb-2 text-lg">Return Mulitpler Vs Interconnectedness</h3>
                <div className="flex text-center text-xs mx-10">
                    <div className="flex-1 border-b-2 border-green-400 border-opacity-60 mx-1 ">UQ</div>
                    <div className="flex-1 border-b-2 border-blue-900 mx-1">MEAN</div>
                    <div className="flex-1 border-b-2 border-purple-700 mx-1">MEDIAN</div>
                    <div className="flex-1 border-b-2 border-red-500 mx-1">LQ</div>
                    <div className="flex-1 border-b-2 border-green-300 mx-1">5TH</div>
                </div>
                <img src={img1} alt="graph1"/>
            </div>)}
            {hehe && (<div className="my-6">
                <h3 className="text-center mb-2 text-lg">Average Interconnectedness For A Given Return Multipler Range Of 10</h3>
                <img src={img2} alt="graph2" />
            </div>)}
        </div>
    )
}
