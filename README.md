# Open FEC GraphQL Server

[![ryanbrandt](https://circleci.com/gh/ryanbrandt/open-fec-graphql.svg?style=svg)](https://app.circleci.com/pipelines/github/ryanbrandt/open-fec-graphql)

A GraphQL wrapper around the [Open FEC API](https://api.open.fec.gov/developers/) for easier consumption

#### Tech:

1. Flask
2. Graphene
3. Redis

## Running Locally

Requires Docker

#### Build

`docker-compose up --build`

#### Run:

`docker-compose up`

Visit the GraphiQL interface at `localhost:5000/graphql?api_key={your_open_fec_key}` to run queries in the GUI and inspect the documentation

Send queries to the server over HTTP [as documented by the GraphQL specification](https://graphql.org/learn/serving-over-http/#post-request)

### Note:

GraphiQL and HTTP Requests require `api_key={your_open_fec_key}` query parameter

If you do not have one, a key can be obtained at the [official Open FEC Site](https://api.open.fec.gov/developers/)
