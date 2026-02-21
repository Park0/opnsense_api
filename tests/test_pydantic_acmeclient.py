import json
from unittest import TestCase
from opnsense_api.pydantic.Certificate import Certificate


class TestPydanticAcmeClient(TestCase):

    @staticmethod
    def data_certificate_response_1():
        return r'{"certificate":{"id":"688525d7b8c7c0.97251853","enabled":"1","name":"homer.sso.lan","description":"","altNames":{"":{"value":"","selected":1}},"account":{"a4485aee-3217-4182-b93b-bfba45512d5f":{"value":"OpenBao","selected":1}},"validationMethod":{"7ca5303b-177e-4122-8322-9862977bc891":{"value":"http","selected":1}},"keyLength":{"key_2048":{"value":"2048 bit","selected":0},"key_3072":{"value":"3072 bit","selected":0},"key_4096":{"value":"4096 bit","selected":1},"key_ec256":{"value":"ec-256","selected":0},"key_ec384":{"value":"ec-384","selected":0}},"ocsp":"0","restartActions":[],"autoRenewal":"1","renewInterval":"60","aliasmode":{"none":{"value":"Not using DNS alias mode","selected":1},"automatic":{"value":"Automatic Mode (uses DNS lookups)","selected":0},"domain":{"value":"Domain alias mode","selected":0},"challenge":{"value":"Challenge alias mode","selected":0}},"domainalias":"","challengealias":"","certRefId":"6885bad526ec7","lastUpdate":"1753594581","statusCode":"200","statusLastUpdate":"1753594581"}}'

    @staticmethod
    def data_certificate_request_1():
        return r'{"certificate":{"enabled":"1","name":"homer.sso.lan","description":"","altNames":"","account":"a4485aee-3217-4182-b93b-bfba45512d5f","validationMethod":"7ca5303b-177e-4122-8322-9862977bc891","autoRenewal":"1","renewInterval":"60","keyLength":"key_4096","ocsp":"0","restartActions":"","aliasmode":"none","domainalias":"","challengealias":""}}'

    def test_certificate_request(self):
        cert = Certificate(
            enabled=True,
            name='example.lan',
            account='someuuid',
            validationMethod='validationuuid',
            keyLength=Certificate.CertificatesCertificateKeylengthEnum.KEY_4096,
            ocsp=False,
            autoRenewal=True,
            renewInterval=60,
            aliasmode=Certificate.CertificatesCertificateAliasmodeEnum.NONE
        )
        self.assertEqual(cert.to_simple_dict(),
        {'certificate': {
         'enabled': '1',
         'name': 'example.lan',
         'description': '',
         'altNames': '',
         'account': 'someuuid',
         'validationMethod': 'validationuuid',
         'autoRenewal': '1',
         'certRefId': '',
         'renewInterval': '60',
         'keyLength': 'key_4096',
         'lastUpdate': '',
         'ocsp': '0',
         'restartActions': '',
         'statusCode': '100',
         'statusLastUpdate': '',
         'aliasmode': 'none',
         'domainalias': '',
         'challengealias': ''
     }})

    def test_load_cert_data(self):
        cert_from_response = Certificate.from_ui_dict(json.loads(self.data_certificate_response_1()))  # type: Certificate
        self.assertTrue(cert_from_response.enabled)
        self.assertEqual("688525d7b8c7c0.97251853", cert_from_response.id)
        cert_from_request = Certificate.from_basic_dict(json.loads(self.data_certificate_request_1()))  # type: Certificate
        self.assertTrue(cert_from_request.enabled)
