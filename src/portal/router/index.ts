import { RouteConfig } from "vue-router";
import TwinView from "@/portal/views/Twin.vue";


export const portalRouter: RouteConfig[] = [
  { path: "/", component: TwinView },
];
