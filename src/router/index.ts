import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import ExplorerView from "@/explorer/Explorer.vue";
import { explorerRouter } from "@/explorer/router";
import PortalView from "@/portal/Portal.vue";
import CalculatorView from "@/calculator/Calculator.vue";
import { portalRouter } from "@/portal/router";
import { calculatorRouter } from "@/calculator/router";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    component: PortalView,
    path: "/",
    children: portalRouter,
  },
  {
    component: ExplorerView,
    path: "/explorer",
    children: explorerRouter,
  },
  {
    component: CalculatorView,
    path: "/calculator",
    children: calculatorRouter,
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
