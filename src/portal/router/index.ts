import { RouteConfig } from "vue-router";
import AccountsView from '@/portal/views/Accounts.vue';
import AccountView from '@/portal/views/Account.vue'
import TransferView from "@/portal/views/Transfer.vue";

export const portalRouter: RouteConfig[] = [
  { path: "/", 
  name:"Accounts",
  component: AccountsView },
  { path: "/:accountID",
   name: "Account", 
   component: AccountView 
 },
  { path: "/:accountID/transfer", 
  name: "Transfer", 
  component: TransferView },
];
