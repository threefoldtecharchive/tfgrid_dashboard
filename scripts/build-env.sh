#!/bin/bash

REQUIRED_ENV_VARS=( GRAPHQL_URL TFT_ASSET_ISSUER BRIDGE_TFT_ADDRESS GRIDPROXY_URL VERSION SUBSTRATE_URL ACTIVATION_SERVICE_URL PLAYGROUND_URL RELAY_DOMAIN )
STELLAR_NETWORK="${NETWORK:=main}"
echo -e "\nHINT:\e[1;10m The default selected STELLAR_NETWORK is\e[0m \e[1;32m$STELLAR_NETWORK\e[0m\e[1;38m."

if [ -d dist ] 
then
    file="dist/config.js"
else
    file="config.js"
fi

for i in "${REQUIRED_ENV_VARS[@]}"
do
    if ! [[ -v $i ]]; then
        echo -e "\n\e[1;50m \e[1;31m$i is required!\e[0m\n \e[1;3mPlease set it by executing the following command."
        echo -e "\e[1;31m export\e[0m \e[1;32m$i\e[0m=\e[1;38m'Your Value Here'\n"
        return
    fi
done

GRAVITY_CONTRACT_ADDRESS="0xBF8C35Ad93366E159C0F0B75F1a4f4ad6Ff80811"
TFT_TOKEN_CONTRACT_ADDRESS="0xDC5a9199e2604A6BF4A99A583034506AE53F4B34"
BRIDGE_FEES="3"
TFT_DECIMALS=7
TFT_DENOM="TFT"
COSMOS_REST="https://tfhub.test.grid.tf:1317/"
TENDERMINT_RPC="https://tfhub.test.grid.tf:26657/"
GAS_PRICE="80TFT"
CHAIN_ID="threefold-hub-testnet"

case $STELLAR_NETWORK in
  "test")
    STELLAR_HORIZON_URL="https://horizon-testnet.stellar.org"
    ;;
  *"main"*)    
    STELLAR_HORIZON_URL="https://horizon.stellar.org"
    ;;
esac

configs="
window.configs = {
  APP_API_URL: '$SUBSTRATE_URL',
  APP_STELLAR_HORIZON_URL: '$STELLAR_HORIZON_URL',
  APP_TFT_ASSET_ISSUER: '$TFT_ASSET_ISSUER',
  APP_BRIDGE_TFT_ADDRESS: '$BRIDGE_TFT_ADDRESS',
  APP_ACTIVATION_SERVICE_URL: '$ACTIVATION_SERVICE_URL',
  APP_EXPLORER_URL: '$EXPLORER_URL',
  APP_GRAPHQL_URL: '$GRAPHQL_URL',
  APP_GRIDPROXY_URL: '$GRIDPROXY_URL',
  APP_NETWORK: '$STELLAR_NETWORK',
  APP_VERSION: '$VERSION',
  APP_GRAVITY_CONTRACT_ADDRESS: '$GRAVITY_CONTRACT_ADDRESS',
  APP_TFT_TOKEN_CONTRACT_ADDRESS: '$TFT_TOKEN_CONTRACT_ADDRESS',
  APP_BRIDGE_FEES: '$BRIDGE_FEES',
  APP_TFT_DECIMALS: $TFT_DECIMALS,
  APP_TFT_DENOM: '$TFT_DENOM',
  APP_PROPOSAL_DENOM: '$TFT_DENOM',
  APP_COSMOS_REST: '$COSMOS_REST',
  APP_TENDERMINT_RPC: '$TENDERMINT_RPC',
  APP_GAS_PRICE: '$GAS_PRICE',
  APP_CHAIN_ID: '$CHAIN_ID',
  PLAYGROUND_URL: '$PLAYGROUND_URL',
  RELAY: '$RELAY_DOMAIN',
};
"

if [ -e $file ]
then
    rm $file
fi

echo $configs > $file
