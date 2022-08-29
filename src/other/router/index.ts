import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import HubView from "../views/HubView.vue";
import BootstrapView from "../views/BootstrapView.vue";

Vue.use(VueRouter);

export const otherRoutes: Array<RouteConfig> = [
  {
    path: "/other/hub",
    component: HubView,
  },
  {
    path: "/other/bootstrap",
    component: BootstrapView,
  },
];
