from OpenSSL import crypto
from socket import gethostname
from python_settings import settings 
import os
import random
os.environ["SETTINGS_MODULE"] = 'settings' 
# print(settings.DATABASE_HOST) # Will print '10.0.0.1'
# print(settings.DATABASE_NAME) # Will print 'DATABASENAME'

# 创建CA根证书
CA_KEY_FILE = os.path.join(settings.ROOT_CRT_PATH, 'rootCA.key')
CA_CERT_FILE = os.path.join(settings.ROOT_CRT_PATH, 'rootCA.crt')

k = crypto.PKey()
k.generate_key(crypto.TYPE_RSA, 2048)

cert = crypto.X509()

cert.get_subject().C = "CN"
cert.get_subject().ST = "Shenzhen"
cert.get_subject().O = "HW"
cert.get_subject().OU = "HW"
cert.get_subject().CN = gethostname()
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


#生成p12 证书
p12 = crypto.PKCS12()
p12.set_privatekey( k )
p12.set_certificate( cert )
open( "container.p12",  'wb'  ).write( p12.export() )


cert.set_serial_number(1000)
cert.gmtime_adj_notBefore(0)
cert.gmtime_adj_notAfter(10*365*24*60*60)
cert.set_issuer(cert.get_subject())
cert.set_pubkey(k)
cert.sign(k, 'sha1')

#生成服务端证书
open('server.pem', "wb").write(
    crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
open('server.key', "wb").write(
    crypto.dump_privatekey(crypto.FILETYPE_PEM, k, passphrase=bytes('ninovsnino',encoding="utf-8")))