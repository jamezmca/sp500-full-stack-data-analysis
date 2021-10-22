const Pool = require('pg').Pool //could also use knox

//psql -U postgres in terminal
const pool = new Pool({
    user: "postgres",
    password: "",
    host: "localhost",
    port: 5432,
    database: "stockprices"
})

module.exports = pool