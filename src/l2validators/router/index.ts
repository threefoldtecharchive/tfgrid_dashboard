import { RouteConfig } from "vue-router";
import ValidatorsView from "@/l2validators/views/Validators.vue";
export const l2validatorRouter: RouteConfig[] = [
    {
        path: "/l2validators/validators",
        name: "validators",
        component: ValidatorsView
    },


];