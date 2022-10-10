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
        <NodeFilter :filterKey="filter.key" :label="filter.label" />
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
            label="Gateways (Only)"
            style="margin-bottom: -30px"
            v-model="gatewayFilter"
            @change="loadNodesData"
          />
          <v-switch
            label="Online (Only)"
            v-model="onlineFilter"
            @change="loadNodesData"
          />
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
        :items="$store.getters['explorer/nodes']"
        :server-items-length="$store.getters['explorer/getNodesCount']"
        :items-per-page="10"
        class="elevation-1"
        align
        @click:row="openSheet"
        @update:options="onUpdateOptions($event.page, $event.itemsPerPage)"
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
                country:
                  node.country === 'United States'
                    ? 'United States of America'
                    : node.country,
              }
            : {}
        "
        :nodeId="node && node.nodeId"
        v-on:close-sheet="closeSheet"
      />
    </template>
  </Layout>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import DetailsV2 from "../components/DetailsV2.vue";
import { INode } from "../graphql/api";
import Layout from "../components/Layout.vue";
import LayoutFilters from "../components/LayoutFilters.vue";
import gql from "graphql-tag";
import NodeFilter from "../components/NodeFilter.vue";

@Component({
  components: {
    Layout,
    DetailsV2,
    LayoutFilters,
    NodeFilter,
  },
})

export default class Nodes extends Vue {

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

  filters = [
    {
      label: "Node ID",
      key: "node_id",
      placeholder: "Filter by node id.",
    },
    {
      label: "Twin ID",
      key: "twin_id",
      placeholder: "Filter by twin id.",
    },
    {
      label: "Farm IDs",
      key: "farm_ids",
      placeholder: "Filter by farm ids.",
    },
    {
      label: "Country Full Name",
      key: "country",
      placeholder: "Filter by country.",
    },
    {
      label: "Storage (GB)",
      key: "free_sru",
      placeholder: "sru",
    },
    {
      label: "Hard Storage (GB)",
      key: "free_hru",
      placeholder: "hru",
    },
    {
      label: "Memory (GB)",
      key: "free_mru",
      placeholder: "mru",
    },
    {
      label: "CPU (Cores)",
      key: "free_cru",
      placeholder: "cru",
    },
    {
      label: "Free Public IP",
      key: "free_ips",
      placeholder: "Filter by greater than or equal to publicIp Number.",
    },
  ];

  activeFiltersKeys: string[] = ["Node ID"];

  get activeFilters() {
    const keySet = new Set(this.activeFiltersKeys);
    return this.filters.filter((filter) => keySet.has(filter.label));
  }

  // Filter computed props, two-way binding on store.
  get gatewayFilter() {
    return this.$store.getters["explorer/getNodesGatewayFilter"];
  }

  set gatewayFilter(value) {
    this.$store.commit("explorer/setGatewayFilter", value);
  }

  get onlineFilter() {
    return this.$store.getters["explorer/getNodesUpFilter"];
  }

  set onlineFilter(value) {
    this.$store.commit("explorer/setUpFilter", value);
  }

  // update the page/size of the request
  onUpdateOptions(pageNumber: number, pageSize: number) {
    this.$store.commit("explorer/setNodesTablePageNumber", pageNumber);
    this.$store.commit("explorer/setNodesTablePageSize", pageSize);

    // reload if the page/size changed; leads to double requests at init
    this.loadNodesData();
  }

  // reload the nodes table
  loadNodesData() {
    this.$store.dispatch("explorer/loadNodesData");
  }

  getStatus(node: { status: string }) {
    if (node.status === "up") return { color: "green", status: "up" };
    else return { color: "red", status: "down" };
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

      country: countries(
        where: { name_eq: $country, OR: { code_eq: $country } }
      ) {
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

