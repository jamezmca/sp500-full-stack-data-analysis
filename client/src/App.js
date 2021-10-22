import {
  ApolloClient,
  InMemoryCache,
  ApolloProvider,
  useQuery,
  gql
} from "@apollo/client"
import './App.css'
import Header from "./Components/Header";
import Report from "./Components/Report";
import DataPipeline from "./Components/DataPipeline";
import StockList from "./Components/StockList"
import Footer from "./Components/Footer";

//Apollo client setup 
const client = new ApolloClient({
  uri: 'http://localhost:5000/graphql',
  cache: new InMemoryCache()

})

function App() {
  return (
    <ApolloProvider client={client}>
      <div className="app">
        <main className="main">
          <Header />
          <body className="body">
            <Report />
            <DataPipeline />
            <StockList />
          </body>
          <Footer />
        </main>
      </div>
    </ApolloProvider>

  );
}

export default App;
