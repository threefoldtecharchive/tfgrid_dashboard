import { Keyring } from '@polkadot/keyring'

  export function checkAddress (address: string) {
    const keyring = new Keyring({ type: 'sr25519' })
    try {
      keyring.addFromAddress(address)
      return true
    } catch (error) {
      console.log(error)
      return false
    }
  }