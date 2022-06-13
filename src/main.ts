import Vue from "vue";
import Dashboard from "./Dashboard.vue";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";
import Toasted from "vue-toasted";
import * as buffer from "buffer";

import { explorerConfigs } from "./explorer/config";

Vue.config.productionTip = false;
window.Buffer = buffer.Buffer;
Vue.use(Toasted, {
  position: "bottom-right",
  duration: 4000,
});

new Vue({
  router,
  store,
  vuetify,
  ...explorerConfigs,
  render: (h) => h(Dashboard),
}).$mount("#app");
