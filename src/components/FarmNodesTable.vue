<template>
  <v-container>
    <v-text-field
      v-model="searchTerm"
      color="primary darken-2"
      label="Search by node ID, serial number, certification type, farming policy ID"
    ></v-text-field>
    <v-data-table
      :headers="headers"
      :items="filteredNodes()"
      :single-expand="singleExpand"
      :expanded.sync="expanded"
      item-key="nodeID"
      show-expand
      class="elevation-1"
      sort-by="nodeID"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Your Farm Nodes</v-toolbar-title>
        </v-toolbar>
      </template>
      <template v-slot:[`item.status`]="{ item }">
        <p class="text-left mt-1 mb-0">
          <v-chip :color="getStatus(item).color">{{
            getStatus(item).status
          }}</v-chip>
        </p>
      </template>
      <template v-slot:[`item.actions`]="{ item }">
        <v-progress-circular
          v-if="loadingDelete"
          indeterminate
          color="primary"
        ></v-progress-circular>
        <!--delete node-->
        <v-tooltip bottom v-else>
          <template v-slot:activator="{ on, attrs }">
            <v-icon
              medium
              @click="openDelete(item)"
              v-on="on"
              v-bind="attrs"
              :loading="loadingDelete"
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
              @click="openPublicConfig(item)"
            >
              mdi-earth
            </v-icon>
          </template>
          <span>Add a public config</span>
        </v-tooltip>
      </template>
      <!--expanded node view-->
      <template v-slot:expanded-item="{ headers, item }">
        <td :colspan="headers.length" key="item.nodeID">
          <v-col>
            <v-container fluid>
              <v-row>
                <v-flex xs3 class="text-left pr-2">Node ID</v-flex>
                <v-flex class="text-truncate font-weight-bold">
                  <span>{{ item.nodeID }}</span>
                </v-flex>
              </v-row>
              <v-row>
                <v-flex xs3 class="text-left pr-2">Farm ID</v-flex>
                <v-flex class="text-truncate font-weight-bold">
                  <span>{{ item.farmID }}</span>
                </v-flex>
              </v-row>
              <v-row>
                <v-flex xs3 class="text-left pr-2">Twin ID</v-flex>
                <v-flex class="text-truncate font-weight-bold">
                  <span>{{ item.twinID }}</span>
                </v-flex>
              </v-row>
              <v-row>
                <v-flex xs3 class="text-left pr-2">Certification Type</v-flex>
                <v-flex class="text-truncate font-weight-bold">
                  <span>{{ item.certificationType }}</span>
                </v-flex>
              </v-row>
              <v-row>
                <v-flex xs3 class="text-left pr-2">First boot at</v-flex>
                <v-flex class="text-truncate font-weight-bold">
                  <span>{{ new Date(parseInt(item.createdAt)) }}</span>
                </v-flex>
              </v-row>
              <v-row>
                <v-flex xs3 class="text-left pr-2">Uptime</v-flex>
                <v-flex class="text-truncate font-weight-bold">
                  <span>{{ item.uptime }}</span>
                </v-flex>
              </v-row>
              <v-row>
                <v-flex xs3 class="text-left pr-2">Updated at</v-flex>
                <v-flex class="text-truncate font-weight-bold">
                  <span>{{ new Date(parseInt(item.updatedAt)) }}</span>
                </v-flex>
              </v-row>
              <v-row>
                <v-flex xs3 class="text-left pr-2">Country</v-flex>
                <v-flex class="text-truncate font-weight-bold">
                  <span>{{ item.country }}</span>
                </v-flex>
              </v-row>
              <v-row>
                <v-flex xs3 class="text-left pr-2">City</v-flex>
                <v-flex class="text-truncate font-weight-bold">
                  <span>{{ item.city }}</span>
                </v-flex>
              </v-row>
              <v-row>
                <v-flex xs3 class="text-left pr-2">Serial Number</v-flex>
                <v-flex class="text-truncate font-weight-bold">
                  <span>{{ item.serialNumber }}</span>
                </v-flex>
              </v-row>
              <v-row>
                <v-flex xs3 class="text-left pr-2">Farming Policy ID</v-flex>
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
              <v-icon small left>fa-chart-pie</v-icon>Resource units reserved
            </div>

            <v-row>
              <v-col
                v-for="(value, key) in item.resourcesTotal"
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
                          {{ byteToGB(item.resourcesUsed[key]) }} /
                          {{ byteToGB(item.resourcesTotal[key]) }} GB
                        </span>
                        <span v-else>
                          {{ item.resourcesUsed[key] }} /
                          {{ item.resourcesTotal[key] }}
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
    <!--public config dialog-->
    <v-dialog v-model="openPublicConfigDialog" width="800">
      <v-card>
        <v-card-title class="text-h5">
          Add a public config to your node with ID: {{ nodeToEdit.nodeID }}
        </v-card-title>

        <v-card-text class="text">
          <v-text-field
            label="IPV4"
            v-model="ip4"
            required
            outlined
            dense
            hint="IPV4 address in CIDR format xx.xx.xx.xx/xx"
            persistent-hint
            :error-messages="ip4ErrorMessage"
            :validate-on-blur="true"
            :rules="[() => !!ip4 || 'This field is required', ip4check]"
          ></v-text-field>

          <v-text-field
            label="Gateway"
            v-model="gw4"
            required
            outlined
            dense
            hint="Gateway for the IP in ipv4 format"
            persistent-hint
            :validate-on-blur="true"
            :error-messages="gw4ErrorMessage"
            :rules="[() => !!gw4 || 'This field is required', gw4Check]"
          ></v-text-field>

          <v-divider></v-divider>

          <v-text-field
            label="IPV6"
            v-model="ip6"
            outlined
            dense
            hint="IPV6 address (not required)"
            persistent-hint
            :validate-on-blur="true"
            :error-messages="ip6ErrorMessage"
            :rules="[ip6check]"
          ></v-text-field>

          <v-text-field
            label="Gateway IPV6"
            v-model="gw6"
            outlined
            dense
            hint="Gateway for the IP in ipv6 format (not required)"
            persistent-hint
            :validate-on-blur="true"
            :error-messages="gw6ErrorMessage"
            :rules="[gw6Check]"
          ></v-text-field>

          <v-text-field
            label="Domain"
            v-model="domain"
            outlined
            dense
            hint="Domain for webgateway (not required)"
            persistent-hint
            :validate-on-blur="true"
            :error-messages="domainErrorMessage"
            :rules="[domainCheck]"
          ></v-text-field>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-btn text color="error" @click="removeConfig()">
            Remove config
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn text @click="openPublicConfigDialog = false"> Cancel </v-btn>
          <v-btn
            text
            color="primary"
            :loading="loadingPublicConfig"
            @click="saveConfig()"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- delete item dialog-->
    <v-dialog v-model="openDeleteDialog" max-width="700px">
      <v-card>
        <v-card-title class="text-h5"
          >Are you certain you want to delete this node from your
          farm?</v-card-title
        >
        <v-card-text
          >This will delete the node on chain, this action is
          irreversible</v-card-text
        >
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="openDeleteDialog = false"
            >Cancel</v-btn
          >
          <v-btn color="blue darken-1" text @click="deleteItem()">OK</v-btn>
          <v-spacer></v-spacer>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>
