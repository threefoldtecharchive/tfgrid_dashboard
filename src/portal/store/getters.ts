import { PortalState } from "./state";
import { GetterTree } from "vuex";
export default {
    api: (state: PortalState) => state.api ,
    accounts: (state: PortalState) => state.accounts

}as GetterTree<PortalState, PortalState>;