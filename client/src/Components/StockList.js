import React, { useState, useEffect } from 'react'
import { useQuery, gql, useLazyQuery, useMutation } from "@apollo/client"
import { GET_STOCKS_LIST, GET_LIST_OF_STOCKS, GET_NEW_LIST_OF_STOCK_PRICES } from '../GraphQL/Queries'
import { UPDATE_STOCK_PRICES } from '../GraphQL/Mutations'
import { fetchData } from '../api'
import Stock from './Stock';
//information will be stock_id | name | lastfetched | 'prices x 14 in CSV format'


export default function StockList() {
  const { loading: loading1, error: error1, data: steakPricesOld } = useQuery(GET_STOCKS_LIST)
  const { loading: loading2, error: error2, data: steakList } = useQuery(GET_LIST_OF_STOCKS)
  const [seek, { loading, error, data }] = useLazyQuery(GET_NEW_LIST_OF_STOCK_PRICES)

  const [bombs, setBombs] = useState()
  const [dataLoading, setDataLoading] = useState(true)
  const [calculating, setCalculating] = useState(true)
  const [listOfBombs, setListOfBombs] = useState()
  const [inter, setInter] = useState()

  useEffect(() => {
    if (!loading1) {
      const lastFetchedDate = steakPricesOld.getAllStockPrices[0].lastfetched

      const today = new Date()
      let todayDay = today.getDate()
      let todayMonth = today.getMonth()
      let todayYear = today.getFullYear()
      let todayStr = `${todayYear}-${todayMonth}-${todayDay}`
      if (!loading2 && lastFetchedDate !== todayStr && !loading) {
        seek({
          variables: {
            lastfetched: todayStr
          }
        })
      } else {

        setBombs(steakPricesOld)
        setDataLoading(false)
      }
    }
  }, [loading, seek, loading1, loading2, steakPricesOld, steakList])
  useEffect(() => {
    if (data !== [] && !loading) {
      setBombs(() => data)
      setDataLoading(false)
    }
  }, [loading, data])


  useEffect(() => {
    function findBombStocks(stocks, weeks) {
      // console.log('steaks', stocks)
      let arrayOfBombStocks = []
      let interconnectednessCount = 0
      console.log('lleeennnggthh', stocks.length)
      for (let stock of stocks) {
        let arrayOfPrices = stock.prices.split(' ').filter(val => val !== '').map(val => parseFloat(val.replace(',', '')))
        // console.log(stock, arrayOfPrices)
        let maxPrice = Math.max(...arrayOfPrices)
        let minPrice = Math.min(...arrayOfPrices)
        let maxIndex = arrayOfPrices.indexOf(maxPrice)
        let minIndex = arrayOfPrices.indexOf(minPrice)
        let delta = maxIndex - minIndex
        let devaluation = maxPrice / minPrice
        // console.log(stock.name, maxPrice, minPrice, maxIndex, minIndex, delta, devaluation)

        if (delta > 0 && devaluation > 1.2) {
          let temp = {
            name: stock.name.toUpperCase().replace('_', " "),
            decPerc: 100 - (minPrice * 100 / maxPrice),
            maxPrice,
            maxIndex,
            minIndex,
            minPrice,
            daysSinceMin: minIndex,
            gradient: (100 - (minPrice * 100 / maxPrice)) / delta
          }
          console.log(stock, (arrayOfPrices[0] / minPrice -1)*100, minIndex )
          arrayOfBombStocks.push(temp)
          if (temp.daysSinceMin <= 10) interconnectednessCount++
        }
      }
      return { arrayOfBombStocks, interconnectednessCount }
    }

    if (bombs) {
      let { arrayOfBombStocks: bombStocks, interconnectednessCount: count } = findBombStocks(bombs.getAllStockPrices, 3)
      setListOfBombs(bombStocks)
      setInter(count)
      setCalculating(false)
    }

  }, [dataLoading, bombs, setBombs])

  return (
    <div className="my-10">
      {!calculating ? (<div>
        <h2 className="text-center uppercase text-2xl sm:text-3xl font-semibold text-indigo-600 mb-2">Bomb Stocks</h2>
        <p className="text-center">Interconnectedness of events in the last 100 days: {inter}</p>
        <div className="mt-4">
          <div className="flex mx-2 px-1 bg-indigo-600 text-sm">
            <div className="flex-1">NAME</div>
            <div className="flex-1 text-center">DIP%</div>
            <div className="flex-1 text-center">GRAD%/DAY</div>
            <div className="flex-1 text-center">$MIN</div>
            <div className="flex-1 text-right">DAYS SINCE MIN</div>
          </div>
          {listOfBombs.map((bombStock, i) => {
            return <Stock bombStock={bombStock} key={i} />
          })}
        </div>
      </div>
      ) : (
        <h2 className="text-center uppercase text-lg font-semibold">CALCULATING...</h2>
      )}
    </div >
  )



}
