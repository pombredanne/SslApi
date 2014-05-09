import time
import logging

import M2Crypto.X509
import M2Crypto.EVP
import M2Crypto.ASN1
import M2Crypto.RSA

import sapi.ssl.utility

_logger = logging.getLogger(__name__)

def new_cert(ca_private_key_pem, csr_pem, validity_td, issuer_name, bits=2048,
             is_ca=False, passphrase=None):
    _logger.debug("Creating certificate. IS_CA=[%s]", is_ca)

    ca_rsa = sapi.ssl.utility.pem_private_to_rsa(
                ca_private_key_pem, 
                passphrase=passphrase)

    def callback(*args):
        pass

#    ca_rsa = M2Crypto.RSA.gen_key(bits, 65537, callback)

    csr = sapi.ssl.utility.pem_csr_to_csr(csr_pem)

    public_key = csr.get_pubkey()
    name = csr.get_subject()

    cert = M2Crypto.X509.X509()
    cert.set_serial_number(1)
    cert.set_version(2)
    cert.set_subject(name)

    now_epoch = long(time.time()) + time.timezone

    notBefore = M2Crypto.ASN1.ASN1_UTCTIME()
    notBefore.set_time(now_epoch)

    notAfter = M2Crypto.ASN1.ASN1_UTCTIME()
    notAfter.set_time(now_epoch + long(validity_td.total_seconds()))

    cert.set_not_before(notBefore)
    cert.set_not_after(notAfter)

    cert.set_issuer(issuer_name)
    cert.set_pubkey(public_key) 

    if is_ca is True:
        ext = M2Crypto.X509.new_extension('basicConstraints', 'CA:TRUE')
        cert.add_ext(ext)

    pkey = M2Crypto.EVP.PKey()
    pkey.assign_rsa(ca_rsa)
 
    cert.sign(pkey, 'sha1')
    cert_pem = cert.as_pem()

    return cert_pem
