from opnsense_api.base_client import BaseClient
from opnsense_api.pydantic.Cert import Cert
from opnsense_api.pydantic.SearchResult import CertSearchResult, SearchResult


class TrustCertClient(BaseClient):

    def trust_cert_search(self) -> CertSearchResult:
        data = self._get('trust/cert/search')
        return SearchResult.from_ui_dict(data, Cert)

    def trust_cert_get(self, uuid):
        data = self._get('trust/cert/get/' + str(uuid))
        return Cert.from_ui_dict(data)
