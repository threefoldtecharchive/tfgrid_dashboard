import { RouteConfig } from "vue-router";
import AccountsView from '@/portal/views/Accounts.vue';
import AccountView from '@/portal/views/Account.vue'
import TwinView from "@/portal/views/Twin.vue";
import TransferView from "@/portal/views/Transfer.vue";
import FarmsView from "@/portal/views/Farms.vue";
import NodesView from "@/portal/views/Nodes.vue";
export const portalRouter: RouteConfig[] = [
  { path: "/", 
  name:"accounts",
  component: AccountsView },
  { path: "/:accountID",
   name: "account", 
   component: AccountView 
 },
 { path: "/:accountID/twin", 
 name: "twin", 
 component: TwinView },
 { path: "/:accountID/transfer", 
 name: "transfer", 
 component: TransferView },
 { path: "/:accountID/farms", 
 name: "farms", 
 component: FarmsView },
 { path: "/:accountID/nodes", 
 name: "nodes", 
 component: NodesView },

];
