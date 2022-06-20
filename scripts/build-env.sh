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
TFT_ASSET_ISSUER="GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3"
BRIDGE_TFT_ADDRESS="GBLQSUJUD3HTC6YVCOIYI57QX6Q37AR4TNGVCH2YCSKH7YMUUHECHKPN"
STELLAR_HORIZON_URL="https://horizon-testnet.stellar.org"

case $GQL_URL in
  *"dev"*)
    NETWORK="dev"
    GQL_URL="https://graphql.dev.tf/graphql"
	PROXY_URL="https://gridproxy.dev.grid.tf"
    POLKADOT_URL="wss://tfchain.dev.grid.tf/ws"
    TFT_ASSET_ISSUER="GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3"
    BRIDGE_TFT_ADDRESS="GBLQSUJUD3HTC6YVCOIYI57QX6Q37AR4TNGVCH2YCSKH7YMUUHECHKPN"
    ACTIVATION_SERVICE_URL="https://activation.dev.grid.tf"
    EXPLORER_URL="https://explorer.dev.grid.tf/"
    STELLAR_HORIZON_URL="https://horizon-testnet.stellar.org"
    ;;
  *"test"*)
    NETWORK="test"
    GQL_URL="https://graphql.test.tf/graphql"
    PROXY_URL="https://gridproxy.test.grid.tf"
    POLKADOT_URL="wss://tfchain.test.grid.tf/ws"
    TFT_ASSET_ISSUER="GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3"
    BRIDGE_TFT_ADDRESS="GBLQSUJUD3HTC6YVCOIYI57QX6Q37AR4TNGVCH2YCSKH7YMUUHECHKPN"
    ACTIVATION_SERVICE_URL="https://activation.test.grid.tf"
    EXPLORER_URL="https://explorer.test.grid.tf/"
    STELLAR_HORIZON_URL="https://horizon-testnet.stellar.org"
    ;;
  *"qa"*)
    NETWORK="qa"
    GQL_URL="https://graphql.qa.tf/graphql"
    PROXY_URL="https://gridproxy.qa.grid.tf"
    POLKADOT_URL="wss://tfchain.qa.grid.tf/ws"
    TFT_ASSET_ISSUER="GA47YZA3PKFUZMPLQ3B5F2E3CJIB57TGGU7SPCQT2WAEYKN766PWIMB3"
    BRIDGE_TFT_ADDRESS="GBLQSUJUD3HTC6YVCOIYI57QX6Q37AR4TNGVCH2YCSKH7YMUUHECHKPN"
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
  APP_VERSION: '$VERSION'
};
"

if [ -e $file ]
then
    rm $file
fi

echo $configs > $file
