import graphene


class CandidateOfficeEnum(graphene.Enum):
    HOUSE = 'H'
    SENATE = 'S'
    PRESIDENT = 'P'
