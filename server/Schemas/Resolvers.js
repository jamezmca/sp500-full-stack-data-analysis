//connect with DB in here
const pool = require('../db')

//1st - query database for all latest data points
//2nd - check what data is or is not there
//3rd - post any additional data to the database
// 1
const resolvers = {
    Query: {
        getAllStockPrices: async () => {
                const client = await pool.connect()
                let persist
                try {
                    const res = await client.query('SELECT * FROM twoweekprices')
                    persist = res.rows.map(row => {
                        console.log(row)
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