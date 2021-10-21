const express = require('express')
const app = express()
const cors = require('cors')
const pool = require('./db')
const { graphqlHTTP } = require('express-graphql')

const schema = require('./Schemas')

//middleware
// app.use(cors())
// app.use(express.urlencoded({ extended: true }));
// app.use(express.json()) //req.body

//Routes//




app.use('/graphql', graphqlHTTP({ //Graphql route
    schema,
    graphiql: true
}))

app.listen(5000, () => {
    console.log('Server has started on port 5000')
})