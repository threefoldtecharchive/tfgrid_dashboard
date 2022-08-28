import { RouteConfig } from "vue-router";

export const calculatorRouter: RouteConfig[] = [
  {
    path: "/calculator/",
    name: "Calaulator",
    component: () => import("../views/Calculator.vue"),
  }
];
