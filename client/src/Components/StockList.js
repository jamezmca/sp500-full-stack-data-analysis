import React from 'react'
import { gql, useQuery } from "@apollo/client"

//information will be stock_id | name | lastfetched | 'prices x 14 in CSV format'
const GET_STOCKS_LIST = gql`
query Query {
  getAllStockPrices {
    name
  }
}
`

//i want some logic that fetches data from a react hook depending on when the last entry was from 

export default function StockList() {
    const { loading, error, data } = useQuery(GET_STOCKS_LIST);
    if (!loading) {
        console.log(data)
    }
    return (
        <div>

        </div>
    )
}
