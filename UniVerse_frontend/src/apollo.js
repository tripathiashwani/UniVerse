// // src/apollo.js
// import { ApolloClient, InMemoryCache, HttpLink } from '@apollo/client';

// const httpLink = new HttpLink({
//   uri: 'http://127.0.0.1:8000/graphql/',
// });

// const client = new ApolloClient({
//   link: httpLink,
//   cache: new InMemoryCache(),
// });

// export default client;
// src/apollo.js
// src/apollo.js
// src/apollo.js
import { ApolloClient, InMemoryCache, createHttpLink } from '@apollo/client/core';
import { setContext } from '@apollo/client/link/context';

// Create an http link:
const httpLink = createHttpLink({
  uri: 'http://127.0.0.1:8000/graphql/', // Replace with your GraphQL endpoint
});

// Create an auth link to include authentication headers
const authLink = setContext((_, { headers }) => {
  // Get the authentication token from local storage if it exists
  const token = localStorage.getItem('auth_token');
  
  // Return the headers to the context so httpLink can read them
  return {
    headers: {
      ...headers,
      authorization: token ? `Bearer ${token}` : "",
    }
  };
});

// Combine the auth link and http link
const link = authLink.concat(httpLink);

// Create the Apollo Client
const apolloClient = new ApolloClient({
  link,
  cache: new InMemoryCache(),
});

export default apolloClient;
