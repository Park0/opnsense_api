from opnsense_api.base_client import BaseClient
from opnsense_api.pydantic.Cert import Cert
from opnsense_api.pydantic.CertBase import CertBase
from opnsense_api.pydantic.SearchResult import CertSearchResult, CertBaseSearchResult


class TrustCrlClient(BaseClient):

    def trust_crl_search(self) -> CertSearchResult:
        data = self._get('trust/crl/search')
        data['rows'] = [x for x in data['rows'] if not (x.get("refid") == "" and x.get("descr") == "")]
        data['rowCount'] = len(data['rows'])
        return CertBaseSearchResult.from_ui_dict(data, CertBase)

    def trust_crl_get(self, uuid):
        data = self._get('trust/crl/get/' + str(uuid))
        return Cert.from_ui_dict(data)
