from opnsense_api.base_client import BaseClient
from opnsense_api.pydantic.Ca import Ca
from opnsense_api.pydantic.SearchResult import CaSearchResult


class TrustCaClient(BaseClient):

    def trust_ca_search(self) -> CaSearchResult:
        data = self._get('trust/ca/search')
        # print(data)
        return CaSearchResult.from_ui_dict(data, Ca)

    def trust_ca_get(self, uuid):
        data = self._get('trust/ca/get/' + str(uuid))
        # print(data)
        return Ca.from_ui_dict(data)
