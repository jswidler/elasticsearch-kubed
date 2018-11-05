#!/bin/bash
set -e

CA_NAME="$1"
URL="$2"
COUNTRY="$3"
STATE="$4"
LOC="$5"
ORG="$6"
ORG_UNIT="$7"
DEST="$8"

function make_ca {
  openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout ca.key -out ca.crt  -subj "/C=$COUNTRY/ST=$STATE/L=$LOC/O=$ORG/OU=$ORG_UNIT/CN=$CA_NAME"
}

function make_key_and_csr {
  openssl genrsa -out $1.pem 2048
  openssl pkcs8 -in $1.pem -topk8 -nocrypt -out $1.key
  openssl req -new -key $1.key -out $1.csr -subj "/C=$COUNTRY/ST=$STATE/L=$LOC/O=$ORG/OU=$ORG_UNIT/CN=$2"
}

function sign {
  openssl x509 -req -in $1.csr -CA $2.crt -CAkey $2.key -CAcreateserial -out $1.crt -days 3650 -sha256
  rm $1.csr
}

cd "$DEST"

make_ca
make_key_and_csr logstash "$URL"
sign logstash ca
make_key_and_csr client "*"
sign client ca
rm ca.srl
