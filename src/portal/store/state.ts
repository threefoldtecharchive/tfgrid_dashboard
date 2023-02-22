import { balanceInterface, getBalance } from "../lib/balance";
import { getTwin, getTwinID } from "../lib/twin";
import { hex2a } from "../lib/util";

export interface accountInterface {
  address: string;
  meta: { genesisHash: string; name: string; source: string };
  type: string;
  active: boolean;
}

export interface PortalState {
  accounts: accountInterface[];
}
export default {
  accounts: [],
};

export declare type UserCredentials = {
  accountAddress: string;
  accountName: string;
  twinID: number;
  balanceFree: number;
  balanceReserved: number;
  relayAddress: string;
  publicKey: string;
  twin: TwinType;
};

export declare type TwinType = {
  id: string;
  relay: string;
  pk: string;
};

export const decodeHex = (input: string) => {
  return hex2a(input);
};

export const setCredentials = async (api: any, account: accountInterface) => {
  const twinID: number = await getTwinID(api, account.address);
  const balance: balanceInterface = await getBalance(api, account.address);
  const twin = await getTwin(api, twinID);
  const credentials: UserCredentials = {
    accountAddress: "",
    relayAddress: "",
    accountName: "",
    publicKey: "",
    balanceFree: 0,
    balanceReserved: 0,
    twinID: 0,
    twin: { id: "", pk: "", relay: "" },
  };
  if (twinID) {
    credentials.accountAddress = account.address;
    credentials.accountName = account.meta.name;
    credentials.balanceFree = balance.free;
    credentials.balanceReserved = balance.reserved;
    credentials.publicKey = twin.pk;
    credentials.relayAddress = twin.relay ? decodeHex(twin.relay) : "null";
    credentials.twinID = twinID;
    credentials.twin = twin;
  }
  return credentials;
};

export const deleteCredentials = () => {
  const credentials: UserCredentials = {
    accountAddress: "",
    relayAddress: "",
    accountName: "",
    publicKey: "",
    balanceFree: 0,
    balanceReserved: 0,
    twinID: 0,
    twin: { id: "", pk: "", relay: "" },
  };
  return credentials;
};
