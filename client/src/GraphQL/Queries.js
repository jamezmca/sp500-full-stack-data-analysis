import { gql } from '@apollo/client'

export const GET_STOCKS_LIST = gql`
query Query {
  getAllStockPrices {
    name
    prices
    lastfetched
  }
}
`
export const GET_PNGS = gql`
query Query {
  getPngs {
    name
    encode
  }
}
`
export const GET_RISK_REWARD = gql`
query Query {
  getRiskReward {
    name
    reward
    risk
  }
}
`

export const GET_LIST_OF_STOCKS = gql`
query Query {
  getStockList {
    names
  }
}
`

export const GET_NEW_LIST_OF_STOCK_PRICES = gql`
query Query {
  getStockList {
    names
  }
}
`