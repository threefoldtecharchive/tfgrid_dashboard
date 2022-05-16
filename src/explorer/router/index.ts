import { RouteConfig } from "vue-router";
import StatisticsView from "@/explorer/views/Statistics.vue";
import NodesView from "@/explorer/views/Nodes.vue";
import FarmsView from "@/explorer/views/Farms.vue";

export const explorerRouter: RouteConfig[] = [
  { path: "/explorer/statistics", component: StatisticsView },
  { path: "/explorer/nodes", component: NodesView },
  { path: "/explorer/farms", component: FarmsView },
];
