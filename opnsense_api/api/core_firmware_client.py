import time

from opnsense_api.base_client import BaseClient
from opnsense_api.pydantic.FirmwareInfo import FirmwareInfo
from opnsense_api.pydantic.PluginDetail import PluginDetail
from opnsense_api.pydantic.Status import Status
from opnsense_api.pydantic.UpdateStatus import UpdateStatus


class CoreFirmwareClient(BaseClient):

    def core_firmware_status(self) -> UpdateStatus:
        data = self._get('core/firmware/status')
        return UpdateStatus(**data)

    def core_firmware_info(self) -> FirmwareInfo:
        data = self._get('core/firmware/info')
        return FirmwareInfo(**data)

    def core_firmware_install(self, package_name) -> Status:
        data = self._post('core/firmware/install/'+package_name, '')
        return Status(**data)

    def core_firmware_detail(self, package_name) -> PluginDetail:
        data = self._post('core/firmware/details/'+package_name, '')
        return PluginDetail(**data)

    def package_install_wait(self, package_name):
        self.core_firmware_install(package_name)
        info = self.core_firmware_info()
        installed = info.is_installed(package_name)
        while not installed:
            time.sleep(5)
            installed = info.is_installed(package_name)
