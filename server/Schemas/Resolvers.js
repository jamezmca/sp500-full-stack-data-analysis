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
                // console.log('hello',persist)
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
            return { names: listOfStocks }
        },
        getStockHistory: async (_, args) => {
            const hello = require('./james.json')
            console.log(hello)
            //args is an array of stocks
            console.log(args)
            let url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
            const { data } = await axios.get(url, {
                headers: {
                    'Access-Control-Allow-Origin': '*',
                },
            })
            const $ = cheerio.load(data)
            const listOfStocks = $('tbody tr td .external').text().replaceAll('reports', " ")
            let arguments = ['aapl', 'amzn', 'grmn']
            let newFetchStockPrices = []
            // for (const ticker of listOfStocks.split(' ')) {
            //     if (ticker.length > 0) {
            //         let url = `https://finance.yahoo.com/quote/${ticker}/history?p=${ticker}`

            //         const { data } = await axios.get(url, {
            //             headers: {
            //                 'Access-Control-Allow-Origin': '*',
            //             },
            //         })

            //         const $ = cheerio.load(data)
            //         const strOfStocks = $('tbody tr td:nth-child(5)').text()
            //         let listOfStocks = ""
            //         let prevIndex = 0
            //         for (let i = 0; i < strOfStocks.length; i++) {
            //             if (strOfStocks[i] == '.') {
            //                 listOfStocks += strOfStocks.slice(prevIndex, i + 3) + " "
            //                 prevIndex = i + 3
            //             }
            //         }
            //         newFetchStockPrices.push({ name: ticker, prices: listOfStocks })
            //     }

            //     console.log(ticker)
            // }

            const client = await pool.connect()
            try {
                let str = 'name, lastfetched, prices'
                await client.query(`DROP TABLE twoweekprices;`)//don't need column name
                for (let stack of hello.data.getStockHistory) {
                // for (let stack of newFetchStockPrices) {
                    let demo = [stack.name, lastfetched, stack.prices]
                    const res = await client.query(`INSERT INTO twoweekprices (${str}) VALUES ($1, $2, $3)`, demo)//don't need column name

                }

                console.log('hello')
            } catch (err) {
                console.log(err)
            } finally {
                // Make sure to release the client before any error handling,
                // just in case the error handling itself throws an error.
                client.release()
            }

            return newFetchStockPrices
        }
        // practice: () => ([{ name: "hello", married: true }]),

    },
    Mutation: {
        
    }
}

module.exports = { resolvers }