

import { Signer } from '@polkadot/api/types';
import { web3FromAddress } from '@polkadot/extension-dapp';
import axios from 'axios';
import config from '../config';
import { getDedicatedNodes } from './nodes';
import { getNodeMintingFixupReceipts, getNodeUsedResources, receiptInterface } from './nodes';
import { hex2a } from './util'
export interface nodeInterface {
  resourcesTotal: {
    cru: string;
    hru: string;
    mru: string;
    sru: string;
  },
  publicConfig: {
    domain: string;
    gw4: string;
    gw6: string;
    ipv4: string;
    ipv6: string;
  },
  receipts: receiptInterface[];
  certification: string;
  city: string;
  connectionPrice: null;
  country: string;
  created: number;
  createdAt: string;
  farmID: number;
  farmingPolicyId: number;
  gridVersion: number;
  id: string;
  location: {
    latitude: string;
    longitude: string;
  },
  nodeID: number;
  secure: boolean;
  serialNumber: string;
  twinID: number;
  updatedAt: string;
  uptime: number;
  virtualized: boolean;
}
export async function getFarm(api: { query: any; }, twinID: number) {
  const farms = await api.query.tfgridModule.farms.entries()

  const twinFarms = farms.filter((farm: { toJSON: () => { (): any; new(): any; twinId: number } }[]) => {
    if (farm[1].toJSON().twinId === twinID) {
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
export async function deleteNode(address: string, api: { tx: { tfgridModule: { deleteNodeFarm: (arg0: any) => { (): any; new(): any; signAndSend: { (arg0: string, arg1: { signer: Signer; }, arg2: any): any; new(): any; }; }; }; }; }, nodeId: number, callback: any) {
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

  const nodesWithResources = _nodes.map(async (node) => {

    try {
      node.resourcesUsed = await getNodeUsedResources(node.nodeID);
      
      node.resources = node.resourcesTotal;
      node.receipts = await getNodeMintingFixupReceipts(node.nodeID);

    } catch (error) {
      node.receipts = [];
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
    query: `{ nodes (where: {farmID_eq:${farmID}}) { 
      resourcesTotal {
        cru
        hru
        mru
        sru
      }
      publicConfig {
        domain
        gw4
        gw6
        ipv4
        ipv6
      }
      certification
      city
      connectionPrice
      country
      created
      createdAt
      farmID
      farmingPolicyId
      gridVersion
      id
      location {
        latitude
        longitude
      }
      nodeID
      secure
      serialNumber
      twinID
      updatedAt
      uptime
      virtualized
    }}`,
    operation: "getNodes",
  });

  return res.data.data.nodes;
}
export async function addNodePublicConfig(
  address: string,
  api: { tx: { tfgridModule: { addNodePublicConfig: (arg0: any, arg1: any, arg2: any) => { (): any; new(): any; signAndSend: { (arg0: any, arg1: { signer: Signer; }, arg2: any): any; new(): any; }; }; }; }; },
  farmID: number,
  nodeID: number,
  config: {
    ip4: {ip: string, gw: string},
    ip6?: {ip: string | undefined, gw: string | undefined},
    domain?: string
  },
  callback: any
) {
  const injector = await web3FromAddress(address);

  return api.tx.tfgridModule
    .addNodePublicConfig(farmID, nodeID, config)
    .signAndSend(address, { signer: injector.signer }, callback);
}