import os
import tempfile
from unittest import TestCase
from unittest.mock import patch

from opnsense_api.api.core_backup_client import CoreBackupClient
from opnsense_api.client import Client


SAMPLE_CONFIG_XML = """<?xml version="1.0"?>
<opnsense>
  <system>
    <hostname>OPNsense</hostname>
    <domain>localdomain</domain>
  </system>
</opnsense>"""


class TestCoreBackup(TestCase):
    """Tests for Core Backup client using mocked API responses"""

    PROVIDERS_RESPONSE = {
        "this": {"name": "This Firewall", "type": "local"}
    }

    BACKUPS_RESPONSE = {
        "backups": [
            {"time": "2026-02-10T12:00:00", "description": "auto backup"},
            {"time": "2026-02-09T12:00:00", "description": "manual backup"}
        ]
    }

    DELETE_RESPONSE = {"status": "ok"}
    REVERT_RESPONSE = {"status": "ok"}

    def test_client_has_backup_methods(self):
        """Test that Client inherits CoreBackupClient methods"""
        self.assertTrue(hasattr(Client, 'core_backup_backups'))
        self.assertTrue(hasattr(Client, 'core_backup_providers'))
        self.assertTrue(hasattr(Client, 'core_backup_download'))
        self.assertTrue(hasattr(Client, 'core_backup_download_to_file'))
        self.assertTrue(hasattr(Client, 'core_backup_diff'))
        self.assertTrue(hasattr(Client, 'core_backup_delete'))
        self.assertTrue(hasattr(Client, 'core_backup_revert'))

    @patch.object(CoreBackupClient, '_get')
    def test_providers(self, mock_get):
        """Test listing backup providers"""
        mock_get.return_value = self.PROVIDERS_RESPONSE

        client = Client.__new__(Client)
        result = client.core_backup_providers()

        self.assertIn("this", result)
        mock_get.assert_called_once_with('core/backup/providers')

    @patch.object(CoreBackupClient, '_get')
    def test_backups_default_host(self, mock_get):
        """Test listing backups with default host"""
        mock_get.return_value = self.BACKUPS_RESPONSE

        client = Client.__new__(Client)
        result = client.core_backup_backups()

        self.assertIn("backups", result)
        self.assertEqual(len(result["backups"]), 2)
        mock_get.assert_called_once_with('core/backup/backups/this')

    @patch.object(CoreBackupClient, '_get')
    def test_backups_custom_host(self, mock_get):
        """Test listing backups with custom host"""
        mock_get.return_value = self.BACKUPS_RESPONSE

        client = Client.__new__(Client)
        client.core_backup_backups(host='remote')

        mock_get.assert_called_once_with('core/backup/backups/remote')

    @patch.object(CoreBackupClient, '_get')
    def test_download_current_config(self, mock_get):
        """Test downloading current config"""
        mock_get.return_value = SAMPLE_CONFIG_XML

        client = Client.__new__(Client)
        result = client.core_backup_download()

        self.assertIn('<opnsense>', result)
        self.assertIn('<hostname>OPNsense</hostname>', result)
        mock_get.assert_called_once_with('core/backup/download/this', raw=True)

    @patch.object(CoreBackupClient, '_get')
    def test_download_specific_backup(self, mock_get):
        """Test downloading a specific backup"""
        mock_get.return_value = SAMPLE_CONFIG_XML

        client = Client.__new__(Client)
        client.core_backup_download(backup='2026-02-10T12:00:00')

        mock_get.assert_called_once_with(
            'core/backup/download/this/2026-02-10T12:00:00', raw=True
        )

    @patch.object(CoreBackupClient, '_get')
    def test_download_to_file(self, mock_get):
        """Test downloading config and saving to file"""
        mock_get.return_value = SAMPLE_CONFIG_XML

        client = Client.__new__(Client)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            tmppath = f.name

        try:
            result_path = client.core_backup_download_to_file(tmppath)
            self.assertEqual(result_path, tmppath)

            with open(tmppath, 'r') as f:
                content = f.read()
            self.assertIn('<opnsense>', content)
            self.assertIn('<hostname>OPNsense</hostname>', content)
        finally:
            os.unlink(tmppath)

    @patch.object(CoreBackupClient, '_get')
    def test_diff(self, mock_get):
        """Test getting diff between two backups"""
        diff_output = "--- backup1\n+++ backup2\n@@ -1 +1 @@\n-old\n+new"
        mock_get.return_value = diff_output

        client = Client.__new__(Client)
        result = client.core_backup_diff('this', 'backup1', 'backup2')

        self.assertEqual(result, diff_output)
        mock_get.assert_called_once_with(
            'core/backup/diff/this/backup1/backup2', raw=True
        )

    @patch.object(CoreBackupClient, '_post')
    def test_delete_backup(self, mock_post):
        """Test deleting a backup"""
        mock_post.return_value = self.DELETE_RESPONSE

        client = Client.__new__(Client)
        result = client.core_backup_delete('2026-02-10T12:00:00')

        self.assertEqual(result["status"], "ok")
        mock_post.assert_called_once_with(
            'core/backup/delete_backup', {'backup': '2026-02-10T12:00:00'}
        )

    @patch.object(CoreBackupClient, '_post')
    def test_revert_backup(self, mock_post):
        """Test reverting to a backup"""
        mock_post.return_value = self.REVERT_RESPONSE

        client = Client.__new__(Client)
        result = client.core_backup_revert('2026-02-10T12:00:00')

        self.assertEqual(result["status"], "ok")
        mock_post.assert_called_once_with(
            'core/backup/revert_backup', {'backup': '2026-02-10T12:00:00'}
        )
