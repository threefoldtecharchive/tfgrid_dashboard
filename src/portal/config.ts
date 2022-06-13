
const config = {
  wsUrl: process.env.APP_API_URL,
  horizonUrl: process.env.APP_STELLAR_HORIZON_URL,
  tftAssetIssuer: process.env.APP_TFT_ASSET_ISSUER,
  bridgeTftAddress: process.env.APP_BRIDGE_TFT_ADDRESS,
  activationServiceUrl: process.env.APP_ACTIVATION_SERVICE_URL,
  explorerUrl: process.env.APP_EXPLORER_URL,
  graphqlUrl: process.env.APP_GRAPHQL_URL,
  gridproxyUrl: process.env.APP_GRIDPROXY_URL,
  network: process.env.APP_NETWORK
}
export default config