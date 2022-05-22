
export interface accountInterface {
    address: string;
    meta: { genesisHash: string; name: string; source: string };
    type: string;
  }

export interface PortalState{
    accounts:accountInterface[],
    currentAccountBalance: number, 
    currentAccountID: string, 
    api: any

}
export default{
    accounts:[],
    currentAccountBalance: 0, 
    currentAccountID: ''

}