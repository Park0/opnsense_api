from opnsense_api.api.helper import Helper
from opnsense_api.api.trust_ca_client import TrustCaClient
from opnsense_api.api.trust_cert_client import TrustCertClient
from opnsense_api.api.trust_crl_client import TrustCrlClient


class Trust(TrustCaClient, TrustCrlClient, TrustCertClient):
    def certificates_check(self):
        certs = self.trust_cert_search()
        crl = self.trust_crl_search()

        valid = []
        invalid = []

        for cert in certs.rows:
            found = False
            for revoke_cert in crl.rows:
                if revoke_cert.refid == cert.refid:
                    invalid.append(cert)
                    found = True
            if found:
                continue
            else:
                if not Helper.cert_expired(cert):
                    valid.append(cert)
                else:
                    invalid.append(cert)
        return valid, invalid

