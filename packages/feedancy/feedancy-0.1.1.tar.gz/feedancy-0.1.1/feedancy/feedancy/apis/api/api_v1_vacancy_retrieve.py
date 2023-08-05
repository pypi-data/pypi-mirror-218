from __future__ import annotations

import datetime
import pydantic
import typing

from pydantic import BaseModel

from feedancy.lib.base import BaseApi
from feedancy.lib.request import ApiRequest
from feedancy.lib import json
class Vacancy(BaseModel):
    company: typing.Optional[typing.Union[int, None]]  = None
    contract_type: typing.Optional[typing.Union[typing.Union[str, str, str], None]]  = None
    employment_format: typing.Optional[typing.Union[typing.Union[str, str, str], None]]  = None
    experience: typing.Optional[typing.Union[typing.Union[str, str, str], None]]  = None
    external_id: str 
    has_insurance: typing.Optional[typing.Union[bool, None]]  = None
    has_portfolio: typing.Optional[typing.Union[bool, None]]  = None
    has_test_task: typing.Optional[typing.Union[bool, None]]  = None
    id: int 
    is_relocation_required: typing.Optional[typing.Union[bool, None]]  = None
    link: str 
    name: str 
    publicated_at: typing.Optional[typing.Union[datetime.datetime, None]]  = None
    raw_description: typing.Optional[typing.Union[str, None]]  = None
    requirement: typing.Optional[typing.Union[str, None]]  = None
    responsibility: typing.Optional[typing.Union[str, None]]  = None
    salary: typing.Optional[typing.Union[int, None]]  = None
    source: int 
    test_task_link: typing.Optional[typing.Union[str, None]]  = None
    work_format: typing.Optional[typing.Union[typing.Union[str, str, str], None]]  = None

def make_request(self: BaseApi,


    id: str,

) -> Vacancy:
    

    
    body = None
    

    m = ApiRequest(
        method="GET",
        path="/api/v1/vacancy/{id}/".format(
            
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
            
                "application/json": Vacancy,
            
        },
    
    }, m)