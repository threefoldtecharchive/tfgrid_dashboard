import { PortalState } from './state';
import type { ActionContext } from "vuex";
import {
   web3Enable,web3AccountsSubscribe

  } from '@polkadot/extension-dapp';
  
export default{
    async subscribeAccounts({commit}: ActionContext<PortalState, PortalState>){
        const extensions = await web3Enable('TF Chain UI')
        if(extensions.length === 0){
            console.log('sign into polkadot')
        }
        // this is the function of type `() => void` that should be called to unsubscribe
    
        // we subscribe to any account change and log the new list.
        // note that `web3AccountsSubscribe` returns the function to unsubscribe
        await web3AccountsSubscribe(( injectedAccounts ) => { 
            commit('setAccounts', { accounts: injectedAccounts })
            injectedAccounts.map(( account ) => {
                console.log(account.address);
            })
        });


        // don't forget to unsubscribe when needed, e.g when unmounting a component
     

    },
    async unsubscribeAccounts({commit}:ActionContext<PortalState, PortalState> ){
        const unsubscribe = await web3AccountsSubscribe(( ) => { 
            console.log(`unsubscribing`)
        });
        unsubscribe && unsubscribe();
        commit('removeAccounts')
    }
}