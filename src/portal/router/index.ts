import { RouteConfig } from "vue-router";
import TwinView from "@/portal/views/Twin.vue";
import TransferView from "@/portal/views/Transfer.vue";

export const portalRouter: RouteConfig[] = [
  { path: "/", component: TwinView },
  { path: "/transfer", component: TransferView },
];
