
import { Signer } from '@polkadot/api/types';
import {
  web3FromAddress,
} from '@polkadot/extension-dapp';


export async function createTwin(address: string, api: { tx: { tfgridModule: { createTwin: (arg0: string) => { (): any; new(): any; signAndSend: { (arg0: string, arg1: { signer: Signer; }, arg2: any): any; new(): any; }; }; }; }; }, ip: string, callback: any) {
  const injector = await web3FromAddress(address)
  return api.tx.tfgridModule
    .createTwin(ip)
    .signAndSend(address, { signer: injector.signer }, callback)
}
export async function getTwin(api: { query: { tfgridModule: { twins: (arg0: number) => any; }; }; }, id: number) {
  const twin = await api.query.tfgridModule.twins(id)
  return twin.toJSON()
}
export async function getTwinID(api: { query: { tfgridModule: { twinIdByAccountID: (arg0: string) => any; }; }; }, accountID: string) {
  const twin = await api.query.tfgridModule.twinIdByAccountID(accountID)
  console.log
  return twin.toJSON()
}
export async function updateTwinIP(address: string, api: { tx: { tfgridModule: { updateTwin: (arg0: string) => { (): any; new(): any; signAndSend: { (arg0: string, arg1: { signer: Signer; }, arg2: any, arg3: any): any; new(): any; }; }; }; }; }, ip: string, callback: any, errc?: any) {
  const injector = await web3FromAddress(address)
  return api.tx.tfgridModule
    .updateTwin(ip)
    .signAndSend(address, { signer: injector.signer }, callback, errc)
}
export async function deleteTwin(address: string, api: { tx: { tfgridModule: { deleteTwin: (arg0: any) => { (): any; new(): any; signAndSend: { (arg0: string, arg1: { signer: Signer; }, arg2: any): any; new(): any; }; }; }; }; }, twinID: string, callback: any) {
  const injector = await web3FromAddress(address)
  return api.tx.tfgridModule
    .deleteTwin(twinID)
    .signAndSend(address, { signer: injector.signer }, callback)
}