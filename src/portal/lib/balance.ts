import { ApiPromise } from "@polkadot/api"


export async function getBalance (api: any, address: string) {
   const res = await api.query.system.account(address)
   const balance = res.data
   return balance.free.toJSON()
  }