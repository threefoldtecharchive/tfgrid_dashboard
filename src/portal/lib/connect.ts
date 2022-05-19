import { ApiPromise, WsProvider } from '@polkadot/api'
import config from '../config'
export async function connect () {
    const wsProvider = new WsProvider(config.wsUrl);
    const api = await ApiPromise.create({ provider: wsProvider });
    return api

}