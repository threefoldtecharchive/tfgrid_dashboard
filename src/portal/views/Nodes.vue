<template>
  <v-container>
    <v-card
      color="#388E3C"
      class="text-center py-5 my-3 "
    >
      <h3>You can now reserve nodes from other's farms!</h3>
    </v-card>
    <v-text-field
      v-model="searchTerm"
      color="purple darken-2"
      label="Search by node location or ID"
    ></v-text-field>
    <v-data-table
      :headers="headers"
      :items="filteredNodes()"
      :single-expand="singleExpand"
      :expanded.sync="expanded"
      item-key="nodeId"
      show-expand
      class="elevation-1"
      dark
      sort-by="item.nodeId"
      :loading="loading"
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
        <NodeActionBtn :nodeId="item.nodeId" />
      </template>
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Your Nodes</v-toolbar-title>
        </v-toolbar>
      </template>
      <template v-slot:expanded-item="{ item }">
        <td
          :colspan="headers.length"
          key="item.nodeId"
        >
          <v-container
            fluid
            class="text-left"
          >
            <v-row>
              <v-col>
                <v-flex class="text-left pr-2">Node ID</v-flex>

              </v-col>
              <v-col>
                <v-flex class="text-truncate font-weight-bold">
                  <span>{{ item.nodeId }}</span>
                </v-flex>
              </v-col>
            </v-row>
            <v-row>

            </v-row>

          </v-container>

        </td>
      </template>

    </v-data-table>
  </v-container>
</template>

<script lang="ts">
import NodeActionBtn from "@/components/NodeActionBtn.vue";
import { Component, Vue, Watch } from "vue-property-decorator";
import { getDNodes } from "../lib/nodes";

@Component({
  name: "NodesView",
  components: { NodeActionBtn },
})
export default class NodesView extends Vue {
  headers = [
    { text: "Node ID", value: "nodeId" },
    { text: "Location", value: "location.country" },
    { text: "CRU", value: "resources.cru" },
    { text: "HRU (GB)", value: "resources.hru" },
    { text: "MRU (GB)", value: "resources.mru" },
    { text: "SRU (GB)", value: "resources.sru" },
    { text: "Price (USD)", value: "discount" },
    { text: "Actions", value: "actions" },
  ];
  nodes: any = [];
  $api: any;
  singleExpand = true;
  expanded: any = [];
  loading = false;
  address = "";
  searchTerm = "";
  async mounted() {
    this.address = this.$route.params.accountID;
    if (this.$api) {
      this.nodes = await getDNodes(this.$api, this.address);
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
    this.nodes = await getDNodes(this.$api, value);
    console.log(this.nodes);
  }
  public filteredNodes() {
    if (this.searchTerm.length !== 0) {
      return this.nodes.filter(
        (node: { location: { country: string }; nodeId: any }) =>
          node.location.country
            .toLowerCase()
            .includes(this.searchTerm.toLowerCase()) ||
          `${node.nodeId}`.includes(this.searchTerm)
      );
    }
    return this.nodes;
  }
  byteToGB(capacity: number) {
    return (capacity / 1024 / 1024 / 1024).toFixed(0);
  }
}
</script>