import { IState } from "../store/state";
import { ApiPromise, WsProvider } from "@polkadot/api";
import { ActionContext } from "vuex";
import { types } from "../json/types";

export default async function getChainData({
  state,
}: ActionContext<IState, IState>) {
  const URL = window.configs.polkadot_url;
  const provider = new WsProvider(URL);
  const pricingPolicies = await getPricingPolicies(provider);
  const { specName, specVersion } = await getSpecData(provider);
  const proxyVersion = await fetch(window.configs.proxy_url + "/version")
    .then<{ version: string }>((res) => res.json())
    .then(({ version: value }) => ({ name: "Grid Proxy", value }));

  state.pricingPolicies = pricingPolicies;
  state.versions = [
    {
      name: "Explorer",
      value: window.configs.version,
    },
    proxyVersion,
    { name: "Chain", value: `${specName} v${specVersion}` },
  ];

  provider.disconnect();
}
function _toString(bytes: ArrayLike<number>): string {
  return Array.from(bytes, (byte) => String.fromCharCode(byte)).join("");
}

function getPricingPolicies(
  provider: WsProvider
): Promise<Map<number, string>> {
  return ApiPromise.create({ provider, types })
    .then((api) => {
      return api.query.tfgridModule.pricingPolicies.entries();
    })
    .then(([[_, ...entries]]) => {
      return entries.reduce(
        (
          map,
          {
            id: {
              words: [id],
            },
            name,
          }: any
        ) => {
          return map.set(id, _toString(name));
        },
        new Map<number, string>()
      );
    });
}

function getSpecData(wsProvider: WsProvider) {
  return ApiPromise.create({ provider: wsProvider }).then((api) => {
    return api.query.system.lastRuntimeUpgrade().then((result: any) => {
      const { specName, specVersion } = result?.toJSON() as {
        specName: string;
        specVersion: number;
      };
      return { specName, specVersion };
    });
  });
}
