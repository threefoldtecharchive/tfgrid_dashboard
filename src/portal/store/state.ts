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
  twinIP: string;
  balanceFree: number;
  balanceReserved: number;
};
