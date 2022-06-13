import { Signer } from "@polkadot/api/types";
import { web3FromAddress } from "@polkadot/extension-dapp";
import axios from "axios";
import config from "../config";
import { getBalance } from "./balance";
export function byteToGB(capacity: number) {
  return (capacity / 1024 / 1024 / 1024).toFixed(0);
}
export async function createRentContract(api: { tx: { smartContractModule: { createRentContract: (arg0: any) => { (): any; new(): any; signAndSend: { (arg0: any, arg1: { signer: Signer; }, arg2: any): any; new(): any; }; }; }; }; }, address: string, nodeId: string, callback: any) {
  const injector = await web3FromAddress(address);
  return api.tx.smartContractModule
    .createRentContract(nodeId)
    .signAndSend(address, { signer: injector.signer }, callback);
}
export async function cancelRentContract(api: { tx: { smartContractModule: { cancelContract: (arg0: any) => { (): any; new(): any; signAndSend: { (arg0: any, arg1: { signer: Signer; }, arg2: any): any; new(): any; }; }; }; }; }, address: string, contractId: string, callback: any) {
  const injector = await web3FromAddress(address);
  return api.tx.smartContractModule
    .cancelContract(contractId)
    .signAndSend(address, { signer: injector.signer }, callback);
}
export async function getRentContractID(api: { query: { smartContractModule: { activeRentContractForNode: (arg0: any) => any; }; }; }, nodeID: string) {
  const rentContractID =
    await api.query.smartContractModule.activeRentContractForNode(nodeID);
  return rentContractID.toJSON().contract_id;
}
export async function getActiveContracts(api: { query: { smartContractModule: { activeNodeContracts: (arg0: any) => any; }; }; }, nodeID: string) {
  return await api.query.smartContractModule.activeNodeContracts(nodeID);
}
export async function getRentStatus(api: { query: { smartContractModule: { activeRentContractForNode: (arg0: string) => any; }; }; }, nodeID: string, currentTwinID: string) {
  const data = await api.query.smartContractModule.activeRentContractForNode(
    nodeID
  );

  const activeRentContracts = data.toJSON();

  if (activeRentContracts.contract_id === 0) {
    return "free";
  } else {
    if (activeRentContracts.twin_id == currentTwinID) {
      return "yours";
    } else {
      return "taken";
    }
  }
}

export async function getNodeUsedResources(nodeId: string) {
  const res = await axios.get(`${config.gridproxyUrl}nodes/${nodeId}`, {
    timeout: 1000,
  });

  if (res.status === 200) {
    if (res.data == "likely down") {
      throw Error("likely down");
    } else {
      return res.data.capacity.used_resources;
    }
  }
}
////
export async function getIpsForFarm(farmID: string) {
  if (config.graphqlUrl) {
    const res = await axios.post(
      config.graphqlUrl,
      {
        query: `query MyQuery {
            farms(where: {farmID_eq: ${farmID}}) {
              publicIPs {
                id
              }
            }
          }      
          `,
        operation: "getNodes",
      },
      { timeout: 1000 }
    );
    return res.data.data.farms[0].publicIPs.length;
  }

}
export function calSU(hru: number, sru: number) {
  return hru / 1200 + sru / 200;
}
export function calCU(cru: number, mru: number) {
  const mru_used_1 = mru / 4;
  const cru_used_1 = cru / 2;
  const cu1 = mru_used_1 > cru_used_1 ? mru_used_1 : cru_used_1;

  const mru_used_2 = mru / 8;
  const cru_used_2 = cru;
  const cu2 = mru_used_2 > cru_used_2 ? mru_used_2 : cru_used_2;

  const mru_used_3 = mru / 2;
  const cru_used_3 = cru / 4;
  const cu3 = mru_used_3 > cru_used_3 ? mru_used_3 : cru_used_3;

  let cu = cu1 > cu2 ? cu2 : cu1;
  cu = cu > cu3 ? cu3 : cu;

  return cu;
}
export async function getPrices(api: { query: { tfgridModule: { pricingPolicies: (arg0: number) => any; }; }; }) {
  const pricing = await api.query.tfgridModule.pricingPolicies(1);
  return pricing.toJSON();
}
export async function getDedicatedFarms() {
  if (config.graphqlUrl) {
    const res = await axios.post(
      config.graphqlUrl,
      {
        query: `{
          farms(where: {dedicatedFarm_eq: true}) {
            farmID
          }
        }
        `,
        operation: "getDedicatedFarms",
      },
      { timeout: 1000 }
    );
    return res.data.data.farms.map((farm: { farmID: string; }) => farm.farmID);
  }

}

