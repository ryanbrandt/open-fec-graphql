import asyncio
import os
from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView
from graphene.types.schema import Schema
from graphql.execution.executors.asyncio import AsyncioExecutor


from .handlers.query import bootstrap_queries

BASE_ROUTE = 'graphql'


def create_app() -> Flask:
    app = Flask(__name__)
    cors = CORS(app)

    queries = bootstrap_queries()

    schema = Schema(query=queries)

    if os.environ['FLASK_ENV'] == 'development' or os.environ['FLASK_DEBUG'] == 1:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    app.add_url_rule(
        '/graphql', view_func=GraphQLView.as_view(BASE_ROUTE, schema=schema, graphiql=True, executor=AsyncioExecutor(), graphiql_html_title='Open FEC GraphiQL'))

    return app


if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run()
