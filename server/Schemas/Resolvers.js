//connect with DB in here
const pool = require('../db')
//localhost:5000/graphql
const axios = require('axios')
const cheerio = require('cheerio')

//1st - query database for all latest data points
//2nd - check what data is or is not there
//3rd - post any additional data to the database
// df_last_six_weeks | df_encoded | df_stock_return_risk

const resolvers = {
    Query: {
        getAllStockPrices: async () => {
            const client = await pool.connect()
            let persist
            try {
                const res = await client.query('SELECT * FROM df_last_six_weeks')
                persist = res.rows.map(row => row)
            } catch (err) {
                console.log(err)
            } finally {
                // Make sure to release the client before any error handling,
                // just in case the error handling itself throws an error.
                client.release()
                return persist
            }
        },
        getPngs: async () => {
            const client = await pool.connect()
            let persist
            try {
                const res = await client.query('SELECT * FROM df_encoded')
                persist = res.rows.map(row => row)
            } catch (err) {
                console.log(err)
            } finally {
                // Make sure to release the client before any error handling,
                // just in case the error handling itself throws an error.
                client.release()
                return persist
            }
        },
        getRiskReward: async () => {
            const client = await pool.connect()
            let persist
            try {
                const res = await client.query('SELECT * FROM df_stock_return_risk')
                persist = res.rows.map(row => row)
            } catch (err) {
                console.log(err)
            } finally {
                // Make sure to release the client before any error handling,
                // just in case the error handling itself throws an error.
                client.release()
                return persist
            }
        },
        getStockList: async (_, args) => {
            console.log('args', args)
            let url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
            const { data } = await axios.get(url, {
                headers: {
                    'Access-Control-Allow-Origin': '*',
                },
            })
            const $ = cheerio.load(data)
            const listOfStocks = $('tbody tr td .external').text().replaceAll('reports', " ")
            return {names: listOfStocks}
        }
        // practice: () => ([{ name: "hello", married: true }]),

    },
    Mutation: {
        addStock: async (_, args) => {
            //make SQL statements
            const newDay = args
            const client = await pool.connect()
            console.log(args) // want to have args inserted in
            try {
                let str = 'name, price1, price2, price3, price4, price5, price6, price7, price8, price9, price10, price11, price12, price13, price14'
                let demo = ["howdy", 1, 3, 5, 7, 5, 3, 1, 3, 5, 7, 8, 19, 14, 29]
                const res = await client.query(`INSERT INTO twoweekprices (${str}) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)`, demo)//don't need column name
                console.log('hello')
            } catch (err) {
                console.log(err)
            } finally {
                // Make sure to release the client before any error handling,
                // just in case the error handling itself throws an error.
                client.release()
            }
            return args

        }
    }
}

module.exports = { resolvers }