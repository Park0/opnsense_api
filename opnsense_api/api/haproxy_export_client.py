from opnsense_api.base_client import BaseClient
from opnsense_api.pydantic.Response import Response


class HaproxyExportClient(BaseClient):

    def haproxy_export_config(self):
        data = self._get('haproxy/export/config')
        return Response(**data)
