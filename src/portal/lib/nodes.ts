/* eslint-disable */
import { Signer } from "@polkadot/api/types";
import { web3FromAddress } from "@polkadot/extension-dapp";
import axios from "axios";
import config from "../config";
import { getBalance } from "./balance";
import { jsPDF } from "jspdf";
import { nodeInterface } from "./farms";
import moment from "moment";
import 'jspdf-autotable';
export interface receiptInterface {
  hash: string;
  mintingStart?: number;
  mintingEnd?: number;
  measuredUptime?: number;
  fixupStart?: number;
  fixupEnd?: number;
  tft?: number;
}
export function getNodeUptimePercentage(node: nodeInterface) {
  const totalReceiptsUptime = node.receipts.reduce(
    (total, receipt) =>
      receipt.measuredUptime
        ? (total += receipt.measuredUptime)
        : (total += 0),
    0
  );
  return ((totalReceiptsUptime / node.uptime) * 100).toFixed(2);
}
export function getTime(num: number | undefined) {
  if (num) {
    return new Date(num);
  }
  return new Date();
}
export function generateNodeSummary(doc: jsPDF, nodes: nodeInterface[]) {
  doc.setFontSize(15);
  const topY = 20;
  const topX = 80;
  const lineOffset = 10;
  const cellOffset = 40;
  const cellX = 15;
  const cellY = topY + lineOffset

  doc.text("Total Nodes Summary", topX, topY);
  doc.setFontSize(10);



  doc.text(`Nodes: ${nodes.length}`, cellX, cellY)
  doc.text(`Receipts: ${nodes.reduce((total, node) => total += node.receipts.length, 0)}`, cellX, cellY + lineOffset)
  doc.text(`Minting Receipts: ${nodes.reduce((total, node) => total += node.receipts.filter((receipt) => receipt.measuredUptime).length, 0)}`, cellX, cellY + lineOffset * 2)
  doc.text(`Fixup Receipts: ${nodes.reduce((total, node) => total += node.receipts.filter((receipt) => receipt.fixupStart).length, 0)}`, cellX, cellY + lineOffset * 3)
  doc.text(`TFT: ${nodes.reduce((total, node) => total += node.receipts.reduce((totalTFT, receipt) => totalTFT += receipt.tft || 0, 0), 0).toFixed(2)}`, cellX, cellY + lineOffset * 4)
  doc.text(`Uptime: ${(nodes.reduce((totalM, node) => totalM += node.receipts.reduce((total, receipt) => total += receipt.measuredUptime || 0, 0), 0)
    / nodes.reduce((totalU, node) => totalU += Math.floor(moment.duration(node.uptime, 'seconds').asSeconds()), 0) * 100).toFixed(2)}% - ${nodes.reduce((total, node) => total += Math.floor(moment.duration(node.uptime, 'seconds').asDays()), 0)} days`, cellX, cellY + lineOffset * 5)


}
export function generateReceipt(doc: jsPDF, node: nodeInterface) {

  doc.setFontSize(15);

  const topY = 20;
  const lineOffset = 5;
  const cellOffset = 30;
  const cellX = 15;
  const cellY = topY + lineOffset * 8;

  doc.text(`Node ${node.nodeID} Summary`, 80, topY);
  doc.setFontSize(10);
  doc.text(
    `Receipts total: ${node.receipts.length}`,
    cellX,
    topY + lineOffset
  );
  doc.text(
    `Minting total: ${node.receipts.filter((receipt) => receipt.measuredUptime).length
    }`,
    cellX,
    topY + lineOffset * 2
  );
  doc.text(
    `Fixup total: ${node.receipts.filter((receipt) => receipt.fixupStart).length
    }`,
    cellX,
    topY + lineOffset * 3
  );

  doc.text(
    `TFT total: ${node.receipts
      .reduce((total, receipt) => (total += receipt.tft || 0), 0)
      .toFixed(2)}`,
    cellX,
    topY + lineOffset * 4
  );
  doc.text(`Uptime: ${getNodeUptimePercentage(node)}% - ${Math.floor(moment.duration(node.uptime, 'seconds').asDays())} days`, cellX, topY + lineOffset * 5);

  doc.line(cellX, topY + lineOffset * 6, cellX + 175, topY + lineOffset * 6);

  node.receipts.map((receipt, i) => {
    if (receipt.measuredUptime) {
      doc.text(`Minting: ${receipt.hash}`, cellX, cellY + cellOffset * i);
      doc.text(
        `start: ${getTime(receipt.mintingStart)}`,
        cellX,
        cellY + cellOffset * i + lineOffset
      );
      doc.text(
        `end: ${getTime(receipt.mintingEnd)}`,
        cellX,
        cellY + cellOffset * i + lineOffset * 2
      );
      doc.text(
        `TFT: ${receipt.tft?.toFixed(2)}`,
        cellX,
        cellY + cellOffset * i + lineOffset * 3
      );

    } else {
      doc.text(`Fixup: ${receipt.hash}`, cellX, cellY + cellOffset * i);
      doc.text(
        `start: ${getTime(receipt.fixupStart)}`,
        cellX,
        cellY + cellOffset * i + lineOffset
      );
      doc.text(
        `end: ${getTime(receipt.fixupEnd)}`,
        cellX,
        cellY + cellOffset * i + lineOffset * 2
      );


    }
    if (i !== node.receipts.length - 1) {
      doc.line(
        cellX,
        cellY + cellOffset * i + lineOffset * 4,
        cellX + 175,
        cellY + cellOffset * i + lineOffset * 4
      );
    }

  });


  return doc
}
export function byteToGB(capacity: number) {
  return (capacity / 1024 / 1024 / 1024).toFixed(0);
}
export async function createRentContract(api: { tx: { smartContractModule: { createRentContract: (arg0: any, arg1: any) => { (): any; new(): any; signAndSend: { (arg0: any, arg1: { signer: Signer; }, arg2: any): any; new(): any; }; }; }; }; }, address: string, nodeId: string, solutionProviderID: string | null, callback: any) {
  const injector = await web3FromAddress(address);
  return api.tx.smartContractModule
    .createRentContract(nodeId, solutionProviderID)
    .signAndSend(address, { signer: injector.signer }, callback);
}
export async function cancelRentContract(api: { tx: { smartContractModule: { cancelContract: (arg0: any) => { (): any; new(): any; signAndSend: { (arg0: any, arg1: { signer: Signer; }, arg2: any): any; new(): any; }; }; }; }; }, address: string, contractId: string, callback: any) {
  const injector = await web3FromAddress(address);
  return api.tx.smartContractModule
    .cancelContract(contractId)
    .signAndSend(address, { signer: injector.signer }, callback);
}

