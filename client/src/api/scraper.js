const axios = require('axios')
const cheerio = require('cheerio')
export async function getIndexStocks(url) {
    const { data } = await axios.get(url)
    const $ = cheerio.load(data)
    const table =$('a.external.text', data)

}