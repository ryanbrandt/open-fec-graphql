# Open FEC GraphQL Server

A GraphQL wrapper around the [Open FEC API](https://api.open.fec.gov/developers/) for easier consumption

## Running Locally

### With Docker

`docker-compose up`

### With Pipenv

- `pipenv install`
- `pipenv shell`
- `pipenv run dev`

Visit the GraphiQL interface at `localhost:5000/graphql?api_key={your_open_fec_key}` to run queries in the GUI and inspect the documentation

Send queries to the server over HTTP [as documented by the GraphQL specification](https://graphql.org/learn/serving-over-http/#post-request)

#### Note: GraphiQL and HTTP Requests require `api_key={your_open_fec_key}` query parameter

If you do not have one, a key can be obtained at the [official Open FEC Site](https://api.open.fec.gov/developers/)
