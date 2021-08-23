import graphene


class CandidatePartyEnum(graphene.Enum):
    DEMOCRAT = 'DEM'
    REPUBLICAN = 'REP'
    LIBERTARIAN = 'LIB'
    GREEN = 'GRE'
    SOCIALIST = 'SOC'
