#!/bin/bash
set -euo pipefail
shopt -s inherit_errexit

rm -rf ./momentum-api-client
rm -rf ../momentum_api_client/ 
openapi-python-client generate --url https://momentum-xyz.github.io/ubercontroller/openapi.json
mv momentum-api-client/momentum_api_client ../
