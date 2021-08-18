import graphene

from app.models.dicts.fec_pagination_search_filter_dict import FecPaginationSearchFilterDict


class BaseGraphQLFilter(graphene.InputObjectType):
    page = graphene.Int(required=False, default=None)
    per_page = graphene.Int(required=False, default=None)

    def __init__(self, page=None, per_page=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.per_page = per_page

    def build_api_filter_dict(self) -> dict:
        filter_dict: FecPaginationSearchFilterDict = {}

        if self.page:
            filter_dict['page'] = int(self.page)

        if self.per_page:
            filter_dict['per_page'] = int(self.per_page)

        return filter_dict
