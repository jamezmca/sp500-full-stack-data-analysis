import { gql } from '@apollo/client'

export const UPDATE_STOCK_PRICES = gql`
mutation updateStocks(
    [$name: String!
    $lastfetched: String!
    $prices: String!]
) {
  updateStocks(
      [name: $name
      lastfetched: $lastfetched
      prices: $prices]
  ) {
    name
  }
}
`