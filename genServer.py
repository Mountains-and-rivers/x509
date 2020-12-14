from OpenSSL import crypto
from socket import gethostname
TYPE_RSA = crypto.TYPE_RSA
TYPE_DSA = crypto.TYPE_DSA


# create a key pair
k = crypto.PKey()
k.generate_key(crypto.TYPE_RSA, 1024)

# create a self-signed cert
cert = crypto.X509()
cert.get_subject().C = "US"
cert.get_subject().ST = "Minnesota"
cert.get_subject().L = "Minnetonka"
cert.get_subject().O = "my company"
cert.get_subject().OU = "my organization"
cert.get_subject().CN = gethostname()
cert.set_serial_number(1000)
cert.gmtime_adj_notBefore(0)
cert.gmtime_adj_notAfter(10*365*24*60*60)
cert.set_issuer(cert.get_subject())
cert.set_pubkey(k)
cert.sign(k, 'sha1')

open("server.pem", "wb").write(
    crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
open("server.key", "wb").write(
    crypto.dump_privatekey(crypto.FILETYPE_PEM, k,passphrase=bytes('ninovsnino',encoding="utf-8")))