import React from 'react'

export default function Stock(
    { bombStock: {
        name,
        decPerc,
        maxPrice,
        minPrice,
        daysSinceMin,
        gradient } }
) {
    return (
        <div className="p-2 m-2 bg-white text-indigo-800 font-semibold text-xs flex justify-between items-center">
            <h1 className="flex-1">{name}</h1>
            <p className="flex-1 text-center text-pink-600">&darr;{decPerc.toFixed(1)}%</p>
            <p className="flex-1 text-center">{gradient.toFixed(1)}%</p>
            <p className="flex-1 text-center">${minPrice.toFixed(1)}</p>
            <p className="flex-1 text-right">DSM: {daysSinceMin}</p>
        </div>
    )
}
