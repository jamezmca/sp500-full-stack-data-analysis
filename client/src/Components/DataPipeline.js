import React from 'react'
//optional dropdown displaying the datapipeline for the project
export default function DataPipeline() {
    return (
        <div className="my-10 text-center">
            <h2 className="relative text-center uppercase text-2xl sm:text-3xl font-semibold text-pink-600 mb-6">System Architecture</h2>
            <div className="flex justify-around flex-wrap">
                <div className="bg-white m-1 p-2 text-pink-500 shadow-md flex-1">
                    <div className="bg-red-300">
                        <h4 className="text-center mb-1">FRONT END&rarr;</h4>
                    </div>
                    <ul className="text-xs px-2">
                        <li>REACT</li>
                        <li>GRAPHQL</li>
                        <li>APOLLO</li>
                        <li>TAILWINDCSS</li>
                    </ul>
                </div>

                <div className="bg-white m-1 p-2 text-pink-500 shadow-md flex-1">
                    <div className="bg-red-300">
                        <h4 className="text-center mb-1">&larr;BACK END&rarr;</h4>
                    </div>
                    <ul className="text-xs px-2">
                        <li>EXPRESS</li>
                        <li>GRAPHQL </li>
                        <li>APOLLO</li>
                        <li>POSTGRESQL </li>
                    </ul>
                </div>
                <div className="bg-white m-1 p-2 text-pink-500 shadow-md flex-1">
                    <div className="bg-red-300">
                        <h4 className="text-center mb-1">&larr;DATABASE&rarr;</h4>
                    </div>
                    <ul className="text-xs px-2">
                        <li>AWS</li>
                        <li>POSTRGESQL</li>
                    </ul>
                </div>
                <div className="bg-white m-1 p-2 text-pink-500 shadow-md flex-1">
                    <div className="bg-red-300">
                        <h4 className="text-center mb-1">&larr;ANALYSIS</h4>
                    </div>
                    <ul className="text-xs px-2">
                        <li>PYTHON</li>
                        <li>PLOTLY</li>
                        <li>SCIPY</li>
                        <li>ASYNCPG</li>
                    </ul>
                </div>
            </div>
        </div>
    )
}
