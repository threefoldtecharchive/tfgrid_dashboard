<template>
  <v-data-table
    :headers="headers"
    :items="nodes"
    :single-expand="singleExpand"
    :expanded.sync="expanded"
    item-key="nodeID"
    show-expand
    class="elevation-1"
    dark
    sort-by="nodeID"
  >
    <template v-slot:top>
      <v-toolbar flat>
        <v-toolbar-title>Your Nodes</v-toolbar-title>
      </v-toolbar>
    </template>
    <template v-slot:[`item.status`]="{ item }">
      <p class="text-left mt-1 mb-0">
        <v-chip
          :color="getStatus(item).color"
          dark
        >{{ getStatus(item).status }}</v-chip>
      </p>
    </template>
    <template v-slot:[`item.actions`]="{ item }">
      <v-progress-circular
        v-if="loadingDelete"
        indeterminate
        color="primary"
      ></v-progress-circular>
      <v-tooltip
        bottom
        v-else
      >
        <template v-slot:activator="{ on, attrs }">
          <v-icon
            medium
            @click="deleteItem(item)"
            v-on="on"
            v-bind="attrs"
          >
            mdi-delete
          </v-icon>
        </template>
        <span>Delete a node</span>
      </v-tooltip>

      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-icon
            class="configIcon"
            medium
            v-on="on"
            v-bind="attrs"
          >
            mdi-earth
          </v-icon>
        </template>
        <span>Add a public config</span>
      </v-tooltip>
    </template>
  </v-data-table>
</template>
<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import moment from "moment";

@Component({
  name: "FarmNodesTable",
})
export default class FarmNodesTable extends Vue {
  expanded = [];
  singleExpand = true;

  headers = [
    { text: "Node ID", value: "nodeID" },
    { text: "Farm ID", value: "farmID" },
    { text: "Country", value: "country" },
    { text: "City", value: "city" },
    { text: "Status", value: "status" },
    { text: "Actions", value: "actions", sortable: false },
  ];
  loadingDelete = false;
  dialogDelete = false;
  editedIndex = -1;
  editedItem: any;
  @Prop({ required: true }) nodes!: any;

  getStatus(node: { updatedAt: any }) {
    const { updatedAt } = node;
    const startTime = moment();
    const end = moment(new Date(parseInt(updatedAt)));
    const hours = startTime.diff(end, "hours");

    if (hours < 2) return { color: "green", status: "up" };
    else if (hours > 2 && hours < 3) {
      return { color: "orange", status: "likely down" };
    } else return { color: "red", status: "down" };
  }
  deleteItem(item: any) {
    this.editedIndex = this.nodes.indexOf(item);
    this.editedItem = Object.assign({}, item);
    this.dialogDelete = true;
  }
}
</script>