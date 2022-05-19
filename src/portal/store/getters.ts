import { PortalState } from "./state";
import { GetterTree } from "vuex";
export default {
    balance: (state: PortalState) => state.balance,
    accounts: (state: PortalState) => state.accounts,


}as GetterTree<PortalState, PortalState>;