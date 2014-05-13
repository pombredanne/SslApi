import logging

_logger = logging.getLogger(__name__)

# At the top of the request, perhaps to verify the caller by the client-hash or 
# the information in the CSR.
API_CSR_AUTHORIZE_HOOK = lambda \
                            subject_alt_name_exts, \
                            csr_tuple, \
                            public_key_hash, \
                            client_hash: None

# Called with the certificate before it's signed, to add extensions or such.
API_CSR_PRESIGN_HOOK = lambda \
                            certificate, \
                            public_key_hash, \
                            client_hash: None

# Called with the certificate after it's signed, perhaps to store the 
# certificate's fingerprint.
API_CSR_POSTSIGN_HOOK = lambda \
                            certificate, \
                            public_key_hash, \
                            client_hash: None

from sapi_custom_ca.api import *
