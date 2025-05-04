# lnd_utils.py

import grpc
import codecs
import os
from lnd_grpc import lightning_pb2 as ln
from lnd_grpc import lightning_pb2_grpc as lnrpc


LND_DIR = os.path.expanduser("~/.lnd")
CERT_PATH = os.path.join(LND_DIR, "tls.cert")
MACAROON_PATH = os.path.join(LND_DIR, "data/chain/bitcoin/regtest/admin.macaroon")

with open(CERT_PATH, 'rb') as f:
    cert = f.read()
credentials = grpc.ssl_channel_credentials(cert)

with open(MACAROON_PATH, 'rb') as f:
    macaroon_bytes = f.read()
macaroon = codecs.encode(macaroon_bytes, 'hex')

class MacaroonAuth(grpc.AuthMetadataPlugin):
    def __call__(self, context, callback):
        callback([('macaroon', macaroon)], None)

auth_credentials = grpc.metadata_call_credentials(MacaroonAuth())
combined_creds = grpc.composite_channel_credentials(credentials, auth_credentials)

channel = grpc.secure_channel('localhost:10009', combined_creds)
stub = lnrpc.LightningStub(channel)

def create_invoice(amount_sats, memo="Order Payment"):
    invoice = ln.Invoice(value=amount_sats, memo=memo)
    response = stub.AddInvoice(invoice)
    return {
        "payment_request": response.payment_request,
        "r_hash": response.r_hash.hex()
    }

if __name__ == "__main__":
    result = create_invoice(amount_sats=50, memo="From the top")
    print("Invoice created")
    print(result)