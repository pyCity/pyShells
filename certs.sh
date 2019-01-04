#!/usr/bin/env bash

# Check that openssl is installed before generating certs. Removes the unnecessary files after.
if ! [ -x "$(command -v openssl)" ]; then
    echo "Openssl not detected. Please install openssl (or use ncat --ssl instead)"
    exit 1
else
    echo "Generating certs. Enter a passphrase and example.com as the website"
    openssl genrsa -des3 -out server.orig.key 2048
    openssl rsa -in server.orig.key -out server.key
    openssl req -new -key server.key -out server.csr
    openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
    rm server.orig.key server.csr
fi
