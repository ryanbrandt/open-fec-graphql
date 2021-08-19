import json
from graphql.backend.core import GraphQLCoreBackend
from graphql.error import GraphQLError
from graphene import ResolveInfo

from app.utils.setup_logger import get_logger


class ComplexityLimitMiddleware(GraphQLCoreBackend):
    LOGGER = get_logger(__name__)

    MAXIMUM_DEPTH = 5

    def measure_depth(self, selection_set, level=1):
        max_depth = level

        for field in selection_set.selections:
            if field.selection_set:
                new_depth = self.measure_depth(
                    field.selection_set, level=level + 1)
                if new_depth > max_depth:
                    max_depth = new_depth

        return max_depth

    async def resolve(self, next, root, info: ResolveInfo, *args, **kwargs):
        try:
            parsed_body = json.loads(info.context.data)

            document = super().document_from_string(
                info.schema, parsed_body['query'])
            ast = document.document_ast

            for definition in ast.definitions:
                if definition.operation != 'query':
                    continue

                depth = self.measure_depth(definition.selection_set)

                if depth > ComplexityLimitMiddleware.MAXIMUM_DEPTH:
                    raise GraphQLError(
                        f'Maximum query depth of {ComplexityLimitMiddleware.MAXIMUM_DEPTH} exceeded')

        except Exception as e:
            ComplexityLimitMiddleware.LOGGER.info(e)

        return await next(root, info, *args, **kwargs)
