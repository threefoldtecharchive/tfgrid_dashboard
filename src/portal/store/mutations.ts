
import { PortalState } from "./state"

export enum PortalMutationTypes {
  SET_ACCOUNTS = 'setAccounts'
}
export default {
  setAccounts(state: PortalState, payload: { accounts: [] }) {
    state.accounts = payload.accounts
  },
  removeAccounts(state: PortalState) {
    state.accounts = []
  },

}