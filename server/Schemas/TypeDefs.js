const { gql } = require('apollo-server-express')

const typeDefs = gql`
    type User {
        name: String!
        age: Int!
        married: Boolean!
    }

    #can make several types in here
    
    #Queries
    type Query {
        getAllUsers: [User!]! #Returns a list of users
    }


    #Mutations
    # type Mutation {
    #     getAllUsers: 
    # }
`//can create several types in here

module.exports = { typeDefs }