import { PortalState } from './state';
import type { ActionContext } from "vuex";
import {
    web3Accounts,

  } from '@polkadot/extension-dapp';
  
export default{
    async getAccounts({ commit }: ActionContext<PortalState, PortalState>) {
        console.log('dispatching get accounts')
        const accounts = await web3Accounts()
        commit('setAccounts', { accounts: accounts })
      }
}