import graphene

from app.models.dicts.fec_pagination_search_filter_dict import FecPaginationSearchFilterDict


class BaseGraphQLFilter(graphene.InputObjectType):
    id_in = graphene.List(graphene.String, required=False, default=None)
    page = graphene.Int(required=False, default=None)

    def __init__(self, id_in=None, page=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id_in = id_in
        self.page = page

    def build_api_filter_dict(self) -> dict:
        filter_dict: FecPaginationSearchFilterDict = {}

        if self.page:
            filter_dict['page'] = int(self.page)

        return filter_dict
