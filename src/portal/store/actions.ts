import { PortalState } from './state';
import type { ActionContext } from "vuex";
import {
    web3Accounts,  web3Enable,

  } from '@polkadot/extension-dapp';
  
export default{
    async getAccounts({ commit }: ActionContext<PortalState, PortalState>) {
        await web3Enable('TF Chain UI')
        const accounts = await web3Accounts()
        commit('setAccounts', { accounts: accounts })
      }
}