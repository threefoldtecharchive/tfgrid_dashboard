import { RouteConfig } from "vue-router";
import AccountsView from '@/portal/views/Accounts.vue';
import AccountView from '@/portal/views/Account.vue'
import TwinView from "@/portal/views/Twin.vue";
import TransferView from "@/portal/views/Transfer.vue";

export const portalRouter: RouteConfig[] = [
  { path: "/", 
  name:"Accounts",
  component: AccountsView },
  { path: "/:accountID:accountName",
   name: "Account", 
   component: AccountView 
 },
  { path: "/:accountID/twin",
  name: "Twin", 
   component: TwinView },
  { path: "/:accountID/transfer", 
  name: "Transfer", 
  component: TransferView },
];
