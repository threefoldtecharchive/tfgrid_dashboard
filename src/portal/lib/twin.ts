import { ApiPromise } from "@polkadot/api"
import {
    web3FromAddress,
  } from '@polkadot/extension-dapp';
export async function createTwin (address:string, api: ApiPromise, ip:string, callback:any) {
    const injector = await web3FromAddress(address)
    return api.tx.tfgridModule
      .createTwin(ip)
      .signAndSend(address, { signer: injector.signer }, callback)
  }