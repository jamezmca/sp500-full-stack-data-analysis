import React, { useEffect } from 'react'
import { useQuery, gql } from "@apollo/client"
import { GET_STOCKS_LIST } from '../GraphQL/Queries'
import { introspectionFromSchema } from 'graphql';
import Stock from './Stock';
//information will be stock_id | name | lastfetched | 'prices x 14 in CSV format'


//i want some logic that fetches data from a react hook depending on when the last entry was from 


export default function StockList() {
  const { loading, error, data } = useQuery(GET_STOCKS_LIST);

  useEffect(() => {
    if (!loading) {
      const lastFetchedDate = data.getAllStockPrices[0].lastfetched
      console.log(lastFetchedDate)
      var d = new Date(0)
      d.setUTCMilliseconds(lastFetchedDate)
      console.log(d)

      //and here run new function if dates are different
      // IF NOT TODAy {} ETC
    }
  })

  if (!loading) {
    function findBombStocks(stocks, weeks) {
      let arrayOfBombStocks = []
      let interconnectednessCount = 0
      //rate of drop
      //total percentage drop
      //days since min drop value
      //
      for (let stock of stocks) {
        let arrayOfPrices = stock.prices.split(' ').map(val => parseFloat(val))
        // console.log(arrayOfPrices)
        let maxPrice = Math.max(...arrayOfPrices)
        let minPrice = Math.min(...arrayOfPrices)
        let maxIndex = arrayOfPrices.indexOf(maxPrice)
        let minIndex = arrayOfPrices.indexOf(minPrice)
        let delta = minIndex - maxIndex
        let devaluation = maxPrice / minPrice
        if (delta > 0 && devaluation > 1.2) {
          console.log(stock.name, maxPrice, minPrice, maxIndex, minIndex, delta, devaluation)
          let temp = {
            name: stock.name.toUpperCase().replace('_', " "),
            decPerc: 100 - (minPrice * 100 / maxPrice),
            maxPrice,
            minPrice,
            daysSinceMin: arrayOfPrices.length - minIndex,
            gradient: (100 - (minPrice * 100 / maxPrice)) / delta
          }
          arrayOfBombStocks.push(temp)
          if (temp.daysSinceMin <= 10) interconnectednessCount++
        }
      }
      return {arrayOfBombStocks, interconnectednessCount}
    }
    // console.log(data.getAllStockPrices)
    let {arrayOfBombStocks: bombStocks, interconnectednessCount: count} = findBombStocks(data.getAllStockPrices, 2)


    return (
      <div className="my-10">
        <h2 className="text-center uppercase text-2xl sm:text-3xl font-semibold text-indigo-600 mb-2">Bomb Stocks</h2>
        <p className="text-center">Interconnectedness of events in the last two weeks: {count}</p>
        <div className="mt-4">
          <div className="flex mx-2 px-1 bg-indigo-600 text-sm">
            <div className="flex-1">NAME</div>
            <div className="flex-1 text-center">DIP%</div>
            <div className="flex-1 text-center">GRAD%/DAY</div>
            <div className="flex-1 text-center">$MIN</div>
            <div className="flex-1 text-right">DAYS SINCE MIN</div>
          </div>
          {bombStocks.map((bombStock, i) => {
            return <Stock bombStock={bombStock} key={i} />
          })}
        </div>
      </div>
    )
  }
  return (
    <h2 className="text-center uppercase text-lg font-semibold">CALCULATING...</h2>
  )

}
