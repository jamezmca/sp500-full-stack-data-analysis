const {Client} = require('pg')
//psql -U postgres in terminal
const client = new Client({
    user: "postgres",
    password: "",
    host: "localhost",
    port: 5432,
    database: "stockprices"
})

client.connect()
.then(() => console.log('Successfully connected'))
.then(() => client.query("SELECT * FROM twoweekprices"))
.then(result => console.table(result.rows))
.then(e => console.log)
.finally(() => client.end())