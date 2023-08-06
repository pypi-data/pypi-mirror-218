import typing_extensions

from thiggle.apis.tags import TagValues
from thiggle.apis.tags.thiggle_api import ThiggleApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.THIGGLE: ThiggleApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.THIGGLE: ThiggleApi,
    }
)
