from opnsense_api.base_client import BaseClient
from opnsense_api.pydantic.Certificate import Certificate
from opnsense_api.pydantic.Response import Response
from opnsense_api.pydantic.Result import Result
from opnsense_api.pydantic.SearchRequest import SearchRequest
from opnsense_api.pydantic.SearchResult import BaseObjectSearchResult, CertificateSearchResult


class AcmeclientCertificatesClient(BaseClient):

    def acmeclient_certificates_get(self, uuid = None) -> Certificate:
        data = self._get('acmeclient/certificates/get' + self._get_arg_formatter(uuid))
        # print(data)
        return Certificate.from_ui_dict(data)

    def acmeclient_certificates_search(self, search: SearchRequest = None) -> CertificateSearchResult:
        data = self._post('acmeclient/certificates/search', search)
        # print(data)
        return CertificateSearchResult.from_basic_dict(data, Certificate)

    def acmeclient_certificates_add(self, item: Certificate):
        data = self._post('acmeclient/certificates/add', item)
        # print(data)
        return Result.from_ui_dict(data)

    def acmeclient_certificates_sign(self, uuid = None):
        data = self._post('acmeclient/certificates/sign' + self._get_arg_formatter(uuid), '')
        # print(data)
        return Response.from_basic_dict(data)