export function countPrice(prices: { cu: { value: number; }; su: { value: number; }; }, node: { resourcesTotal: { sru: number; hru: number; mru: number; cru: any; }; }) {

  const resources = {
    sru: node.resourcesTotal.sru / 1024 / 1024 / 1024,
    hru: node.resourcesTotal.hru / 1024 / 1024 / 1024,
    mru: node.resourcesTotal.mru / 1024 / 1024 / 1024,
    cru: node.resourcesTotal.cru,
  };
  const SU = calSU(resources.hru, resources.sru);
  const CU = calCU(resources.cru, resources.mru);

  const totalPrice =
    CU * prices.cu.value * 24 * 30 + SU * prices.su.value * 24 * 30;

  const usdPrice = totalPrice / 10000000;

  return usdPrice.toFixed(2);
}
export async function calDiscount(api: { query: { system: { account: (arg0: string) => { data: any; }; }; }; }, address: string, pricing: { discount_for_dedicated_nodes: any; }, price: any) {
  // discount for Dedicated Nodes
  const discount = pricing.discount_for_dedicated_nodes;

  let totalPrice = price - price * (discount / 100);

  // discount for Twin Balance
  const balance = (await getBalance(api, address)) / 1e7;

  const discountPackages: any = {
    'none': {
      duration: 0,
      discount: 0,
    },
    'default': {
      duration: 3,
      discount: 20,
    },
    'bronze': {
      duration: 6,
      discount: 30,
    },
    'silver': {
      duration: 12,
      discount: 40,
    },
    'gold': {
      duration: 36,
      discount: 60,
    },
  };

  let selectedPackage = discountPackages.none


  for (const pkg in discountPackages) {
    if (balance > totalPrice * discountPackages[pkg].duration) {
      selectedPackage = pkg;
    }
  }

  totalPrice = totalPrice - totalPrice * (discountPackages[selectedPackage].discount / 100);

  return [totalPrice.toFixed(2), discountPackages[selectedPackage].discount];
}
export async function getDedicatedNodes(farmID: string) {
  if (config.graphqlUrl) {
    const res = await axios.post(
      config.graphqlUrl,
      {
        query: `query MyQuery {
            nodes(where: {farmID_eq: ${farmID}}) {
              resourcesTotal {
                cru
                hru
                mru
                sru
              }
              nodeID
              location {
                latitude
                longitude
              }
              country
              city
              farmID
            }
          }      
          `,
        operation: "getNodes",
      },
      { timeout: 1000 }
    );
    return res.data.data.nodes;
  }

}
export async function getDNodes(api: any, address: string) {
  const farmsIDs = await getDedicatedFarms();

  let nodes: any[] = [];
  for (const farmID of farmsIDs) {
    const _nodes = await getDedicatedNodes(farmID);
    nodes = nodes.concat(_nodes);
  }

  const pricing = await getPrices(api);
  const dNodes: { nodeId: string; price: string; discount: any; applyedDiscount: { first: any; second: any; }; location: { country: any; city: any; long: any; lat: any; }; resources: { cru: any; mru: any; hru: any; sru: any; }; pubIps: any; }[] = [];
  nodes.forEach(async (node) => {
    const price = countPrice(pricing, node);
    const [discount, discountLevel] = await calDiscount(api, address, pricing, price);
    const ips = await getIpsForFarm(node.farmID);
    dNodes.push({
      nodeId: node.nodeID,
      price: price,
      discount: discount,
      applyedDiscount: { first: pricing.discount_for_dedicated_nodes, second: discountLevel },
      location: {
        country: node.country,
        city: node.city,
        long: node.location.longitude,
        lat: node.location.latitude,
      },
      resources: {
        cru: node.resourcesTotal.cru,
        mru: node.resourcesTotal.mru,
        hru: node.resourcesTotal.hru,
        sru: node.resourcesTotal.sru,
      },
      pubIps: ips,
    });
  });
  return dNodes;
}
