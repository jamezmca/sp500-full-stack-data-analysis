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
        getStockHistory: async (_, { lastfetched }) => {
            const hello = require('./james.json')

            //args is an array of stocks
            console.log({ lastfetched })
            let url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
            const { data } = await axios.get(url, {
                headers: {
                    'Access-Control-Allow-Origin': '*',
                },
            })
            const $ = cheerio.load(data)
            const listOfStocks = $('tbody tr td .external').text().replaceAll('reports', " ")
            let arguments = ['aapl', 'amzn', 'grmn']
            async function getPrices(steakList) {
                let newFetchStockPrices2 = []
                console.log(steakList)

                await Promise.all(steakList.split(' ').map(async (ticker) => {
                    let url = `https://finance.yahoo.com/quote/${ticker}/history?p=${ticker}`
                    const { data } = await axios.get(url, {
                        headers: {
                            'Access-Control-Allow-Origin': '*',
                        },
                    })
                    // console.log('found stock data', ticker)
                    const $ = cheerio.load(data)
                    const strOfStocks = $('tbody tr td:nth-child(5)').text()
                    let listOfStocks = ""
                    let prevIndex = 0
                    for (let i = 0; i < strOfStocks.length; i++) {
                        if (strOfStocks[i] == '.') {
                            listOfStocks += strOfStocks.slice(prevIndex, i + 3) + " "
                            prevIndex = i + 3
                        }
                    }
                    if (ticker == "TSLA") {
                        console.log(strOfStocks)
                    }
                    newFetchStockPrices2.push({ name: ticker, prices: listOfStocks })
                }))
                const client = await pool.connect()
                try {
                    await client.query(`DROP TABLE IF EXISTS df_last_six_weeks;`)//don't need column name
                    await client.query(`CREATE TABLE df_last_six_weeks (
                        name VARCHAR,
                        lastFetched VARCHAR,
                        prices VARCHAR
                    );`)//don't need column name
                    let str = 'name, lastfetched, prices'
                    // for (let stack of hello.data.getStockHistory) {
                    for (let stack of newFetchStockPrices2) {
                        let demo = [stack.name, lastfetched, stack.prices]
                        const res = await client.query(`INSERT INTO df_last_six_weeks (${str}) VALUES ($1, $2, $3)`, demo)//don't need column name
                    }
                } catch (err) {
                    console.log(err)
                } finally {
                    console.log('end of function')
                    client.release()
                }

                return newFetchStockPrices2
            }

            let newFetchStockPrices = getPrices(listOfStocks)
            return newFetchStockPrices
        }
        // practice: () => ([{ name: "hello", married: true }]),

    },
    Mutation: {

    }
}

module.exports = { resolvers }