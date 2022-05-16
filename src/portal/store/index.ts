import Vue from "vue";
import Vuex from "vuex";

interface PortalState {
  name: string;
}

Vue.use(Vuex);

export const portalStore = new Vuex.Store<PortalState>({
  state: {
    name: "hanafy",
  },
});