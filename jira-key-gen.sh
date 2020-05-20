#!/bin/bash
#
#

KEY_NAME_BASE="NEW_KEY"

openssl genrsa -out "$KEY_NAME_BASE"_privatekey.pem 1024
openssl req -newkey rsa:1024 -x509 -key "$KEY_NAME_BASE"_privatekey.pem -out "$KEY_NAME_BASE"_publickey.cer -days 365
openssl pkcs8 -topk8 -nocrypt -in "$KEY_NAME_BASE"_privatekey.pem -out "$KEY_NAME_BASE"_privatekey.pcks8
openssl x509 -pubkey -noout -in "$KEY_NAME_BASE"_publickey.cer  > "$KEY_NAME_BASE"_publickey.pem
