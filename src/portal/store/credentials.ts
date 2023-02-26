import Vue from "vue";
import Vuex, { ModuleTree } from "vuex";
import { balanceInterface, getBalance } from "../lib/balance";
import { getTwin, getTwinID } from "../lib/twin";
import { accountInterface } from "./state";
import { UserCredentials } from "./types";
import { hex2a } from "../lib/util";

Vue.use(Vuex);

export const decodeHex = (input: string) => {
  return hex2a(input);
};

export const credentialsStore = {
  state() {
    return {
      initialized: false,
      loading: true,
      balance: {
        free: 0,
        reserved: 0,
      },
      twin: {
        address: "",
        relay: "",
        name: "",
        id: "",
        pk: "",
      },
    };
  },
  mutations: {
    async SET_CREDENTIALS(state: UserCredentials, payload: { api: any; account: accountInterface }) {
      const twinID: number = await getTwinID(payload.api, payload.account.address);
      const balance: balanceInterface = await getBalance(payload.api, payload.account.address);
      const twin = await getTwin(payload.api, twinID);

      if (twinID) {
        payload.account.active = true;
        state.initialized = true;
        state.loading = true;
        state.twin = twin;
        state.balance = balance;
        state.twin.relay = twin.relay ? decodeHex(twin.relay) : "null";
      }
      state.twin.address = payload.account.address;
      state.twin.name = payload.account.meta.name;
      state.loading = false;
      return state;
    },
    UNSET_CREDENTIALS(state: UserCredentials) {
      state.initialized = false;
      state.loading = true;
      state.twin = { id: "", relay: "", pk: "", name: "", address: "" };
      state.balance = { free: 0, reserved: 0 };
      return state;
    },
  },
} as unknown as ModuleTree<UserCredentials>;
