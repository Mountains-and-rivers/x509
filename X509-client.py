from OpenSSL import crypto
import random


def create_cert(ca_cert, ca_subj, ca_key, common_name=None):
    client_key = crypto.PKey()
    client_key.generate_key(crypto.TYPE_RSA, 4096)

    client_cert = crypto.X509()
    client_cert.set_version(2)
    client_cert.set_serial_number(random.randint(50000000, 100000000))

    client_subj = client_cert.get_subject()
    if common_name is None:
        client_subj.commonName = "Client"
    else:
        client_subj.commonName = common_name
    client_cert.set_issuer(ca_subj)
    client_cert.set_pubkey(client_key)

    client_cert.add_extensions([
        crypto.X509Extension(b"basicConstraints", False, b"CA:FALSE"),
    ])

    client_cert.add_extensions([
        crypto.X509Extension(b"authorityKeyIdentifier", False, b"keyid", issuer=ca_cert),
        crypto.X509Extension(b"extendedKeyUsage", False, b"serverAuth"),
        crypto.X509Extension(b"keyUsage", True, b"digitalSignature, keyEncipherment"),
    ])

    client_cert.add_extensions([
        crypto.X509Extension(b"subjectKeyIdentifier", False, b"hash", subject=client_cert),
    ])
    client_cert.gmtime_adj_notBefore(0)
    client_cert.gmtime_adj_notAfter(10*365*24*60*60)

    client_cert.sign(ca_key, 'sha256')

    # Save certificate
    with open("client.pem", "wt") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, client_cert).decode("utf-8"))

    # Save private key
    with open("client.key", "wt") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, client_key).decode("utf-8"))


key_path = "clientkey.key"
root_ca_path = "clientcert.pem"
client_subject = "my_client"


with open(key_path, "r") as f:
    private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, f.read())

with open(root_ca_path, "r") as f:
    ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM, f.read())

subject = ca_cert.get_subject()

create_cert(ca_cert, subject, private_key, client_subject)