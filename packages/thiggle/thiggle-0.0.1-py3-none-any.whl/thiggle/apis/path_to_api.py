import typing_extensions

from thiggle.paths import PathValues
from thiggle.apis.paths.v1_categorize import V1Categorize

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.V1_CATEGORIZE: V1Categorize,
    }
)

path_to_api = PathToApi(
    {
        PathValues.V1_CATEGORIZE: V1Categorize,
    }
)
