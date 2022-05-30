import { explorerStore } from "@/explorer/store";
import { portalStore} from "@/portal/store";
import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    explorer: explorerStore,
    portal: portalStore
  },
});
