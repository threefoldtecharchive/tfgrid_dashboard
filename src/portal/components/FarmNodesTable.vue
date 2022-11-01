<template>
  <div>

    <div v-if="nodes.length">
      <v-text-field
        v-model="searchTerm"
        color="primary darken-2"
        label="Search by node ID, serial number, certification, farming policy ID"
      ></v-text-field>
      <v-data-table
        :headers="headers"
        :items="filteredNodes()"
        :single-expand="true"
        :expanded.sync="expanded"
        item-key="id"
        show-expand
        class="elevation-1"
        sort-by="id"
      >
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Your Farm Nodes</v-toolbar-title>
            <v-btn
              v-if="network == 'main'"
              class="ml-auto"
              @click="downloadAllReceipts()"
            >Download Receipts</v-btn>

          </v-toolbar>
        </template>

        <template v-slot:[`item.nodeId`]="{ item }">
          <p class="text-center mt-1 mb-0">
            {{ item.nodeId }}
          </p>
        </template>
        <template v-slot:[`item.status`]="{ item }">
          <p class="text-center mt-1 mb-0">
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
          <!--removed until fixed -->
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
          <td
            :colspan="headers.length"
            key="item.id"
          >

            <v-container fluid>
              <v-row :justify="'space-around'">
                <v-col cols="8">
                  <v-row>
                    <v-flex
                      xs3
                      class="text-left pr-2"
                    >Node ID</v-flex>
                    <v-flex class="text-truncate font-weight-bold">
                      <span>{{ item.nodeID}}</span>
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
                    >Certification </v-flex>

                    <v-flex class="text-truncate font-weight-bold">
                      <span>{{ item.certification }}</span>
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
                    >Serial Number</v-flex>
                    <v-flex class="text-truncate font-weight-bold">
                      <span>{{ item.serialNumber }}</span>
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
                </v-col>
                <v-col
                  v-if="network == 'main' "
                  cols="4"
                  class="text-center"
                  :align-self="'center'"
                >

                  <v-flex class="text-truncate font-weight-bold">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on }">
                        <v-progress-circular
                          v-on="on"
                          :rotate="-90"
                          :size="100"
                          :width="15"
                          :value="getNodeUptimePercentage(item)"
                          color="light-green darken-2"
                        />

                        <span>
                          Uptime: {{getNodeUptimePercentage(item) }} %

                        </span>
                      </template>
                      <span>Current Node Uptime Percentage
                        (since start of the month)</span>

                    </v-tooltip>
                  </v-flex>

                </v-col>
              </v-row>
            </v-container>

            <v-col>
              <v-expansion-panels
                v-model="resourcesPanel"
                :disabled="false"
                focusable
              >
                <v-expansion-panel>
                  <v-expansion-panel-header>
                    Resource units reserved
                  </v-expansion-panel-header>
                  <v-expansion-panel-content>
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
                                <span v-if="item.resourcesTotal[key] > 1000">
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
                  </v-expansion-panel-content>
                </v-expansion-panel>
              </v-expansion-panels>

            </v-col>
            <v-col v-if="network == 'main'">
              <v-expansion-panels
                v-model="receiptsPanel"
                :disabled="false"
                focusable
                single
              >
                <v-expansion-panel>
                  <v-expansion-panel-header>
                    Node Statistics
                  </v-expansion-panel-header>
                  <v-expansion-panel-content>

                    <ReceiptsCalendar :node="item" />

                  </v-expansion-panel-content>
                </v-expansion-panel>

              </v-expansion-panels>
            </v-col>
          </td>
        </template>
      </v-data-table>
      <!--public config dialog-->
      <v-dialog
        v-model="openPublicConfigDialog"
        width="800"
      >
        <v-card>
          <v-card-title class="text-h5">
            Add a public config to your node with ID: {{ nodeToEdit.id }}
          </v-card-title>

          <v-card-text class="text">
            <v-form v-model="isValidPublicConfig">
              <v-text-field
                label="IPV4"
                v-model="ip4"
                required
                outlined
                dense
                type="string"
                hint="IPV4 address in CIDR format xx.xx.xx.xx/xx"
                persistent-hint
                :error-messages="ip4ErrorMessage"
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
                type="string"
                :error-messages="gw4ErrorMessage"
                :rules="[() => !!gw4 || 'This field is required', gw4Check]"
              ></v-text-field>

              <v-divider></v-divider>

              <v-text-field
                label="IPV6"
                v-model="ip6"
                type="string"
                outlined
                dense
                hint="IPV6 address in CIDR format x:x:x:x"
                persistent-hint
                :error-messages="ip6ErrorMessage"
                :rules="[ip6check]"
              ></v-text-field>

              <v-text-field
                label="Gateway IPV6"
                v-model="gw6"
                outlined
                dense
                type="string"
                hint="Gateway for the IP in ipv6 format "
                persistent-hint
                :error-messages="gw6ErrorMessage"
                :rules="[gw6Check]"
              ></v-text-field>

              <v-text-field
                label="Domain"
                v-model="domain"
                outlined
                dense
                type="string"
                hint="Domain for webgateway"
                persistent-hint
                :error-messages="domainErrorMessage"
                :rules="[domainCheck]"
              ></v-text-field>
            </v-form>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-actions>
            <v-btn
              text
              color="error"
              @click="openRemoveConfigWarningDialog = true;"
            >
              Remove config
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn
              color="grey lighten-2 black--text"
              @click="openPublicConfigDialog = false"
            >
              Cancel
            </v-btn>
            <v-btn
              color="primary white--text"
              @click=" openWarningDialog = true;"
              :disabled="!isValidPublicConfig"
            >
              Save
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <!-- delete item dialog-->
      <v-dialog
        v-model="openDeleteDialog"
        max-width="700px"
      >
        <v-card>
          <v-card-title class="text-h5">Are you certain you want to delete this node from your
            farm?</v-card-title>
          <v-card-text>This will delete the node on chain, this action is
            irreversible</v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="grey lighten-2 black--text"
              @click="openDeleteDialog = false"
            >Cancel</v-btn>
            <v-btn
              color="primary white--text"
              @click="deleteItem()"
            >OK</v-btn>
            <v-spacer></v-spacer>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-dialog
        v-model="openWarningDialog"
        max-width="700"
      >
        <v-card>
          <v-card-title class="text-h5">Are you certain you want to update this node's public config?</v-card-title>
          <v-card-text> This action is
            irreversible</v-card-text>
          <v-card-actions>
            <v-btn
              @click="saveConfig()"
              :loading="loadingPublicConfig"
            >Submit</v-btn>
            <v-btn @click="openWarningDialog = false">Cancel</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-dialog
        v-model="openRemoveConfigWarningDialog"
        max-width="700"
      >
        <v-card>
          <v-card-title class="text-h5">Are you certain you want to remove this node's public config?</v-card-title>
          <v-card-text> This action is
            irreversible</v-card-text>
          <v-card-actions>
            <v-btn
              @click="removeConfig()"
              :loading="loadingPublicConfig"
            >Submit</v-btn>
            <v-btn @click="openRemoveConfigWarningDialog = false">Cancel</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
    <div v-if="loadingNodes">
      <v-data-table
        loading
        loading-text="loading nodes.."
      ></v-data-table>
    </div>
  </div>
