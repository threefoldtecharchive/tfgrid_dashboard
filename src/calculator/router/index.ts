import { RouteConfig } from "vue-router";

export const calculatorRouter: RouteConfig[] = [
  {
    path: "/calculator/calculator",
    name: "Calaulator",
    component: () => import("../views/Calculator.vue"),
  }
];
