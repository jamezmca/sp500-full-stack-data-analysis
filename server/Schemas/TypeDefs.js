const { gql } = require('apollo-server-express')

const typeDefs = gql`
    type Stock {
        name: String!
        lastfetched: String!
        prices: String!
    }

    type AddStock {
        name: String!
        price1: Int!
        price2: Int!
    }

    type Pngs {
        name: String!
        encode: String!
    }

    type Risk {
        name: String!
        reward: Float
        risk: Float
    }

    type stockList {
        names: String!
    }
    #can make several types in here
    
    #Queries
    type Query {
        getAllStockPrices: [Stock!]!,   
        getPngs: [Pngs!]!,
        getRiskReward: [Risk!]!,
        getStockList: stockList!

      #Returns a list of users
    }

    #Mutations
    type Mutation {
        addStock(
            stock_id: Int!
            name: String!, 
            price1: Int!,
            price2: Int!,

            ): Stock!
    }
`//can create several types in here

module.exports = { typeDefs }