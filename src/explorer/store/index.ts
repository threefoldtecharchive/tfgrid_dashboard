import Vue from "vue";
import Vuex from "vuex";

interface ExplorerState {
  name: string;
}

Vue.use(Vuex);

export const explorerStore = new Vuex.Store<ExplorerState>({
  state: {
    name: "Mohamed & Amira",
  },
});
