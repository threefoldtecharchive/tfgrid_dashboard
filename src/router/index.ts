import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import ExplorerView from "@/explorer/Explorer.vue";
import { explorerRouter } from "@/explorer/router";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    component: ExplorerView,
    path: "/explorer",
    children: explorerRouter,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
