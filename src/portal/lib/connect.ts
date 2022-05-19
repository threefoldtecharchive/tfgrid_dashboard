import { ApiPromise, WsProvider } from '@polkadot/api'
import config from '../config'
import types from './types.json'
export async function connect () {
    const wsProvider = new WsProvider(config.wsUrl);
    const api = await ApiPromise.create({ provider: wsProvider, types });
    return api

}