import Vue from "vue";
import Dashboard from "./Dashboard.vue";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";

import { explorerConfigs } from "./explorer/config";

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  vuetify,
  ...explorerConfigs,
  render: (h) => h(Dashboard),
}).$mount("#app");
