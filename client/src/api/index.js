const axios = require('axios')

export async function fetchData(steak) {
    const apiKey = process.env.REACT_APP_API_KEY
    const url = `https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=${steak}&apikey=${apiKey}`
    try {
        let { data } = await axios.get(url)
        // let res = await data.json()
        console.log(data)
        return data
        // let priceStr = ''
        // for (const [key, value] of Object.entries(data['Time Series (Daily)'])) {
        //     priceStr += `${value['5. adjusted close']} `
        // }
        // console.log({name: steak, prices: priceStr})
        // return {name: steak, prices: priceStr}
    } catch (err) {
        console.log(err)
    }
}
