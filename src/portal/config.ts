
const config = {
    wsUrl: process.env.VUE_APP_API_URL,
    horizonUrl:  process.env.VUE_APP_STELLAR_HORIZON_URL,
    tftAssetIssuer:  process.env.VUE_APP_TFT_ASSET_ISSUER,
    bridgeTftAddress: process.env.VUE_APP_BRIDGE_TFT_ADDRESS,
    activationServiceUrl: process.env.VUE_APP_ACTIVATION_SERVICE_URL,
    explorerUrl: process.env.VUE_APP_EXPLORER_URL,
    graphqlUrl:  process.env.VUE_APP_GRAPHQL_URL,
    gridproxyUrl: process.env.VUE_APP_GRIDPROXY_URL ,
    network:  process.env.VUE_APP_NETWORK
  }
  
  export default config