const { gql } = require('apollo-server-express')

const typeDefs = gql`
    type Stock {
        stock_id: Int!
        name: String!
        price1: Int!
        price2: Int!
        price3: Int!
        price4: Int!
        price5: Int!
        price6: Int!
        price7: Int!
        price8: Int!
        price9: Int!
        price10: Int!
        price11: Int!
        price12: Int!
        price13: Int!
        price14: Int!
        
    }

    type Handy {
        name: String!
        married: Boolean!
    }

    #can make several types in here
    
    #Queries
    type Query {
        getAllStockPrices: [Stock!]!,         #Returns a list of users
        greeting: String!,
        practice: [Handy!]!,
    }


    #Mutations
    type Mutation {
        addStock(
            stock_id: Int!
            name: String!, 
            price1: Int!,
            price2: Int!,
            price3: Int!,
            price4: Int!,
            price5: Int!,
            price6: Int!,
            price7: Int!,
            price8: Int!,
            price9: Int!,
            price10: Int!,
            price11: Int!,
            price12: Int!,
            price13: Int!,
            price14: Int!
            ): Stock!
    }
`//can create several types in here

module.exports = { typeDefs }