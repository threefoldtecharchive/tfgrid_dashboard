import type { ActionContext } from "vuex";
import type { IState } from "./state";
import { MutationTypes } from "./mutations";
import getChainData from "../utils/getChainData";
import paginated_fetcher from "../utils/paginatedFetch";
export enum ActionTypes {
  INIT_POLICIES = "explorer/initPolicies",
  INIT_PRICING_POLICIES = "explorer/initPricingPolicies",
  LOAD_DATA = "explorer/loadData",
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
    commit("setTableLoad", true);
    const nodes = await paginated_fetcher(
      `${window.configs.proxy_url}/nodes`,
      1,
      50
    );
    const farms = await paginated_fetcher(
      `${window.configs.proxy_url}/farms`,
      1,
      50
    );

    commit("loadNodesData", { nodes, farms });
    commit("setTableLoad", false);
  },

  loadData({ state, commit }: ActionContext<IState, IState>) {
    commit(MutationTypes.SET_LOAD, true);
    fetch(`${window.configs.proxy_url}/stats?status=up`)
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
