import React from 'react'
//title and dictionary definition
export default function Header() {
    return (
        <div className="mb-8 text-base">
            <h1 style={{textShadow: '2px 2px 1px Aquamarine'}} className="text-center py-4 text-2xl sm:text-5xl">INTERCONNECTEDNESS</h1>
            <p className="text-center">1. The number of stocks that have experienced a stock value decrease greater than 20%
                in the same time period.</p>
            <p className="text-center"><i>This stock has experience a price decrease greater than 20%. Let me 
                check it's Interconnectedness to see if I should invest.</i></p>
        </div>
    )
}
