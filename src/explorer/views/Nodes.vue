<template>
  <Layout pageName="Nodes">
    <template v-slot:filters>
      <LayoutFilters
        :items="filters.map((f) => f.label)"
        v-model="activeFiltersKeys"
      />
    </template>

    <template v-slot:active-filters>
      <div v-for="filter in activeFilters" :key="filter.key">
        <InFilter
          key1="nodes"
          :key2="filter.key"
          :label="filter.placeholder"
          v-if="filter.type === 'in'"
        />
        <RangeFilter
          v-if="filter.type === 'range'"
          key1="nodes"
          :key2="filter.key"
          :label="filter.placeholder"
          :max="filter.max"
          :unit="filter.unit"
        />
        <ConditionFilter
          v-if="filter.type === 'condition'"
          key1="nodes"
          :key2="filter.key"
          :labels="filter.placeholder"
        />
        <ComparisonFilter
          key1="nodes"
          :key2="filter.key"
          :label="filter.placeholder"
          :prefix="filter.prefix"
          v-if="filter.type === 'comparison'"
        />
      </div>
    </template>

    <template v-slot:table>
      <div
        style="
          display: flex;
          flex-direction: column;
          align-items: flex-end;
          justify-content: center;
        "
      >
        <div>
          <v-switch
            v-model="withGateway"
            style="margin-bottom: -30px"
            label="Gateways"
          />
          <v-switch v-model="onlyOnline" label="Online" />
        </div>
      </div>
      <div class="d-flex justify-center">
        <v-alert dense text type="success">
          Node statuses are updated every 2 hours.
        </v-alert>
      </div>
      <v-data-table
        ref="table"
        :loading="$store.getters['explorer/tableLoading']"
        loading-text="Loading..."
        :headers="headers"
        :items="listNodes()"
        :items-per-page="10"
        class="elevation-1"
        align
        @click:row="openSheet"
      >
        <template v-slot:[`item.created`]="{ item }">
          {{ item.created | date }}
        </template>

        <template v-slot:[`item.hru`]="{ item }">
          {{ item.hru | toTeraOrGigaOrPeta }}
        </template>

        <template v-slot:[`item.sru`]="{ item }">
          {{ item.sru | toTeraOrGigaOrPeta }}
        </template>

        <template v-slot:[`item.mru`]="{ item }">
          {{ item.mru | toTeraOrGigaOrPeta }}
        </template>

        <template v-slot:[`item.uptime`]="{ item }">
          {{ item.uptime | secondToRedable }}
        </template>

        <template v-slot:[`item.status`]="{ item }">
          <p class="text-left mt-1 mb-0">
            <v-chip :color="getStatus(item).color">{{
              getStatus(item).status
            }}</v-chip>
          </p>
        </template>

      </v-data-table>
    </template>

    <template v-slot:details>
      <DetailsV2
        :open="!!node"
        :query="query"
        :variables="
          node
            ? {
                nodeId: node.nodeId,
                farmId: node.farmId,
                twinId: node.twinId,
                country: node.country === 'United States'? 'United States of America' : node.country,
              }
            : {}
        "
        :nodeId="node && node.nodeId"
        v-on:close-sheet="closeSheet"
      />
    </template>

    <!-- <template v-slot:default>
      <NodesDistribution :nodes="listNodes()" />
    </template> -->
  </Layout>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import DetailsV2 from "../components/DetailsV2.vue";
import { INode } from "../graphql/api";
import Layout from "../components/Layout.vue";
import InFilter from "../components/InFilter.vue";
import RangeFilter from "../components/RangeFilter.vue";
import ConditionFilter from "../components/ConditionFilter.vue";
import ComparisonFilter from "../components/ComparisonFilter.vue";
import LayoutFilters from "../components/LayoutFilters.vue";
import gql from "graphql-tag";

@Component({
  components: {
    Layout,
    DetailsV2,
    InFilter,
    RangeFilter,
    ConditionFilter,
    ComparisonFilter,
    LayoutFilters,
  },
})
export default class Nodes extends Vue {
  withGateway = false;
  onlyOnline = true;

