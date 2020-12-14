from OpenSSL import crypto, SSL
from os.path import join
import random

pubkey = "rootac.key"
privkey = "rootac.pem"

k = crypto.PKey()
k.generate_key(crypto.TYPE_RSA, 2048)
serialnumber=random.getrandbits(64)

# create a self-signed cert
cert = crypto.X509()
cert.get_subject().C = 'CN'
cert.get_subject().ST = 'state'
cert.get_subject().L = 'location'
cert.get_subject().O = 'organization'
cert.get_subject().OU = 'organizational_unit_name'
cert.get_subject().CN = 'cn'
cert.get_subject().emailAddress = 'email'

cert.set_serial_number(serialnumber)
cert.gmtime_adj_notBefore(0)
cert.gmtime_adj_notAfter(31536000)#315360000 is in seconds.
cert.set_issuer(cert.get_subject())
cert.set_pubkey(k)
cert.sign(k, 'sha512')
pub=crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
priv=crypto.dump_privatekey(crypto.FILETYPE_PEM, k)
open(pubkey,"wt").write(pub.decode("utf-8"))
open(privkey, "wt").write(priv.decode("utf-8") )