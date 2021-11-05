import {
  ApolloClient,
  InMemoryCache,
  ApolloProvider,
  useQuery,
  gql,
  HttpLink,
  from
} from "@apollo/client"
import { onError } from '@apollo/client/link/error' //error library

import Header from "./Components/Header";
import Report from "./Components/Report";
import DataPipeline from "./Components/DataPipeline";
import StockList from "./Components/StockList"
import Footer from "./Components/Footer";

//Apollo client setup 
const errorLink = onError(({ graphqlErrors, networkError }) => {
  if (graphqlErrors) {
    graphqlErrors.map(({ message, location, path }) => {
      return alert(`GraphQL error ${message}`)
    })
  }
})

const link = from([
  errorLink,
  new HttpLink({ uri: 'http://localhost:5000/graphql' })
])

const client = new ApolloClient({
  link: link, //uri: 'http://localhost:5000/graphql',
  cache: new InMemoryCache(),


})

function App() {
  return (
    <ApolloProvider client={client}>
      <div className="bg-secondary text-white min-h-screen flex flex-col font-body ">
        <Header />
        <div className="max-w-prose	m-auto text-justify flex-grow px-8">
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
