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
      <!--delete node-->
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
      <!--config Ips-->
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
    <!--expanded node view-->
    <template v-slot:expanded-item="{ headers, item }">
      <td
        :colspan="headers.length"
        key="item.nodeID"
      >
        <v-col>
          <v-container fluid>
            <v-row>
              <v-flex
                xs3
                class="text-left pr-2"
              >Node ID</v-flex>
              <v-flex class="text-truncate font-weight-bold">
                <span>{{ item.nodeID }}</span>
              </v-flex>
            </v-row>
            <v-row>
              <v-flex
                xs3
                class="text-left pr-2"
              >Farm ID</v-flex>
              <v-flex class="text-truncate font-weight-bold">
                <span>{{ item.farmID }}</span>
              </v-flex>
            </v-row>
            <v-row>
              <v-flex
                xs3
                class="text-left pr-2"
              >Twin ID</v-flex>
              <v-flex class="text-truncate font-weight-bold">
                <span>{{ item.twinID }}</span>
              </v-flex>
            </v-row>
            <v-row>
              <v-flex
                xs3
                class="text-left pr-2"
              >Certification Type</v-flex>
              <v-flex class="text-truncate font-weight-bold">
                <span>{{ item.certificationType }}</span>
              </v-flex>
            </v-row>
            <v-row>
              <v-flex
                xs3
                class="text-left pr-2"
              >First boot at</v-flex>
              <v-flex class="text-truncate font-weight-bold">
                <span>{{ new Date(parseInt(item.createdAt)) }}</span>
              </v-flex>
            </v-row>
            <v-row>
              <v-flex
                xs3
                class="text-left pr-2"
              >Uptime</v-flex>
              <v-flex class="text-truncate font-weight-bold">
                <span>{{ item.uptime  }}</span>
              </v-flex>
            </v-row>
            <v-row>
              <v-flex
                xs3
                class="text-left pr-2"
              >Updated at</v-flex>
              <v-flex class="text-truncate font-weight-bold">
                <span>{{ new Date(parseInt(item.updatedAt)) }}</span>
              </v-flex>
            </v-row>
            <v-row>
              <v-flex
                xs3
                class="text-left pr-2"
              >Country</v-flex>
              <v-flex class="text-truncate font-weight-bold">
                <span>{{ item.country }}</span>
              </v-flex>
            </v-row>
            <v-row>
              <v-flex
                xs3
                class="text-left pr-2"
              >City</v-flex>
              <v-flex class="text-truncate font-weight-bold">
                <span>{{ item.city }}</span>
              </v-flex>
            </v-row>
            <v-row>
              <v-flex
                xs3
                class="text-left pr-2"
              >Farming Policy ID</v-flex>
              <v-flex class="text-truncate font-weight-bold">
                <span>{{ item.farmingPolicyId }}</span>
              </v-flex>
            </v-row>

            <v-row>
              <span>For more information visit the Capacity Explorer</span>
            </v-row>
          </v-container>
        </v-col>

        <v-col>
          <div class="title">
            <v-icon
              small
              left
            >fa-chart-pie</v-icon>Resource units reserved
          </div>

          <v-row>
            <v-col
              v-for="( value, key) in item.resourcesTotal"
              :key="key"
              align="center"
            >
              <v-flex class="text-center pr-2">
                <span class="text-uppercase">{{ key }}</span>
              </v-flex>
              <v-flex class="text-truncate font-weight-bold">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on }">
                    <v-progress-circular
                      v-on="on"
                      :rotate="-90"
                      :size="100"
                      :width="15"
                      :value="getPercentage(key)"
                      color="light-green darken-2"
                    />
                    <template v-if="item.resourcesUsed">

                      <span v-if="item.resourcesTotal[key] >> 1000">
                        {{ byteToGB( item.resourcesUsed[key] )}} / {{ byteToGB(item.resourcesTotal[key])  }} GB
                      </span>
                      <span v-else>
                        {{ item.resourcesUsed[key] }} / {{ item.resourcesTotal[key]  }}
                      </span>

                    </template>

                  </template>

                </v-tooltip>
              </v-flex>
            </v-col>
          </v-row>
        </v-col>

      </td>
    </template>
  </v-data-table>
</template>
<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import moment from "moment";
import { byteToGB } from "@/portal/lib/nodes";

@Component({
  name: "FarmNodesTable",
})
export default class FarmNodesTable extends Vue {
  expanded: any = [];
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
  byteToGB(capacity: number) {
    return byteToGB(capacity);
  }
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
  getPercentage(type: any) {
    if (!this.expanded[0].resourcesUsed) return 0;
    const reservedResources = this.expanded[0].resourcesUsed[type];
    const totalResources = this.expanded[0].resourcesTotal[type];
    if (reservedResources === 0 && totalResources === 0) return 0;
    return (reservedResources / totalResources) * 100;
  }
}
</script>