</template>
<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import moment from "moment";
import {
  byteToGB,
  generateNodeSummary,
  generateReceipt,
  getNodeUptimePercentage,
} from "@/portal/lib/nodes";
import {
  addNodePublicConfig,
  deleteNode,
  nodeInterface,
} from "@/portal/lib/farms";
import { hex2a } from "@/portal/lib/util";
import ReceiptsCalendar from "./ReceiptsCalendar.vue";
import jsPDF from "jspdf";
import config from "@/portal/config";

@Component({
  name: "FarmNodesTable",
  components: { ReceiptsCalendar },
})
export default class FarmNodesTable extends Vue {
  expanded: any = [];
  receiptsPanel = [];
  resourcesPanel = [];
  network = config.network;

  headers = [
    { text: "Node ID", value: "nodeID", align: "center" },
    { text: "Farm ID", value: "farmID", align: "center" },
    { text: "Country", value: "country", align: "center" },
    { text: "Serial Number", value: "serialNumber", align: "center" },
    { text: "Status", value: "status", align: "center" },
    { text: "Actions", value: "actions", sortable: false, align: "center" },
  ];

  loadingDelete = false;
  openDeleteDialog = false;
  editedIndex = -1;
  editedItem: any;
  nodeToEdit: nodeInterface = {
    resourcesTotal: {
      cru: "",
      hru: "",
      mru: "",
      sru: "",
    },
    publicConfig: {
      domain: "",
      gw4: "",
      gw6: "",
      ipv4: "",
      ipv6: "",
    },
    receipts: [],
    certification: "",
    city: "",
    connectionPrice: null,
    country: "",
    created: 0,
    createdAt: "",
    farmID: 0,
    farmingPolicyId: 0,
    gridVersion: 0,
    id: "",
    location: {
      latitude: "",
      longitude: "",
    },
    nodeID: 0,
    secure: false,
    serialNumber: "",
    twinID: 0,
    updatedAt: "",
    uptime: 0,
    downtime: 0,
    virtualized: false,
  };
  nodeToDelete: { id: string } = {
    id: "",
  };
  openPublicConfigDialog = false;
  @Prop({ required: true }) nodes!: nodeInterface[];
  @Prop({ required: true }) loadingNodes!: boolean;
  searchTerm = "";
  ip4 = "";
  gw4 = "";
  ip6 = "";
  gw6 = "";
  domain = "";
  loadingPublicConfig = false;
  $api: any;
  isValidPublicConfig = false;
  openWarningDialog = false;
  openRemoveConfigWarningDialog = false;
  ip4ErrorMessage = "";
  gw4ErrorMessage = "";
  ip6ErrorMessage = "";
  gw6ErrorMessage = "";
  domainErrorMessage = "";
  receipts = [];
  updated() {
    this.receiptsPanel = [];
  }
  filteredNodes() {
    let nodes = this.nodes;
    if (this.nodes.length > 0) {
      nodes = this.nodes.filter(
        (node: nodeInterface) =>
          `${node.nodeID}`.includes(this.searchTerm) ||
          node.serialNumber
            ?.toLowerCase()
            .includes(this.searchTerm.toLowerCase()) ||
          node.certification
            ?.toLowerCase()
            .includes(this.searchTerm.toLowerCase()) ||
          `${node.farmingPolicyId}`.includes(this.searchTerm)
      );
    }
    return nodes.map((node) => {
      return { ...node, status: node.updatedAt };
    });
  }
  downloadAllReceipts() {
    let docSum = new jsPDF();
    generateNodeSummary(docSum, this.nodes);
    docSum.addPage();

    this.nodes.map((node, i) => {
      generateReceipt(docSum, node);
      docSum.text(`${i + 1}`, 185, docSum.internal.pageSize.height - 10);
      docSum.addPage();
    });
    docSum.save("nodes_receipts.pdf");
  }
  convertHex(node: { id: string }) {
    return hex2a(node.id);
  }
  byteToGB(capacity: number) {
    return byteToGB(capacity);
  }
  saveConfig() {
    var config: {
      ip4: { ip: string; gw: string };
      ip6?: { ip: string; gw: string };
      domain?: string;
    } = {
      ip4: {
        ip: this.ip4,
        gw: this.gw4,
      },
    };

    if (this.ip6 != "")
      config.ip6 = {
        ip: this.ip6,
        gw: this.gw6,
      };

    if (this.domain != "") config.domain = this.domain;

    this.save(config);
  }
  save(
    config: {
      ip4: { ip: string; gw: string };
      ip6?: { ip: string | undefined; gw: string | undefined };
      domain?: string;
    } | null
  ) {
    this.loadingPublicConfig = true;
    addNodePublicConfig(
      this.$route.params.accountID,
      this.$api,
      this.nodeToEdit.farmID,
      this.nodeToEdit.nodeID,
      config,
      (res: {
        events?: never[] | undefined;
        status: { type: string; asFinalized: string; isFinalized: string };
      }) => {
        console.log(res);
        if (res instanceof Error) {
          console.log(res);
          this.ip4 = "";
          this.ip6 = "";
          this.gw4 = "";
          this.gw6 = "";
          this.domain = "";
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
          if (!events.length) {
            if (this.openWarningDialog)
              this.$toasted.show("Adding Node public config failed");
            else if (this.openRemoveConfigWarningDialog)
              this.$toasted.show("Removing Node public config failed");

            this.loadingPublicConfig = false;
            this.openWarningDialog = false;
            this.openRemoveConfigWarningDialog = false;
          } else {
            // Loop through Vec<EventRecord> to display all events
            events.forEach(({ phase, event: { data, method, section } }) => {
              console.log(`\t' ${phase}: ${section}.${method}:: ${data}`);
              if (
                section === "tfgridModule" &&
                method === "NodePublicConfigStored"
              ) {
                if (this.openWarningDialog)
                  this.$toasted.show("Node public config added!");
                else if (this.openRemoveConfigWarningDialog) {
                  this.$toasted.show("Node public config removed!");
                  this.ip4 = "";
                  this.ip6 = "";
                  this.gw4 = "";
                  this.gw6 = "";
                  this.domain = "";
                }

                this.loadingPublicConfig = false;
                this.openPublicConfigDialog = false;
                this.openWarningDialog = false;
                this.openRemoveConfigWarningDialog = false;
              } else if (section === "system" && method === "ExtrinsicFailed") {
                if (this.openWarningDialog)
                  this.$toasted.show("Adding Node public config failed");
                else if (this.openRemoveConfigWarningDialog)
                  this.$toasted.show("Removing Node public config failed");
                this.loadingPublicConfig = false;
                this.openWarningDialog = false;
                this.openRemoveConfigWarningDialog = false;
              }
            });
          }
        }
      }
    ).catch((err: { message: string }) => {
      console.log(err.message);
      if (this.openWarningDialog)
        this.$toasted.show("Adding Node public config failed");
      else if (this.openRemoveConfigWarningDialog)
        this.$toasted.show("Removing Node public config failed");
      this.loadingPublicConfig = false;
      this.openPublicConfigDialog = false;
      this.openWarningDialog = false;
      this.openRemoveConfigWarningDialog = false;
    });
  }
  removeConfig() {
    this.save(null);
  }
  openPublicConfig(node: nodeInterface) {
    this.nodeToEdit = node;
    if (this.nodeToEdit.publicConfig) {
      this.ip4 = this.nodeToEdit.publicConfig.ipv4;
      this.gw4 = this.nodeToEdit.publicConfig.gw4;
      this.ip6 = this.nodeToEdit.publicConfig.ipv6;
      this.gw6 = this.nodeToEdit.publicConfig.gw6;
      this.domain = this.nodeToEdit.publicConfig.domain;
    }
    this.openPublicConfigDialog = true;
  }
  openDelete(node: { id: string }) {
    this.nodeToDelete = node;
    this.openDeleteDialog = true;
  }
  ip4check() {
    if (this.ip4 === "") return true;
    const IPv4SegmentFormat =
      "(?:[0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])";
    const IPv4AddressFormat = `(${IPv4SegmentFormat}[.]){3}${IPv4SegmentFormat}`;
    const ipRegex = new RegExp(`^${IPv4AddressFormat}/(1[6-9]|2[0-9]|3[0-2])$`);
    if (ipRegex.test(this.ip4)) {
      this.ip4ErrorMessage = "";
      return true;
    } else {
      this.ip4ErrorMessage = "IP address is not formatted correctly";
      return false;
    }
  }
  ip6check() {
    if (!this.ip6) return true;
    const IPv4SegmentFormat =
      "(?:[0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])";
    const IPv4AddressFormat = `(${IPv4SegmentFormat}[.]){3}${IPv4SegmentFormat}`;
    const IPv6SegmentFormat = "(?:[0-9a-fA-F]{1,4})";
    const ipRegex = new RegExp(
      "^(" +
        `(?:${IPv6SegmentFormat}:){7}(?:${IPv6SegmentFormat}|:)|` +
        `(?:${IPv6SegmentFormat}:){6}(?:${IPv4AddressFormat}|:${IPv6SegmentFormat}|:)|` +
        `(?:${IPv6SegmentFormat}:){5}(?::${IPv4AddressFormat}|(:${IPv6SegmentFormat}){1,2}|:)|` +
        `(?:${IPv6SegmentFormat}:){4}(?:(:${IPv6SegmentFormat}){0,1}:${IPv4AddressFormat}|(:${IPv6SegmentFormat}){1,3}|:)|` +
        `(?:${IPv6SegmentFormat}:){3}(?:(:${IPv6SegmentFormat}){0,2}:${IPv4AddressFormat}|(:${IPv6SegmentFormat}){1,4}|:)|` +
        `(?:${IPv6SegmentFormat}:){2}(?:(:${IPv6SegmentFormat}){0,3}:${IPv4AddressFormat}|(:${IPv6SegmentFormat}){1,5}|:)|` +
        `(?:${IPv6SegmentFormat}:){1}(?:(:${IPv6SegmentFormat}){0,4}:${IPv4AddressFormat}|(:${IPv6SegmentFormat}){1,6}|:)|` +
        `(?::((?::${IPv6SegmentFormat}){0,5}:${IPv4AddressFormat}|(?::${IPv6SegmentFormat}){1,7}|:))` +
        ")([0-9a-fA-F]{1})?(/(1[6-9]|([2-5][0-9])|6[0-4]))?$"
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
    const IPv4SegmentFormat =
      "(?:[0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])";
    const IPv4AddressFormat = `(${IPv4SegmentFormat}[.]){3}${IPv4SegmentFormat}`;
    const gatewayRegex = new RegExp(`^${IPv4AddressFormat}$`);
    if (gatewayRegex.test(this.gw4)) {
      this.gw4ErrorMessage = "";
      return true;
    } else {
      this.gw4ErrorMessage = "Gateway is not formatted correctly";
      return false;
    }
  }
  gw6Check() {
    if (!this.gw6) return true;
    const IPv4SegmentFormat =
      "(?:[0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])";
    const IPv4AddressFormat = `(${IPv4SegmentFormat}[.]){3}${IPv4SegmentFormat}`;

    const IPv6SegmentFormat = "(?:[0-9a-fA-F]{1,4})";
    const gatewayRegex = new RegExp(
      "^(" +
        `(?:${IPv6SegmentFormat}:){7}(?:${IPv6SegmentFormat}|:)|` +
        `(?:${IPv6SegmentFormat}:){6}(?:${IPv4AddressFormat}|:${IPv6SegmentFormat}|:)|` +
        `(?:${IPv6SegmentFormat}:){5}(?::${IPv4AddressFormat}|(:${IPv6SegmentFormat}){1,2}|:)|` +
        `(?:${IPv6SegmentFormat}:){4}(?:(:${IPv6SegmentFormat}){0,1}:${IPv4AddressFormat}|(:${IPv6SegmentFormat}){1,3}|:)|` +
        `(?:${IPv6SegmentFormat}:){3}(?:(:${IPv6SegmentFormat}){0,2}:${IPv4AddressFormat}|(:${IPv6SegmentFormat}){1,4}|:)|` +
        `(?:${IPv6SegmentFormat}:){2}(?:(:${IPv6SegmentFormat}){0,3}:${IPv4AddressFormat}|(:${IPv6SegmentFormat}){1,5}|:)|` +
        `(?:${IPv6SegmentFormat}:){1}(?:(:${IPv6SegmentFormat}){0,4}:${IPv4AddressFormat}|(:${IPv6SegmentFormat}){1,6}|:)|` +
        `(?::((?::${IPv6SegmentFormat}){0,5}:${IPv4AddressFormat}|(?::${IPv6SegmentFormat}){1,7}|:))` +
        ")([0-9a-fA-F]{1})?$"
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
    return true;
  }
  getTime(num: number | undefined) {
    if (num) {
      return new Date(num);
    }
    return new Date();
  }

  getNodeUptimePercentage(node: nodeInterface) {
    return getNodeUptimePercentage(node);
  }
  getStatus(node: { updatedAt: string }) {
    const { updatedAt } = node;
    const startTime = moment();
    const end = moment(new Date(parseInt(updatedAt)));
    const hours = startTime.diff(end, "hours");
    if (hours < 2) return { color: "green", status: "up" };
    else if (hours > 2 && hours < 3) {
      return { color: "orange", status: "likely down" };
    } else return { color: "red", status: "down" };
  }

  deleteItem() {
    this.loadingDelete = true;
    this.openDeleteDialog = false;
    deleteNode(
      this.$route.params.accountID,
      this.$api,
      parseInt(this.nodeToDelete.id.split("-")[1]),
      (res: {
        events?: never[] | undefined;
        status: { type: string; asFinalized: string; isFinalized: string };
      }) => {
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
              this.$emit("on:delete", this.nodeToDelete.id);
            } else if (section === "system" && method === "ExtrinsicFailed") {
              this.$toasted.show("Deleting a node failed");
              this.loadingDelete = false;
            }
          });
        }
      }
    ).catch((err: { message: string }) => {
      console.log(err.message);
      this.$toasted.show("Deleting a node failed");
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