from OpenSSL import crypto
import os
from python_settings import settings 

ROOT_CRT_PATH = '.'
CA_KEY_FILE = os.path.join(settings.ROOT_CRT_PATH, 'rootCA.key')
CA_CERT_FILE = os.path.join(settings.ROOT_CRT_PATH, 'rootCA.crt')
k = crypto.PKey()
k.generate_key(crypto.TYPE_RSA, 2048)

cert = crypto.X509()

cert.get_subject().C = 'country'
cert.get_subject().ST = 'state'
cert.get_subject().L = 'location'
cert.get_subject().O = 'organization'
cert.get_subject().OU = 'organizational_unit_name'
cert.get_subject().CN = 'cn'
cert.get_subject().emailAddress = 'email'

cert.set_serial_number(1000)
cert.gmtime_adj_notBefore(0)
cert.gmtime_adj_notAfter(5 * 365 * 24 * 60 * 60)
cert.set_issuer(cert.get_subject())
cert.set_pubkey(k)
cert.sign(k, 'sha256')

key_path = os.path.join(settings.MEDIA_ROOT, CA_KEY_FILE)
cert_path = os.path.join(settings.MEDIA_ROOT, CA_CERT_FILE)

if not os.path.exists(os.path.join(settings.MEDIA_ROOT, settings.ROOT_CRT_PATH)):
    os.mkdir(os.path.join(settings.MEDIA_ROOT, settings.ROOT_CRT_PATH))

with open(cert_path, 'wb') as f:
    f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

with open(key_path, 'wb') as f:
    f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))


# Now the real world use case; use certificate to verify signature
f = open("private.key")
pv_buf = f.read()
f.close()
#priv_key = crypto.load_privatekey(crypto.FILETYPE_PEM, pv_buf, bytes('ninovsnino',encoding="utf-8"))
priv_key = crypto.load_privatekey(crypto.FILETYPE_PEM, pv_buf, bytes('ninovsnino',encoding="utf-8"))
f = open("selfsign.pem")
ss_buf = f.read()
f.close()


#生成p12 证书
p12 = crypto.PKCS12()
p12.set_privatekey( k )
p12.set_certificate( cert )
open( "container.p12",  'wb'  ).write( p12.export() )