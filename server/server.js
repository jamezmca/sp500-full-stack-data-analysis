const { ApolloServer } = require("apollo-server-express")
const express = require('express')
const cors = require('cors')
const { typeDefs } = require("./Schemas/TypeDefs")
const { resolvers } = require("./Schemas/resolvers")


async function startApolloServer() {
    // const corsOptions = {
    //     origin: 'http://localhost:3000',
    //     credentials: true
    // }
    const server = new ApolloServer({
        typeDefs, resolvers
    })
    // cors: {
    // 	origin: '*',			// <- allow request from all domains
    // 	credentials: true},
    await server.start()

    const app = express()
    app.use(cors())
    // server.applyMiddleware({ app, path: "/graphql", cors: false })
    server.applyMiddleware({ app })


    app.listen(5000, () => {
        console.log('Server has started on port 5000')
    })
}
startApolloServer()


