import asyncio
import os
from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView
from graphene.types.schema import Schema
from graphql.execution.executors.asyncio import AsyncioExecutor
from dotenv import load_dotenv

from .handlers.query import bootstrap_queries
from app.middleware.complexity_limit_middleware import ComplexityLimitMiddleware

BASE_ROUTE = 'graphql'


def create_app() -> Flask:
    app = Flask(__name__)
    cors = CORS(app)

    queries = bootstrap_queries()
    schema = Schema(query=queries)

    complexity_middleware = ComplexityLimitMiddleware()

    if os.environ['FLASK_ENV'] == 'development' or os.environ['FLASK_DEBUG'] == 1:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    app.add_url_rule(
        '/graphql', view_func=GraphQLView.as_view(BASE_ROUTE, schema=schema, graphiql=True, executor=AsyncioExecutor(), graphiql_html_title='Open FEC GraphiQL', middleware=[complexity_middleware]))

    return app


if __name__ == '__main__':
    if os.environ['FLASK_ENV'] == 'development':
        load_dotenv()

    flask_app = create_app()
    flask_app.run()
