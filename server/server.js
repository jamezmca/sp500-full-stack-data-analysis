const { ApolloServer } = require("apollo-server-express")
const express = require('express')
const cors = require('cors')
const { typeDefs } = require("./Schemas/TypeDefs")
const { resolvers } = require("./Schemas/resolvers")


async function startApolloServer() {
    const server = new ApolloServer({ typeDefs, resolvers })
    await server.start()

    const app = express()
    app.use(cors())
    server.applyMiddleware({ app, cors: true })


    app.listen(5000, () => {
        console.log('Server has started on port 5000')
    })
}
startApolloServer()


