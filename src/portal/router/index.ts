import { RouteConfig } from "vue-router";
import AccountsView from '@/portal/views/Accounts.vue';
import AccountView from '@/portal/views/Account.vue'
import TwinView from "@/portal/views/Twin.vue";
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

];
