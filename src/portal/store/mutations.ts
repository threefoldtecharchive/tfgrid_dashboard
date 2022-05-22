
import { PortalState } from "./state"

export enum PortalMutationTypes{
 SET_ACCOUNTS = 'setAccounts'
}
export default{
    setAccounts (state: PortalState, payload: {accounts: []}) {
      state.accounts = payload.accounts
    },
    removeAccounts (state: PortalState) {
        state.accounts = []
    },
    setBalance(state: PortalState, payload: {balance: number}){
      state.currentAccountBalance = payload.balance
    }, 
    setCurrentAccountID(state: PortalState, payload: {address: string}){
      state.currentAccountID = payload.address
    },

  
}