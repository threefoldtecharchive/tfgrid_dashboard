import { PortalState } from "./state";
import { GetterTree } from "vuex";
export default {
    currentAccountBalance: (state: PortalState) => state.currentAccountBalance,
    currentAccountID: (state: PortalState) => state.currentAccountID,
    accounts: (state: PortalState) => state.accounts,


}as GetterTree<PortalState, PortalState>;