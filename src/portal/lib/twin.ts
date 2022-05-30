
import {
    web3FromAddress,
  } from '@polkadot/extension-dapp';
export async function createTwin (address:string, api: any, ip:string, callback:any) {
    const injector = await web3FromAddress(address)
    return api.tx.tfgridModule
      .createTwin(ip)
      .signAndSend(address, { signer: injector.signer }, callback)
  }
  export async function getTwin (api: any, id: number) {
    const twin = await api.query.tfgridModule.twins(id)
    return twin.toJSON()
  }
  export async function getTwinID (api: any, accountID: string) {
    const twin = await api.query.tfgridModule.twinIdByAccountID(accountID)
    console.log
    return twin.toJSON()
  }
  export async function updateTwinIP (address: string, api:any, ip: string, callback: any, errc?: any) {
    const injector = await web3FromAddress(address)
    return api.tx.tfgridModule
      .updateTwin(ip)
      .signAndSend(address, { signer: injector.signer }, callback, errc)
  }
  export async function deleteTwin (address:string, api: any, twinID: any, callback:any) {
    const injector = await web3FromAddress(address)
    return api.tx.tfgridModule
      .deleteTwin(twinID)
      .signAndSend(address, { signer: injector.signer }, callback)
  }