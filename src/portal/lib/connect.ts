import { ApiPromise, WsProvider } from '@polkadot/api'
import { web3FromAddress } from '@polkadot/extension-dapp';
import config from '../config'
import types from './types.json'
import { Client } from 'tfgrid-api-client';

export async function connect() {

    const wsProvider = new WsProvider(config.wsUrl);
    const api = await ApiPromise.create({ provider: wsProvider, types });
    const [chain, nodeName, nodeVersion] = await Promise.all([
        api.rpc.system.chain(),
        api.rpc.system.name(),
        api.rpc.system.version()
    ])
    console.log(`You are connected to chain ${chain} using ${nodeName} v${nodeVersion}`)
    return api

}
export async function createClient(address: string) {
    const injector = await web3FromAddress(address)
    const client = new Client(config.wsUrl, "", "sr25519", { signer: injector.signer, address })
    try {
        await client.init()
        return client
    } catch (err) {
        return err
    }
}