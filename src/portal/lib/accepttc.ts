import { web3FromAddress } from "@polkadot/extension-dapp"

export async function acceptTermsAndCondition (api: any, address: string, documentLink: string, documentHash: string, callback: any) {
    const injector = await web3FromAddress(address)
    return api.tx.tfgridModule
      .userAcceptTc(documentLink, documentHash)
      .signAndSend(address, { signer: injector.signer }, callback)
  }
  export async function userAcceptedTermsAndConditions (api: any, address: string) {
    const tcs = await api.query.tfgridModule.usersTermsAndConditions(address)
    const parsedTcs = tcs.toJSON()
    return parsedTcs.length > 0
  }