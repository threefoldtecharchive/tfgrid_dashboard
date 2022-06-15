import { Signer } from '@polkadot/api/types';
import { web3FromAddress } from '@polkadot/extension-dapp';
import axios from 'axios';
import config from '../config';
import { getNodeUsedResources } from './nodes';
import { hex2a } from './util'
export async function getFarm(api: { query: any; }, twinID: number) {
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
export async function getFarmPayoutV2Address(api: { query: { tfgridModule: { farmPayoutV2AddressByFarmID: (arg0: number) => any; }; }; }, id: number) {
  const address = await api.query.tfgridModule.farmPayoutV2AddressByFarmID(id)
  return address.toJSON()
}
export async function setFarmPayoutV2Address(address: string, api: { tx: { tfgridModule: { addStellarPayoutV2address: (arg0: number, arg1: string) => { (): any; new(): any; signAndSend: { (arg0: string, arg1: { signer: Signer; }, arg2: any): any; new(): any; }; }; }; }; }, id: number, v2address: string, callback: any) {
  const injector = await web3FromAddress(address)

  return api.tx.tfgridModule
    .addStellarPayoutV2address(id, v2address)
    .signAndSend(address, { signer: injector.signer }, callback)
}
export async function createFarm(address: string, api: { tx: { tfgridModule: { createFarm: (arg0: string, arg1: never[]) => { (): any; new(): any; signAndSend: { (arg0: string, arg1: { signer: Signer; }, arg2: any): any; new(): any; }; }; }; }; }, name: string, callback: any) {
  const injector = await web3FromAddress(address)

  return api.tx.tfgridModule
    .createFarm(name, [])
    .signAndSend(address, { signer: injector.signer }, callback)
}
export async function createIP(address: string, api: { tx: { tfgridModule: { addFarmIp: (arg0: number, arg1: string, arg2: string) => { (): any; new(): any; signAndSend: { (arg0: string, arg1: { signer: Signer; }, arg2: any): any; new(): any; }; }; }; }; }, farmID: number, ip: string, gateway: string, callback: any) {
  const injector = await web3FromAddress(address)

  return api.tx.tfgridModule
    .addFarmIp(farmID, ip, gateway)
    .signAndSend(address, { signer: injector.signer }, callback)
}
export async function deleteIP(address: string, api: { tx: { tfgridModule: { removeFarmIp: (arg0: number, arg1: any) => { (): any; new(): any; signAndSend: { (arg0: string, arg1: { signer: Signer; }, arg2: any): any; new(): any; }; }; }; }; }, farmID: number, ip: { ip: string }, callback: any) {
  const injector = await web3FromAddress(address)

  return api.tx.tfgridModule
    .removeFarmIp(farmID, ip.ip)
    .signAndSend(address, { signer: injector.signer }, callback)
}
export async function deleteNode(address: string, api: { tx: { tfgridModule: { deleteNodeFarm: (arg0: any) => { (): any; new(): any; signAndSend: { (arg0: string, arg1: { signer: Signer; }, arg2: any): any; new(): any; }; }; }; }; }, nodeId: string, callback: any) {
  const injector = await web3FromAddress(address)

  return api.tx.tfgridModule
    .deleteNodeFarm(nodeId)
    .signAndSend(address, { signer: injector.signer }, callback)
}
export async function deleteFarm(address: string, api: { tx: { tfgridModule: { deleteFarm: (arg0: string) => { (): any; new(): any; signAndSend: { (arg0: string, arg1: { signer: Signer; }, arg2: any): any; new(): any; }; }; }; }; }, farmId: string, callback: any) {
  const injector = await web3FromAddress(address)

  return api.tx.tfgridModule
    .deleteFarm(farmId)
    .signAndSend(address, { signer: injector.signer }, callback)
}
export async function getNodesByFarmID(farms: any[]) {
  const farmIDs = farms.map((farm: { id: any; }) => farm.id);

  const nodes = farmIDs.map((farmID: string) => {
    return getNodesByFarm(farmID);
  });
  const data = await Promise.all(nodes);

  if (data.length === 0) return [];
  const _nodes = data.flat();

  const nodesWithResources = await _nodes.map(async (node) => {
    try {
      node.resourcesUsed = await getNodeUsedResources(node.nodeID);
      node.resources = node.resourcesTotal;
    } catch (error) {
      node.resourcesUsed = {
        sru: 0,
        hru: 0,
        mru: 0,
        cru: 0,
      };
      node.resources = {
        sru: 0,
        hru: 0,
        mru: 0,
        cru: 0,
      };
    }

    return node;
  });

  return await Promise.all(nodesWithResources);
}
export async function getNodesByFarm(farmID: string) {
  const res = await axios.post(config.graphqlUrl, {
    query: `{ nodes(where: {farmID_eq:${farmID}}) { id, farmID, twinID, resourcesTotal { sru, hru, mru, cru } , location { longitude, latitude }, country, city, publicConfig { ipv4, ipv6, gw4, gw6 }, created, farmingPolicyId, interfaces { name, mac, ips }, certification ,  secure, virtualized, serialNumber, connectionPrice }}`,
    operation: "getNodes",
  });

  return res.data.data.nodes;
}
export async function addNodePublicConfig(
  address: string,
  api: { tx: { tfgridModule: { addNodePublicConfig: (arg0: any, arg1: any, arg2: any) => { (): any; new(): any; signAndSend: { (arg0: any, arg1: { signer: Signer; }, arg2: any): any; new(): any; }; }; }; }; },
  farmID: string,
  nodeID: string,
  config: any,
  callback: any
) {
  const injector = await web3FromAddress(address);

  return api.tx.tfgridModule
    .addNodePublicConfig(farmID, nodeID, config)
    .signAndSend(address, { signer: injector.signer }, callback);
}
