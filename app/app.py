from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView
from graphene.types.schema import Schema
from graphql.execution.executors.asyncio import AsyncioExecutor

from .handlers.query import bootstrap_queries

app = Flask(__name__)
cors = CORS(app)

queries = bootstrap_queries()

schema = Schema(query=queries)

app.add_url_rule(
    '/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True, executor=AsyncioExecutor()))

if __name__ == '__main__':
    app.run(debug=True)
