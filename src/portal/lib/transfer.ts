export async function getDepositFee (api:any) {
    const fee = await api.query.tftBridgeModule.depositFee()
    return fee.toNumber() / 1e7
  }