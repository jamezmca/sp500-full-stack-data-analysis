import React from 'react'
//title and dictionary definition
export default function Header() {
    return (
        <div className="mb-8 text-base">
            <div className="h-8 bg-gradient-to-b from-white to-transparent opacity-10"></div>
            <div className="m-8">
                <h1 style={{ textShadow: '0 0 5px white' }}
                    // className="text-center py-4 text-2xl sm:text-5xl text-gradient font-bold bg-gradient-to-r from-yellow-100 via-yellow-400 to-pink-500">
                    className="text-center py-4 text-2xl sm:text-5xl font-bold">
                    INTERCONNECTEDNESS</h1>
                <p className="text-center pt-4">1. The number of stocks that have experienced a stock devaluation of greater than 20%
                within the same time period.</p>
                <p className="text-center"><i>This stock has experience a price decrease greater than 20%. Let me
                check it's Interconnectedness to see if I should invest.</i></p>
            </div>
        </div>
    )
}
