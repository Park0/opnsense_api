from opnsense_api.base_client import BaseClient
from opnsense_api.pydantic.Result import Result
from opnsense_api.pydantic.Status import Status


class HaproxyServiceClient(BaseClient):

    def haproxy_service_configtest(self):
        data = self._get('haproxy/service/configtest')
        # print(data)
        return Result(**data)

    def haproxy_service_reconfigure(self):
        data = self._post('haproxy/service/reconfigure', '')
        # print(data)
        return Status(**data)
