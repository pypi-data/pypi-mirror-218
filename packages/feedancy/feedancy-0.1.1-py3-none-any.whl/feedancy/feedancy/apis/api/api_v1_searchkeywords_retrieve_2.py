from __future__ import annotations

import datetime
import pydantic
import typing

from pydantic import BaseModel

from feedancy.lib.base import BaseApi
from feedancy.lib.request import ApiRequest
from feedancy.lib import json
class SearchKeywords(BaseModel):
    id: int 
    name: str 
    stop_keywords: typing.List[int] 

def make_request(self: BaseApi,


    id: str,

) -> SearchKeywords:
    

    
    body = None
    

    m = ApiRequest(
        method="GET",
        path="/api/v1/searchkeywords/{id}/".format(
            
                id=id,
            
        ),
        content_type=None,
        body=body,
        headers=self._only_provided({
        }),
        query_params=self._only_provided({
        }),
        cookies=self._only_provided({
        }),
    )
    return self.make_request({
    
        "200": {
            
                "application/json": SearchKeywords,
            
        },
    
    }, m)