import { Keyring } from '@polkadot/keyring'
export interface balanceInterface {
  free: number;
  reserved: number;
}

export async function getBalance(api: { query: { system: { account: (arg0: string) => { data: { free: { toJSON: () => number; }; reserved: { toJSON: () => number; }; } } } } }, address: string) {
  const res = await api.query.system.account(address)

  return { free: res.data.free.toJSON() / 1e7, reserved: res.data.reserved.toJSON() / 1e7 }

}

export async function getMoreFunds(substrateAccountID: string, api: { tx: { balances: { transfer: (arg0: string, arg1: number) => any } } }, callback: any) {
  const keyring = new Keyring({ type: 'sr25519' })
  const alice = keyring.addFromUri('//Alice')

  const transfer = await api.tx.balances.transfer(substrateAccountID, 100 * 1e7)

  transfer.signAndSend(alice, callback)
}