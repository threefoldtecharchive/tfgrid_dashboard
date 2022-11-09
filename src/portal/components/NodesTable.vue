<template>
  <v-container>
    <v-data-table
      :headers="headers"
      :items="nodes"
      :single-expand="true"
      :expanded.sync="expanded"
      show-expand
      :disable-sort="true"
      item-key="nodeId"
      class="elevation-1"
      :loading="loading"
      loading-text="loading nodes ..."
      :server-items-length="count"
      :items-per-page="pageSize"
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
              <li>{{ item.applyedDiscount.first }}% for the dedicated node</li>
              <li>{{ item.applyedDiscount.second }}% for the twin balance</li>
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
  </v-container>
</template>

<script lang="ts">
import NodeActionBtn from "../components/NodeActionBtn.vue";
import NodeDetails from "../components/NodeDetails.vue";
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import { getDNodes, ITab } from "../lib/nodes";
import { byteToGB } from "../lib/nodes";

@Component({
  name: "NodesTable",
  components: { NodeActionBtn, NodeDetails },
})
export default class NodesTable extends Vue {
  @Prop({ required: true }) tab!: ITab;
  @Prop({ required: true }) twinId: any;
  $api: any;
  expanded: any = [];
  loading = true;
  address = "";
  accountName: any = "";

  nodes: any[] = [];
  count = 0;
  pageNumber = 1;
  pageSize = 10;

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

  @Watch("$route.params.accountID") async onPropertyChanged(
    value: string,
    oldValue: string
  ) {
    console.log(`removing nodes of ${oldValue}, putting in nodes of ${value}`);
    await this.getNodes();
  }

  async mounted() {
    console.log("mounted");
    await this.getNodes();
  }

  async onUpdateOptions(pageNumber: number, pageSize: number) {
    this.pageNumber = pageNumber;
    this.pageSize = pageSize;
    await this.getNodes();
  }

  async getNodes() {
    this.nodes = [];
    this.loading = true;

    let { dNodes, count } = await getDNodes(
      this.$api,
      this.address,
      this.twinId,
      this.tab.query,
      this.pageNumber,
      this.pageSize
    );

    this.nodes = dNodes;
    this.count = parseInt(count as string);
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