  headers = [
    { text: "ID", value: "nodeId" },
    { text: "Farm ID", value: "farmId", align: "center" },
    { text: "Total Public IPs", value: "totalPublicIPs", align: "center" },
    { text: "Free Public IPs", value: "freePublicIPs", align: "center" },
    { text: "HRU", value: "hru", align: "center" },
    { text: "SRU", value: "sru", align: "center" },
    { text: "MRU", value: "mru", align: "center" },
    { text: "CRU", value: "cru", align: "center" },
    { text: "Up Time", value: "uptime", align: "center" },
    { text: "Status", value: "status", align: "center" },
    
  ];

  activeFiltersKeys: string[] = ["MRU", "HRU", "CRU"];

  get activeFilters() {
    const keySet = new Set(this.activeFiltersKeys);
    return this.filters.filter((filter) => keySet.has(filter.label));
  }

  filters = [
    {
      label: "Node ID",
      type: "in",
      key: "nodeId",
      placeholder: "Filter by node id.",
    },
    {
      label: "Farm ID",
      type: "in",
      key: "farmId",
      placeholder: "Filter by farm id.",
    },
    {
      label: "Twin ID",
      type: "in",
      key: "twinId",
      placeholder: "Filter by twin id.",
    },
    {
      label: "Country Full Name",
      type: "in",
      key: "countryFullName",
      placeholder: "Filter by country.",
    },
    {
      label: "Farming Policy",
      type: "in",
      key: "farmingPolicyName",
      placeholder: "Filter by farming policy name.",
    },
    {
      label: "SRU",
      type: "range",
      key: "sru",
      placeholder: "sru",
      max: 1e12 * 10, // 1e12 is Terra and we want here 10 Terrabytes
      unit: "TB",
    },
    {
      label: "HRU",
      type: "range",
      key: "hru",
      placeholder: "hru",
      max: 1e12 * 1000, // 1e12 is Terra and we want here 1000 Terrabytes
      unit: "TB",
    },
    {
      label: "MRU",
      type: "range",
      key: "mru",
      placeholder: "mru",
      max: 1e12 * 10, // 1e12 is Terra and we want here 10 Terrabytes
      unit: "TB",
    },
    {
      label: "CRU",
      type: "range",
      key: "cru",
      placeholder: "cru",
      max: 64 * 3,
      unit: "core",
    },
    {
      label: "Free Public IP",
      type: "comparison",
      key: "freePublicIPs",
      placeholder: "Filter by greater than or equal to publicIp Number.",
      prefix: ">=",
    },
    {
      label: "Certification Type",
      type: "in",
      key: "certificationType",
      placeholder: "Filter by certification type",
      value: ["Diy", "Certified"],
    },
  ];

  listNodes() {
    let nodes: INode[] = this.$store.getters["explorer/listFilteredNodes"];
    if (this.withGateway) {
      nodes = nodes.filter(({ publicConfig }) => publicConfig?.domain !== "");
    }

    if (this.onlyOnline) {
      nodes = nodes.filter(({ status }) => status === "up");
    }

    return nodes;
  }

  getStatus(node: { status: string }) {
    if (node.status === "up")
      return { color: "green", status: "up" };
    else 
      return { color: "red", status: "down" };
  }

  toggleActive(label: string): void {
    this.activeFiltersKeys = this.activeFiltersKeys.filter((x) => x !== label);
  }

  node: INode | null = null;
  query = gql`
    query getNodeDetails(
      $nodeId: Int!
      $farmId: Int!
      $twinId: Int!
      $country: String!
    ) {
      node: nodes(where: { nodeID_eq: $nodeId }) {
        country
        city
        location {
          latitude
          longitude
        }
        nodeId: nodeID
        farmId: farmID
        farmingPolicyId
        gridVersion
        uptime
        created
        updatedAt
        certificationType: certification
        interfaces {
          id
          name
          mac
          ips
        }
        publicConfig {
          ipv4
          gw4
          ipv6
          gw6
          domain
        }
        farmingPolicyId
      }

      farm: farms(where: { farmID_eq: $farmId }) {
        id
        farmId: farmID
        name
        gridVersion
        certificationType: certification
        stellarAddress
      }

      twin: twins(where: { twinID_eq: $twinId }) {
        id
        twinId: twinID
        accountId: accountID
        gridVersion
        ip
      }

      country: countries(where: { name_eq: $country, OR: {code_eq: $country}}) {
        code
      }
    }
  `;

  openSheet(node: INode): void {
    this.node = node;
  }

  closeSheet(): void {
    this.node = null;
  }
}
</script>

