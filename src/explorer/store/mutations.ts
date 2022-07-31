import { byInternet } from "country-code-lookup";
import { INode } from "./../graphql/api";
import { GetDataQueryType } from "../graphql/api";
import { IState } from "./state";

export enum MutationTypes {
  SET_LOAD = "setLoad",
  SET_TABLE_LOAD = "setTableLoad",
  SET_DATA = "setData",
  SET_FILTER_ENABLE = "setFilterEnable",
  SET_FILTER_VALUE = "setFilterValue",
  SET_POLICIES = "setPolicies",
  SET_NODES_STATUS = "setNodesStatus",
  SET_PRICING_POLICIES = "setPricingPolicies",
  LOAD_NODES_DATA = "loadNodesData",
}

interface ISetNodeFilter {
  key1: keyof IState["filters"];
  key2: any;
  value: any;
}

export default {
  setLoad(state: IState, payload: boolean) {
    state.loading = payload;
  },
  setTableLoad(state: IState, payload: boolean) {
    state.tableLoading = payload;
  },
  setData(state: IState, payload: GetDataQueryType) {
    state.data = payload;
  },
  setPolicies(state: IState, payload: any) {
    state.policies = payload;
  },
  setPricingPolicies(state: IState, payload: Map<number, string>) {
    state.pricingPolicies = payload;
  },
  setFilterEnable(state: IState, { key1, key2, value }: ISetNodeFilter) {
    (state.filters[key1] as any)[key2].enabled = value;
  },
  setFilterValue(state: IState, { key1, key2, value }: ISetNodeFilter) {
    (state.filters[key1] as any)[key2].value = value;
  },
  setNodesStatus(state: IState, payload: { [key: number]: boolean }) {
    state.nodes_status = payload;
  },
  async loadNodesData(state: IState, payload: any): Promise<void> {
    const farms = await payload.farms;
    const nodes = await payload.nodes;
    for (let i = 0; i < nodes.length; i++) {
      const node: INode = {
        id: nodes[i].id,
        createdAt: nodes[i].createdAt,
        createdById: "",
        updatedAt: nodes[i].updatedAt,
        updatedById: "",
        deletedAt: nodes[i].deletedAt,
        deletedById: "",
        version: nodes[i].version,
        gridVersion: nodes[i].gridVersion,
        nodeId: nodes[i].nodeId,
        farmId: nodes[i].farmId,
        twinId: nodes[i].twinId,
        cityId: 0,

        totalPublicIPs: farms.find(
          (farm: any) => farm.farmId === nodes[i].farmId
        )?.publicIps.length,
        freePublicIPs: farms
          .find((farm: any) => farm.farmId === nodes[i].farmId)
          ?.publicIps.filter((ip: any) => ip.contractId === 0).length,
        hru: nodes[i].total_resources.hru,
        sru: nodes[i].total_resources.sru,
        cru: nodes[i].total_resources.cru,
        mru: nodes[i].total_resources.mru,
        publicConfig: nodes[i].publicConfig,
        uptime: nodes[i].uptime,
        created: nodes[i].created,
        farmingPolicyId: nodes[i].farmingPolicyId,
        location: nodes[i].location,
        country: nodes[i].country,
        city: nodes[i].city,
        interfaces: [
          {
            name: "",
            mac: "",
            ips: "",
            id: "",
          },
        ],
        status: nodes[i].status,
        certificationType: nodes[i].certificationType,
        farmingPolicyName: state.policies[nodes[i].farmingPolicyId],
        countryFullName:
          nodes[i].country && nodes[i].country?.length == 2
            ? byInternet(nodes[i].country)?.country
            : nodes[i].country,
      };

      state.nodes.push(node);
    }
  },
};
