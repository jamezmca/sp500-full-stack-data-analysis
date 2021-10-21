const express = require('express')
const app = express()
const cors = require('cors')
const pool = require('./db')


//middleware
app.use(cors())
app.use(express.urlencoded({extended: true})); 
app.use(express.json()) //req.body

//Routes//

//Create a todo
app.post('/todos', async (req, res) => {
    try {
        console.log(req.body)
        res.send({'bod': req.body}).status(200)
    } catch (err) {
        console.error(err.messages)
    }
})


//Get a todo

//get all todos

//update a todo

//delete a todo 

app.listen(5000, () => {
    console.log('Server has started on port 5000')
})