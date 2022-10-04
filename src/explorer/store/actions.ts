import type { ActionContext } from "vuex";
import type { IState } from "./state";
import { MutationTypes } from "./mutations";
import getChainData from "../utils/getChainData";
export enum ActionTypes {
  INIT_POLICIES = "explorer/initPolicies",
  INIT_PRICING_POLICIES = "explorer/initPricingPolicies",
  LOAD_DATA = "explorer/loadData",
  LOAD_CHAIN_DATA = "explorer/loadChainData",
  LOAD_NODES_DATA = "explorer/loadNodesData",
}

export default {
  initPolicies({ commit }: ActionContext<IState, IState>) {
    fetch(
      "https://raw.githubusercontent.com/threefoldtech/tfchain/development/farming_policies.json"
    )
      .then<{ id: number; name: string }[]>((res) => res.json())
      .then((items) => {
        return items.map(({ name }) => name);
      })
      .then((data) => {
        commit(MutationTypes.SET_POLICIES, data);
      });
  },

  async loadNodesData({ state, commit }: ActionContext<IState, IState>) {
    commit(MutationTypes.SET_TABLE_LOAD, true);

    let url = `${window.configs.APP_GRIDPROXY_URL}/nodes?ret_count=true`;
    url += `&size=${state.nodesTablePageSize}`;
    url += `&page=${state.nodesTablePageNumber}`;

    // move these to nodesFilter
    if (state.nodesUpFilter) url += "&status=up";
    if (state.nodesGatewayFilter) url += "&ipv4=true&domain=true";

    for (const key in state.nodesFilter) {
      let value = state.nodesFilter[key];

      if (key == "free_hru" || key == "free_mru" || key == "free_sru") {
        value *= 1024 * 1024 * 1024; // convert from gb to b
      }

      url += `&${key}=${value}`;
    }

    console.log({
      status: state.nodesUpFilter,
      gw: state.nodesGatewayFilter,
      filters: state.nodesFilter,
      url,
    });

    const res = await fetch(url);

    const nodesCount: any = res.headers.get("count");
    commit(MutationTypes.SET_NODES_COUNT, +nodesCount);

    const nodes = res.json();
    commit(MutationTypes.LOAD_NODES_DATA, { nodes, farms: [] });

    commit(MutationTypes.SET_TABLE_LOAD, false);
  },

  loadData({ state, commit }: ActionContext<IState, IState>) {
    commit(MutationTypes.SET_LOAD, true);
    fetch(`${window.configs.APP_GRIDPROXY_URL}/stats?status=up`)
      .then((data) => data.json())
      .then((data) => {
        const {
          nodes,
          farms,
          twins,
          contracts,
          publicIps,
          accessNodes,
          countries,
          gateways,
          totalCru,
          totalHru,
          totalMru,
          totalSru,
          nodesDistribution,
        } = data;
        state.nodeContractsNo = contracts;
        state.twinsNo = twins;
        state.farmsNo = farms;
        state.nodesNo = nodes;
        state.publicIpsNo = publicIps;
        state.accessNodesNo = accessNodes;
        state.countriesNo = countries;
        state.gatewaysNo = gateways;
        state.totalCru = totalCru;
        state.totalHru = totalHru;
        state.totalMru = totalMru;
        state.totalSru = totalSru;
        state.nodesDistribution = nodesDistribution;

        return {
          nodes: nodes,
          farms: farms,
        };
      })
      // .then(createDataRequests)
      .then((data) => {
        commit(MutationTypes.SET_DATA, data);
      })
      .catch((err) => {
        /**
         * @todo Should handle this error nicely. :"(
         */
        console.log("something went wrong", err);
      })
      .finally(() => {
        commit(MutationTypes.SET_LOAD, false);
      });
  },
  loadChainData(store: ActionContext<IState, IState>): void {
    getChainData(store);
  },
};
