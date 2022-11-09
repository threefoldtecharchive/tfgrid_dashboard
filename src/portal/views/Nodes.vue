<template>
  <v-container>
    <!-- <v-text-field
      v-model="searchTerm"
      color="primary darken-2"
      label="Search by node location or ID"
    ></v-text-field> -->

    <v-card>
      <v-tabs
        v-model="activeTab"
        background-color="deep-blue accent-4"
        centered
        dark
        @change="onChangeTab()"
      >
        <v-tab
          v-for="tab in tabs"
          :key="tab.index"
          :value="tab.query"
          :href="'#' + tab.query"
        >
          {{ tab.label }}
        </v-tab>
      </v-tabs>

      <v-tabs-items v-model="activeTab">
        <v-tab-item v-for="tab in tabs" :key="tab.index" :value="tab.query">
          <v-data-table
            :headers="headers"
            :items="tab.nodes"
            :single-expand="singleExpand"
            :expanded.sync="expanded"
            show-expand
            :disable-sort="true"
            item-key="nodeId"
            class="elevation-1"
            sort-by="item.nodeId"
            :loading="loading"
            loading-text="loading nodes ..."
            :server-items-length="$store.getters['portal/getTableCount']"
            :items-per-page="10"
            :footer-props="{
              'items-per-page-options': [5, 10, 15, 50],
            }"
            @update:options="onUpdateOptions($event.page, $event.itemsPerPage)"
          >
            <template v-slot:[`item.resources.mru`]="{ item }">
              {{ byteToGB(item.resources.mru) }}
            </template>
            <template v-slot:[`item.resources.sru`]="{ item }">
              {{ byteToGB(item.resources.sru) }}
            </template>
            <template v-slot:[`item.resources.hru`]="{ item }">
              {{ byteToGB(item.resources.hru) }}
            </template>
            <template v-slot:[`item.actions`]="{ item }">
              <NodeActionBtn :nodeId="item.nodeId" :status="item.rentStatus" />
            </template>
            <template v-slot:[`item.discount`]="{ item }">
              <v-tooltip bottom color="primary" close-delay="700">
                <template v-slot:activator="{ on, attrs }">
                  <span v-bind="attrs" v-on="on">{{ item.discount }} *</span>
                </template>
                <span
                  >Discounts: <br />
                  <ul>
                    <li>
                      {{ item.applyedDiscount.first }}% for the dedicated node
                    </li>
                    <li>
                      {{ item.applyedDiscount.second }}% for the twin balance
                    </li>
                  </ul>
                  See
                  <a
                    target="_blank"
                    href="https://library.threefold.me/info/threefold/#/tfgrid/grid/pricing?id=discount-levels"
                  >
                    <p style="color: blue; display: inline">discount levels</p>
                  </a>
                </span>
              </v-tooltip>
            </template>
            <template v-slot:expanded-item="{ headers, item }">
              <td :colspan="headers.length">
                <NodeDetails :node="item" :byteToGB="byteToGB" />
              </td>
            </template>
          </v-data-table>
        </v-tab-item>
      </v-tabs-items>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import NodeActionBtn from "../components/NodeActionBtn.vue";
import NodeDetails from "../components/NodeDetails.vue";
import { Component, Vue, Watch } from "vue-property-decorator";
import { getDNodes, ITab } from "../lib/nodes";
import { byteToGB } from "../lib/nodes";

@Component({
  name: "NodesView",
  components: { NodeActionBtn, NodeDetails },
})
export default class NodesView extends Vue {
  $api: any;
  singleExpand = true;
  expanded: any = [];
  loading = true;
  address = "";
  searchTerm = "";
  accountName: any = "";
  $currentTwinID: any = 0;

  activeTab = "";

  tabs: ITab[] = [
    {
      label: "Rentable",
      query: "rentable",
      index: 1,
      page: 1,
      size: 10,
      nodes: [],
    },
    {
      label: "Rented",
      query: "rented",
      index: 2,
      page: 1,
      size: 10,
      nodes: [],
    },
    {
      label: "Mine",
      query: "rented_by",
      index: 3,
      page: 1,
      size: 10,
      nodes: [],
    },
  ];

  headers = [
    { text: "Node ID", value: "nodeId", align: "center" },
    { text: "Location", value: "location.country", align: "center" },
    { text: "CRU", value: "resources.cru", align: "center" },
    { text: "HRU (GB)", value: "resources.hru", align: "center" },
    { text: "MRU (GB)", value: "resources.mru", align: "center" },
    { text: "SRU (GB)", value: "resources.sru", align: "center" },
    { text: "Price (USD)", value: "discount", align: "center" },
    { text: "Actions", value: "actions", align: "center", sortable: false },
  ];

  async mounted() {
    this.address = this.$route.params.accountID;
    this.accountName = this.$route.query.accountName;
    this.$currentTwinID = this.$route.query.twinID;
    if (this.$api) {
      // await this.getNodes();
    } else {
      this.$router.push({
        name: "accounts",
        path: "/",
      });
    }
  }
  updated() {
    this.address;
  }

  @Watch("$route.params.accountID") async onPropertyChanged(
    value: string,
    oldValue: string
  ) {
    console.log(`removing nodes of ${oldValue}, putting in nodes of ${value}`);
    await this.getNodes();
  }

  async onUpdateOptions(pageNumber: number, pageSize: number) {
    let idx = this.tabs.findIndex((tab) => tab.query == this.activeTab);
    this.tabs[idx].page = pageNumber;
    this.tabs[idx].size = pageSize;

    await this.getNodes();
  }

  async onChangeTab() {
    await this.getNodes();
  }

  async getNodes() {
    this.loading = true;

    let idx = this.tabs.findIndex((tab) => tab.query == this.activeTab);
    let { query, page, size } = this.tabs[idx];

    this.tabs[idx].nodes = []

    console.log(
      `Requesting new nodes for tab: ${query}, page: ${page}, size: ${size}`
    );

    this.tabs[idx].nodes = await getDNodes(
      this.$api,
      this.address,
      this.$currentTwinID,
      this.$store,
      query,
      page,
      size,
    );

    this.loading = false;
  }

  byteToGB(capacity: number) {
    return byteToGB(capacity);
  }
}
</script>
<style>
.v-data-table-header th {
  white-space: nowrap;
}
</style>

<style scoped>
.v-tooltip__content {
  pointer-events: initial;
}
</style>