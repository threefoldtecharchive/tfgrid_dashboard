import { web3FromAddress } from '@polkadot/extension-dapp';
import { hex2a } from './util'
export async function getFarm (api: any, twinID:number) {
    const farms = await api.query.tfgridModule.farms.entries()
    const twinFarms = farms.filter((farm: { toJSON: () => { (): any; new(): any; twin_id: number } }[]) => {
      if (farm[1].toJSON().twin_id === twinID) {
        return farm
      }
    })
    const parsedFarms = twinFarms.map(async (farm: { toJSON: () => any; }[]) => {
        const parsedFarm = farm[1].toJSON()
        const v2address = await getFarmPayoutV2Address(api, parsedFarm.id)
    
        return {
          ...parsedFarm,
          name: hex2a(parsedFarm.name),
          v2address: hex2a(v2address)
        }
      })
    
      return await Promise.all(parsedFarms)
  }
  export async function getFarmPayoutV2Address (api:any, id:number) {
    const address = await api.query.tfgridModule.farmPayoutV2AddressByFarmID(id)
    return address.toJSON()
  }
  export async function setFarmPayoutV2Address (address: string, api: any, id: number, v2address: string, callback: any) {
    const injector = await web3FromAddress(address)
  
    return api.tx.tfgridModule
      .addStellarPayoutV2Address(id, v2address)
      .signAndSend(address, { signer: injector.signer }, callback)
  }