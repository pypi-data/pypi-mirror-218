from dataclasses import dataclass
from feedancy.lib.client import ApiClient
from feedancy.lib.configuration import Configuration
from feedancy.lib.adapter.base import HttpClientAdapter


from .apis.api.api import ApiApi



@dataclass
class AutogeneratedApiClient:
    configuration: Configuration
    client: ApiClient
    api: ApiApi


def new_client(
    adapter: HttpClientAdapter, configuration: Configuration
) -> AutogeneratedApiClient:
    client = ApiClient(configuration=configuration, adapter=adapter)
    return AutogeneratedApiClient(
        configuration,
        client=client,
        
        api=ApiApi(client, configuration)
        
    )