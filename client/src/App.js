import {
  ApolloClient,
  InMemoryCache,
  ApolloProvider,
  useQuery,
  gql
} from "@apollo/client"
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
      <div className="bg-primary text-white min-h-screen p-4">
          <Header />
          <div className="max-w-prose	m-auto text-justify">
            <Report />
            <DataPipeline />
            <StockList />
          </div>
          <Footer />
      </div>
    </ApolloProvider>

  );
}

export default App;
