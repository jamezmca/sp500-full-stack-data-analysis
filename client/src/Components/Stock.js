import React from 'react'

export default function Stock(
    { bombStock: {
        name,
        decPerc,
        maxPrice,
        minPrice,
        daysSinceMin,
        gradient,
        maxIndex,
        minIndex } }
) {
    let bgColor = minIndex - maxIndex < 2.6*5 ? 'bg-green-400' : 'bg-white'
    let style = "p-2 m-2 text-indigo-800 font-semibold text-xs flex justify-between items-center " + bgColor
    console.log(style)
    return (
        <div className={style}>
            <h1 className="flex-1">{name}</h1>
            <p className="flex-1 text-center text-pink-600">&darr;{decPerc.toFixed(1)}%</p>
            <p className="flex-1 text-center">{gradient.toFixed(1)}%</p>
            <p className="flex-1 text-center">${minPrice.toFixed(1)}</p>
            <p className="flex-1 text-right">DSM: {daysSinceMin}</p>
        </div>
    )
}
