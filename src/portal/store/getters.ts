import { PortalState } from "./state";
import { GetterTree } from "vuex";
export default {

    accounts: (state: PortalState) => state.accounts,



} as GetterTree<PortalState, PortalState>;