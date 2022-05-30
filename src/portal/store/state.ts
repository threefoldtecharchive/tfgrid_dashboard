
export interface accountInterface {
    address: string;
    meta: { genesisHash: string; name: string; source: string };
    type: string;
  }

export interface PortalState{
    accounts:accountInterface[],
   


}
export default{
    accounts:[],
 
}