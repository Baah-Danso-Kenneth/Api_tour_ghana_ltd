import os
import grpc
import codecs

import lightning_pb2 as ln
import  lightning_pb2_grpc as lnrpc

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

if __name__ == '__main__':
    info = stub.GetInfo(ln.GetInfoRequest())
    print(info)