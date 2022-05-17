import { RouteConfig } from "vue-router";
import AccountsView from '@/portal/views/Accounts.vue';
import TwinView from "@/portal/views/Twin.vue";
import TransferView from "@/portal/views/Transfer.vue";

export const portalRouter: RouteConfig[] = [
  { path: "/", 
  name:"Accounts",
  component: AccountsView },
  { path: "/:accountID/twin",
  name: "Twin", 
   component: TwinView },
  { path: "/:accountID/transfer", 
  name: "Transfer", 
  component: TransferView },
];
