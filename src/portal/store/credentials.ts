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
      accountAddress: "",
      accountName: "",
      twinID: 0,
      balanceFree: 0,
      balanceReserved: 0,
      relayAddress: "",
      publicKey: "",
      twin: {
        id: "",
        relay: "",
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
        state.accountAddress = payload.account.address;
        state.accountName = payload.account.meta.name;
        state.balanceFree = balance.free;
        state.balanceReserved = balance.reserved;
        state.publicKey = twin.pk;
        state.relayAddress = twin.relay ? decodeHex(twin.relay) : "null";
        state.twinID = twinID;
        state.twin = twin;
      } else {
        state.accountAddress = payload.account.address;
        state.accountName = payload.account.meta.name;
      }
      return state;
    },
    UNSET_CREDENTIALS(state: UserCredentials) {
      state.initialized = false;
      state.accountAddress = "";
      state.accountName = "";
      state.twinID = 0;
      state.balanceFree = 0;
      state.balanceReserved = 0;
      state.relayAddress = "";
      state.publicKey = "";
      state.twin = { id: "", relay: "", pk: "" };
      return state;
    },
  },
} as unknown as ModuleTree<UserCredentials>;
