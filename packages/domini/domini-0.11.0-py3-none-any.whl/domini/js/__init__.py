from typing import Union


JSONBasic = Union[None, bool, int, float, str]
JSONArray = list['JSON']
JSONObject = dict[str, 'JSON']
JSON = Union[JSONBasic, JSONArray, JSONObject]
