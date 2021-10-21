//connect with DB in here
const pool = require('../db')

//1st - query database for all latest data points
//2nd - check what data is or is not there
//3rd - post any additional data to the database
// 1
const resolvers = {
    Query: {
        getAllStockPrices() {
            // async/await - check out a client
            ; (async () => {
                const client = await pool.connect()
                let persist = []
                try {
                    const res = await client.query('SELECT * FROM twoweekprices')
                    persist = res.rows.map(row => {
                        console.log('aloha', row)
                        return row
                    })
                    console.log(persist)
                } catch (err) {
                    console.log(err)
                } finally {
                    // Make sure to release the client before any error handling,
                    // just in case the error handling itself throws an error.
                    client.release()
                    return persist

                }
            })().catch(err => console.log(err.stack))
            //make return data statement
            //write fetch statement from db
            console.log('coolio')
            return 'hello'//returns like res.send
        },
        greeting: async () => {
                const client = await pool.connect()
                let persist = 'aloha'
                try {
                    const res = await client.query('SELECT * FROM twoweekprices')
                    persist = res.rows[0].name
                    
                    console.log(persist)
                } catch (err) {
                    console.log(err)
                } finally {
                    // Make sure to release the client before any error handling,
                    // just in case the error handling itself throws an error.
                    client.release()
                    return persist

                }
            },
        practice: () => ([{name:"hello", married: true}]),

    },
    Mutation: {
        addStock(parent, args) {
            //make SQL statements
            const newDay = args
            //write insert statement into db
            return newUser
        }
    }
}

module.exports = { resolvers }