<script lang="ts">
import { Component, Vue, Prop, Emit } from "vue-property-decorator";
import moment from "moment";
import { byteToGB } from "@/portal/lib/nodes";
import { addNodePublicConfig, deleteNode } from "@/portal/lib/farms";

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
    { text: "Serial Number", value: "serialNumber" },
    { text: "Status", value: "status" },
    { text: "Actions", value: "actions", sortable: false },
  ];
  loadingDelete = false;
  openDeleteDialog = false;
  editedIndex = -1;
  editedItem: any;
  nodeToEdit: any = {};
  nodeToDelete: any = {};
  openPublicConfigDialog = false;
  @Prop({ required: true }) nodes!: any;
  searchTerm = "";
  ip4 = "";
  gw4 = "";
  ip6 = "";
  gw6 = "";
  domain = "";
  ip4ErrorMessage = "";
  gw4ErrorMessage = "";
  ip6ErrorMessage = "";
  gw6ErrorMessage = "";
  domainErrorMessage = "";
  loadingPublicConfig = false;
  $api: any;
  public filteredNodes() {
    if (this.searchTerm.length !== 0) {
      return this.nodes.filter(
        (node: {
          nodeID: any;
          serialNumber: string;
          certificationType: string;
          farmingPolicyId: number;
        }) =>
          `${node.nodeID}`.includes(this.searchTerm) ||
          node.serialNumber
            .toLowerCase()
            .includes(this.searchTerm.toLowerCase()) ||
          node.certificationType
            .toLowerCase()
            .includes(this.searchTerm.toLowerCase()) ||
          `${node.farmingPolicyId}`.includes(this.searchTerm)
      );
    }
    return this.nodes;
  }
  byteToGB(capacity: number) {
    return byteToGB(capacity);
  }
  saveConfig() {
    const config = {
      ipv4: this.ip4,
      gw4: this.gw4,
      ipv6: this.ip6,
      gw6: this.gw6,
      domain: this.domain,
    };
    this.save(config);
  }
  save(config: {
    ipv4: string;
    gw4: string;
    ipv6: string;
    gw6: string;
    domain: string;
  }) {
    this.loadingPublicConfig = true;
    console.log(this.nodeToEdit.nodeId);
    console.log(this.nodeToEdit.farmId);
    addNodePublicConfig(
      this.$route.params.accountID,
      this.$store.state.api,
      this.nodeToEdit.farmId,
      this.nodeToEdit.nodeId,
      config,
      (res: { events?: never[] | undefined; status: any }) => {
        console.log(res);
        if (res instanceof Error) {
          console.log(res);
          return;
        }

        const { events = [], status } = res;
        console.log(`Current status is ${status.type}`);
        switch (status.type) {
          case "Ready":
            this.$toasted.show(`Transaction submitted`);
        }

        if (status.isFinalized) {
          console.log(
            `Transaction included at blockHash ${status.asFinalized}`
          );

          // Loop through Vec<EventRecord> to display all events
          events.forEach(({ phase, event: { data, method, section } }) => {
            console.log(`\t' ${phase}: ${section}.${method}:: ${data}`);
            if (
              section === "tfgridModule" &&
              method === "NodePublicConfigStored"
            ) {
              this.$toasted.show("Node public config added!");
              this.loadingPublicConfig = false;
              this.openPublicConfigDialog = false;
            } else if (section === "system" && method === "ExtrinsicFailed") {
              this.$toasted.show("Adding Node public config failed");
              this.loadingPublicConfig = false;
            }
          });
        }
      }
    ).catch((err: { message: any }) => {
      console.log(err.message);
      this.loadingPublicConfig = false;
    });
  }
  removeConfig() {
    this.ip4 = "";
    this.gw4 = "";
    this.ip6 = "";
    this.gw6 = "";
    this.domain = "";
    const config = {
      ipv4: "",
      ipv6: "",
      gw4: "",
      gw6: "",
      domain: "",
    };
    this.save(config);
  }
  openPublicConfig(node: any) {
    this.nodeToEdit = node;
    console.log(this.nodeToEdit);
    if (this.nodeToEdit.publicConfig) {
      this.ip4 = this.nodeToEdit.publicConfig.ipv4;
      this.gw4 = this.nodeToEdit.publicConfig.gw4;
      this.ip6 = this.nodeToEdit.publicConfig.ipv6;
      this.gw6 = this.nodeToEdit.publicConfig.gw6;
      this.domain = this.nodeToEdit.publicConfig.domain;
    }

    this.openPublicConfigDialog = true;
  }
  openDelete(node: any) {
    this.nodeToDelete = node;
    this.openDeleteDialog = true;
  }
  ip4check() {
    if (this.ip4 === "") return true;

    const ipRegex = new RegExp(
      "^([0-9]{1,3}.){3}[0-9]{1,3}(/([0-9]|[1-2][0-9]|3[0-2]))$"
    );
    if (ipRegex.test(this.ip4)) {
      this.ip4ErrorMessage = "";
      return true;
    } else {
      this.ip4ErrorMessage = "IP address is not formatted correctly";
      return false;
    }
  }
  ip6check() {
    if (this.ip6 === "") return true;
    /* eslint-disable */
    const ipRegex = new RegExp(
      "(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]).){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]).){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"
    );
    if (ipRegex.test(this.ip6)) {
      this.ip6ErrorMessage = "";
      return true;
    } else {
      this.ip6ErrorMessage = "IPV6 address is not formatted correctly";
      return false;
    }
  }
  gw4Check() {
    if (this.gw4 === "") return true;

    const gatewayRegex = new RegExp("^(?:[0-9]{1,3}.){3}[0-9]{1,3}$");
    if (gatewayRegex.test(this.gw4)) {
      this.gw4ErrorMessage = "";
      return true;
    } else {
      this.gw4ErrorMessage = "Gateway is not formatted correctly";
      return false;
    }
  }
  gw6Check() {
    if (this.gw6 === "") return true;

    const gatewayRegex = new RegExp(
      "(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]).){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]).){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))[0-9]{1,3}$"
    );
    if (gatewayRegex.test(this.gw6)) {
      this.gw6ErrorMessage = "";
      return true;
    } else {
      this.gw6ErrorMessage = "Gateway is not formatted correctly";
      return false;
    }
  }
  domainCheck() {
    if (this.domain === "") return true;
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
  get getFarmNodes() {
    return this.nodes;
  }

  deleteItem() {
    this.loadingDelete = true;
    this.openDeleteDialog = false;
    deleteNode(
      this.$route.params.accountID,
      this.$api,
      this.nodeToDelete.nodeID,
      (res: { events?: never[] | undefined; status: any }) => {
        console.log(res);
        if (res instanceof Error) {
          console.log(res);
          return;
        }

        const { events = [], status } = res;
        console.log(`Current status is ${status.type}`);
        switch (status.type) {
          case "Ready":
            this.$toasted.show(`Transaction submitted`);
        }

        if (status.isFinalized) {
          console.log(
            `Transaction included at blockHash ${status.asFinalized}`
          );

          // Loop through Vec<EventRecord> to display all events
          events.forEach(({ phase, event: { data, method, section } }) => {
            console.log(`\t' ${phase}: ${section}.${method}:: ${data}`);
            if (section === "tfgridModule" && method === "NodeDeleted") {
              this.$toasted.show("Node deleted!");
              this.loadingDelete = false;
              this.openDeleteDialog = false;
              this.$emit("on:delete", this.nodeToDelete.nodeID);
            } else if (section === "system" && method === "ExtrinsicFailed") {
              this.$toasted.show("Deleting a node failed");
              this.loadingDelete = false;
            }
          });
        }
      }
    ).catch((err: { message: any }) => {
      console.log(err.message);
      this.loadingDelete = false;
    });
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