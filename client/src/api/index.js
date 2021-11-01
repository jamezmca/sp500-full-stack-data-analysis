
export async function fetchData(lFD) { 
    // console.log(dictionary)
    async function getData() { 
        const response = await fetch("dictionary.csv"); 
        const data = await response.text(); 
        console.log(data)
       } 
       getData()
    //fetches new stock data from alphavantage 


    // const url = ''
    // const apiKey = process.env.REACT_APP_API_KEY
    // try {
    //     let response = await fetch(url)
    //     let data = await response.json()

    //     return data
    // } catch (err) {
    //     console.log(err)
    // }
}
