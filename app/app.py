from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView
from graphene.types.schema import Schema
from graphql.execution.executors.asyncio import AsyncioExecutor
import asyncio
import os

from .handlers.query import bootstrap_queries

BASE_ROUTE = 'graphql'

app = Flask(__name__)
cors = CORS(app)

queries = bootstrap_queries()

schema = Schema(query=queries)

if os.environ['FLASK_ENV'] == 'development' or os.environ['FLASK_DEBUG'] == 1:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

app.add_url_rule(
    '/graphql', view_func=GraphQLView.as_view(BASE_ROUTE, schema=schema, graphiql=True, executor=AsyncioExecutor()))

if __name__ == '__main__':
    app.run()
