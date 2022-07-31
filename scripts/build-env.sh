#!/bin/sh

if [ -d dist ] 
then
    file="dist/config.js"
else
    file="config.js"
fi

if [ -z ${GQL_URL+x} ]
then
    echo 'Error! $GQL_URL is required.'
    exit 64
fi


NETWORK="main"
POLKADOT_URL="wss://tfchain.grid.tf/ws"
PROXY_URL="https://gridproxy.grid.tf"
ACTIVATION_SERVICE_URL="https://activation.grid.tf"
EXPLORER_URL="https://explorer.grid.tf/"
TFT_ASSET_ISSUER=GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3
BRIDGE_TFT_ADDRESS=GBNOTAYUMXVO5QDYWYO2SOCOYIJ3XFIP65GKOQN7H65ZZSO6BK4SLWSC
STELLAR_HORIZON_URL="https://horizon-testnet.stellar.org"

GRAVITY_CONTRACT_ADDRESS="0xBF8C35Ad93366E159C0F0B75F1a4f4ad6Ff80811"
TFT_TOKEN_CONTRACT_ADDRESS="0xDC5a9199e2604A6BF4A99A583034506AE53F4B34"
BRIDGE_FEES="3"
TFT_DECIMALS=7
TFT_DENOM="TFT"
PROPOSAL_DENOM="TFT"
COSMOS_REST="https://tfhub.test.grid.tf:1317/"
TENDERMINT_RPC="https://tfhub.test.grid.tf:26657/"
GAS_PRICE="80TFT"
CHAIN_ID="threefold-hub-testnet"

case $GQL_URL in
  *"dev"*)
    NETWORK="dev"
    GQL_URL="https://graphql.dev.grid.tf/graphql"
	  PROXY_URL="https://gridproxy.dev.grid.tf"
    POLKADOT_URL="wss://tfchain.dev.grid.tf/ws"
    TFT_ASSET_ISSUER=GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3
    BRIDGE_TFT_ADDRESS=GDHJP6TF3UXYXTNEZ2P36J5FH7W4BJJQ4AYYAXC66I2Q2AH5B6O6BCFG
    ACTIVATION_SERVICE_URL="https://activation.dev.grid.tf"
    EXPLORER_URL="https://explorer.dev.grid.tf/"
    STELLAR_HORIZON_URL="https://horizon-testnet.stellar.org"
    ;;
  *"test"*)
    NETWORK="test"
    GQL_URL="https://graphql.test.grid.tf/graphql"
    PROXY_URL="https://gridproxy.test.grid.tf"
    POLKADOT_URL="wss://tfchain.test.grid.tf/ws"
    TFT_ASSET_ISSUER=GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3
    BRIDGE_TFT_ADDRESS=GA2CWNBUHX7NZ3B5GR4I23FMU7VY5RPA77IUJTIXTTTGKYSKDSV6LUA4
    ACTIVATION_SERVICE_URL="https://activation.test.grid.tf"
    EXPLORER_URL="https://explorer.test.grid.tf/"
    STELLAR_HORIZON_URL="https://horizon-testnet.stellar.org"
    ;;
  *"qa"*)
    NETWORK="qa"
    GQL_URL="https://graphql.qa.grid.tf/graphql"
    PROXY_URL="https://gridproxy.qa.grid.tf"
    POLKADOT_URL="wss://tfchain.qa.grid.tf/ws"
    TFT_ASSET_ISSUER=GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3
    BRIDGE_TFT_ADDRESS=GDHJP6TF3UXYXTNEZ2P36J5FH7W4BJJQ4AYYAXC66I2Q2AH5B6O6BCFG
    ACTIVATION_SERVICE_URL="https://activation.qa.grid.tf"
    EXPLORER_URL="https://explorer.qa.grid.tf/"
    STELLAR_HORIZON_URL="https://horizon-testnet.stellar.org"
    ;;
esac

configs="
window.configs = {
  APP_API_URL: '$POLKADOT_URL',
  APP_STELLAR_HORIZON_URL: '$STELLAR_HORIZON_URL',
  APP_TFT_ASSET_ISSUER: '$TFT_ASSET_ISSUER',
  APP_BRIDGE_TFT_ADDRESS: '$BRIDGE_TFT_ADDRESS',
  APP_ACTIVATION_SERVICE_URL: '$ACTIVATION_SERVICE_URL',
  APP_EXPLORER_URL: '$EXPLORER_URL',
  APP_GRAPHQL_URL: '$GQL_URL',
  APP_GRIDPROXY_URL: '$PROXY_URL',
  APP_NETWORK: '$NETWORK',
  APP_VERSION: '$VERSION',
  APP_GRAVITY_CONTRACT_ADDRESS: '$GRAVITY_CONTRACT_ADDRESS',
  APP_TFT_TOKEN_CONTRACT_ADDRESS: '$TFT_TOKEN_CONTRACT_ADDRESS',
  APP_BRIDGE_FEES: '$BRIDGE_FEES',
  APP_TFT_DECIMALS: $TFT_DECIMALS,
  APP_TFT_DENOM: '$TFT_DENOM',
  APP_PROPOSAL_DENOM: '$PROPOSAL_DENOM',
  APP_COSMOS_REST: '$COSMOS_REST',
  APP_TENDERMINT_RPC: '$TENDERMINT_RPC',
  APP_GAS_PRICE: '$GAS_PRICE',
  APP_CHAIN_ID: '$CHAIN_ID'
};
"

if [ -e $file ]
then
    rm $file
fi

echo $configs > $file
