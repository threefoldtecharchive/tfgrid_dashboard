import Vue from "vue";
import Dashboard from "./Dashboard.vue";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";
import Toasted from 'vue-toasted'

Vue.config.productionTip = false;

Vue.use(Toasted, {
  position: 'bottom-right',
  duration: 4000
})

  new Vue({
    router,
    store,
    vuetify,
    render: (h) => h(Dashboard),
  }).$mount("#app");

 