export async function getActiveContracts(api: { query: { smartContractModule: { activeNodeContracts: (arg0: any) => any; }; }; }, nodeID: string) {
  console.log("getActiveContracts", api.query.smartContractModule.activeNodeContracts(nodeID));
  return await api.query.smartContractModule.activeNodeContracts(nodeID);
}

export async function getNodeMintingFixupReceipts(nodeId: string) {
  let nodeReceipts: receiptInterface[] = []
  const res = await axios.get(`https://alpha.minting.tfchain.grid.tf/api/v1/node/${nodeId}`)
    .then(res => res.data.map((rec:
      {
        hash: any;
        receipt:
        {
          Minting:
          {
            period: { start: number; end: number; };
            measured_uptime: number;
            reward: { musd: number, tft: number }
          };
          Fixup: { period: { start: number; end: number; }; };
        };
      }) => {
      if (rec.receipt.Minting) {
        nodeReceipts.push({
          hash: rec.hash,
          mintingStart: rec.receipt.Minting.period.start * 1000,
          mintingEnd: rec.receipt.Minting.period.end * 1000,
          measuredUptime: rec.receipt.Minting.measured_uptime || 0,
          tft: (rec.receipt.Minting.reward.tft / 1e7)
        })
      } else {
        nodeReceipts.push({
          hash: rec.hash,
          fixupStart: rec.receipt.Fixup.period.start * 1000 || 0,
          fixupEnd: rec.receipt.Fixup.period.end * 1000 || 0,
        })
      }
    }
    ))

  return nodeReceipts

}
export async function getNodeUsedResources(nodeId: string) {
  const res = await axios.get(`${config.gridproxyUrl}/nodes/${nodeId}`, {
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

export async function getIpsForFarm(farmID: string) {
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

export function countPrice(prices: { cu: { value: number; }; su: { value: number; }; }, node: { total_resources: { sru: number; hru: number; mru: number; cru: any; }; }) {

  const resources = {
    sru: node.total_resources.sru / 1024 / 1024 / 1024,
    hru: node.total_resources.hru / 1024 / 1024 / 1024,
    mru: node.total_resources.mru / 1024 / 1024 / 1024,
    cru: node.total_resources.cru,
  };
  const SU = calSU(resources.hru, resources.sru);
  const CU = calCU(resources.cru, resources.mru);

  const totalPrice =
    CU * prices.cu.value * 24 * 30 + SU * prices.su.value * 24 * 30;

  const usdPrice = totalPrice / 10000000;

  return usdPrice.toFixed(2);
}
export async function calDiscount(api: { query: { system: { account: (arg0: string) => { data: any; }; }; }; }, address: string, pricing: { discountForDedicationNodes: any; }, price: any) {
  // discount for Dedicated Nodes
  const discount = pricing.discountForDedicationNodes;

  let totalPrice = price - price * (discount / 100);

  // discount for Twin Balance
  const balance = (await getBalance(api, address));

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

  let selectedPackage = "none"


  for (const pkg in discountPackages) {
    if (balance.free > totalPrice * discountPackages[pkg].duration) {
      selectedPackage = pkg;
    }
  }

  totalPrice = totalPrice - totalPrice * (discountPackages[selectedPackage].discount / 100);

  return [totalPrice.toFixed(2), discountPackages[selectedPackage].discount];
}

export async function getNodeByID(nodeID: any) {
  const node = await fetch(
    `${config.gridproxyUrl}/nodes/${nodeID}`
  ).then((res) => res.json())
  return node;
}
export async function getRentableNodes() {
  const res = await fetch(
    `${config.gridproxyUrl}/nodes?rentable=true&status=up`
  ).then((res) => res.json())
  return res;
}

export async function getRentedNodes() {
  const res = await fetch(
    `${config.gridproxyUrl}/nodes?rented=true&status=up`
  ).then((res) => res.json())
  return res;
}

export async function getDedicatedNodes() {
  const rentedNodes = await getRentableNodes();
  const rentableNodes = await getRentedNodes();
  let dedicatedNodes: any[] = [];
  dedicatedNodes = dedicatedNodes.concat(rentedNodes, rentableNodes);
  return dedicatedNodes;
}
export async function getDNodes(api: any, address: string, currentTwinID: string) {
  let nodes: any[] = [];
  nodes = await getDedicatedNodes();

  const pricing = await getPrices(api); let dNodes: { nodeId: string; price: string; discount: any; applyedDiscount: { first: any; second: any; }; location: { country: any; city: any; long: any; lat: any; }; resources: { cru: any; mru: any; hru: any; sru: any; }; pubIps: any; rentContractId: any, rentedByTwinId: any; usedResources: { cru: any; mru: any; hru: any; sru: any; }; rentStatus: any }[] = [];
  nodes.forEach(async (node) => {
    const price = countPrice(pricing, node);
    const [discount, discountLevel] = await calDiscount(api, address, pricing, price);
    const ips = await getIpsForFarm(node.farmId);
    dNodes.push({
      nodeId: node.nodeId,
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
        cru: node.total_resources.cru,
        mru: node.total_resources.mru,
        hru: node.total_resources.hru,
        sru: node.total_resources.sru,
      },
      usedResources: {
        cru: node.used_resources.cru,
        mru: node.used_resources.mru,
        hru: node.used_resources.hru,
        sru: node.used_resources.sru,
      },
      pubIps: ips,
      rentContractId: node.rentContractId,
      rentedByTwinId: node.rentedByTwinId,
      rentStatus: node.rentContractId === 0 ? "free" : node.rentedByTwinId == currentTwinID ? "yours" : "taken"
    });
  });
  return dNodes;
}



