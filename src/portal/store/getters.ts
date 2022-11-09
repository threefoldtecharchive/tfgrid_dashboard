import { PortalState } from "./state";
import { GetterTree } from "vuex";

export default {
  accounts: (state: PortalState) => state.accounts,
  getTableCount: (state: PortalState) => state.tableCount,
} as GetterTree<PortalState, PortalState>;
