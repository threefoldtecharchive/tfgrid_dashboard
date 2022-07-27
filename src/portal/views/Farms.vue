<template>
  <v-container fluid>

    <v-card
      color="primary"
      class="white--text my-3 pa-3 text-center d-flex justify-center align-baseline"
    >
      <h3>Don't have any farms? Start by creating one:</h3>

      <v-btn
        @click="openCreateFarmDialog = true"
        class="farm my-3 mx-5"
        :loading="loadingCreateFarm"
      >Create farm</v-btn>
    </v-card>
    <v-dialog
      transition="dialog-bottom-transition"
      v-model="openCreateFarmDialog"
      max-width="500"
    >
      <v-card>
        <v-toolbar
          color="primary"
          class="white--text"
        >Create Farm</v-toolbar>
        <v-card-text>
          <v-text-field
            label="Farm Name"
            v-model="farmName"
            required
            :error-messages="farmNameErrorMessage"
            :rules="[
              () => !!farmName || 'This field is required',
              farmNameCheck,
              () =>
                farmName.length < 20 ||
                'Name too long, only 20 characters permitted',
            ]"
          ></v-text-field>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn
            color="primary white--text"
            @click="createFarmFromName"
            :loading="loadingCreateFarm"
          >Submit</v-btn>
          <v-btn
            @click="openCreateFarmDialog = false"
            color="grey lighten-2 black--text"
          >Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-text-field
      v-model="searchTerm"
      color="primary darken-2"
      label="Search by farm name or ID"
    ></v-text-field>
    <v-data-table
      :headers="headers"
      :items="farms.length ? filteredFarms() : []"
      :single-expand="singleExpand"
      :expanded.sync="expanded"
      item-key="name"
      show-expand
      class="elevation-1"
      disable-pagination
    >
      <template v-slot:top>
        <v-toolbar
          flat
          class="primary white--text"
        >
          <v-toolbar-title>Your Farms</v-toolbar-title>
          <v-spacer></v-spacer>
        </v-toolbar>
      </template>
      <template v-slot:[`item.actions`]="{ item }">
        <!--delete node-->
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-icon
              medium
              v-on="on"
              v-bind="attrs"
              @click="openDeleteFarm(item)"
            >
              mdi-delete
            </v-icon>
          </template>
          <span>Delete a farm</span>
        </v-tooltip>
      </template>
      <template v-slot:expanded-item="{ item }">
        <td :colspan="headers.length">
          <v-container
            fluid
            class="text-left"
          >
            <v-row>
              <v-col>
                <v-flex class="text-left pr-2">Farm ID</v-flex>
              </v-col>
              <v-col>
                <v-flex class="text-truncate font-weight-bold">
                  <span>{{ item.id }}</span>
                </v-flex>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-flex class="text-left pr-2">Farm Name</v-flex>
              </v-col>
              <v-col>
                <v-flex class="text-truncate font-weight-bold">
                  <span>{{ item.name }}</span>
                </v-flex>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-flex class="text-left pr-2">Linked Twin ID</v-flex>
              </v-col>
              <v-col>
                <v-flex class="text-truncate font-weight-bold">
                  <span>{{ item.twin_id }}</span>
                </v-flex>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-flex class="text-left pr-2">Certification Type</v-flex>
              </v-col>
              <v-col>
                <v-flex class="text-truncate font-weight-bold">
                  <span>{{ item.certification }}</span>
                </v-flex>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-flex class="text-left">Linked Pricing Policy ID</v-flex>
              </v-col>
              <v-col>
                <v-flex class="text-truncate font-weight-bold">
                  <span>{{ item.pricing_policy_id }}</span>
                </v-flex>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-flex class="text-left">Stellar Payout Address</v-flex>
              </v-col>
              <v-col v-if="item.v2address">
                <v-row
                  class="d-flex align-baseline justify-between"
                  style="
                    text-overflow: ellipsis;
                    white-space: nowrap;
                    overflow: hidden;
                  "
                >
                  <span style="font-size: small">
                    {{ item.v2address }}
                  </span>
                  <v-btn
                    x-small
                    @click="openV2AddressDialog = true"
                  >Edit</v-btn>
                </v-row>
              </v-col>
              <v-col v-else>
                <v-flex>
                  <v-btn
                    x-small
                    @click="openV2AddressDialog = true"
                  >Add V2 Address</v-btn>
                </v-flex>
              </v-col>
              <v-dialog
                transition="dialog-bottom-transition"
                v-model="openV2AddressDialog"
                max-width="500"
              >
                <v-card>
                  <v-toolbar color="primary">Add/Edit V2 Stellar Address</v-toolbar>
                  <v-card-text>
                    <v-text-field
                      v-model="v2_address"
                      label="Stellar Wallet Address"
                    >
                    </v-text-field>
                  </v-card-text>
                  <v-card-actions class="justify-end">
                    <v-btn
                      @click="openV2AddressDialog = false"
                      color="grey lighten-2 black--text"
                    >Close</v-btn>
                    <v-btn
                      @click="addV2Address"
                      color="primary white--text"
                    >Submit</v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-row>
            <v-row>
              <v-col>
                <v-flex class="text-left">Bootstrap Node Image</v-flex>
              </v-col>
              <v-col>
                <v-flex>
                  <v-btn
                    x-small
                    v-bind:href="'https://v3.bootstrap.grid.tf/'"
                    target="blank"
                  >view bootstrap</v-btn>
                </v-flex>
              </v-col>
            </v-row>

            <PublicIPTable
              :ips="item.public_ips"
              :deleteIP="deletePublicIP"
              :loadingDelete="loadingDeleteIP"
              :createIP="createPublicIP"
              :loadingCreate="loadingCreateIP"
            />
          </v-container>
        </td>
      </template>
    </v-data-table>
    <FarmNodesTable
      :nodes="nodes"
      @on:delete="getNodes()"
    />
    <v-dialog
      v-model="openDeleteFarmDialog"
      max-width="700px"
    >
      <v-card>
        <v-card-title class="text-h5">Are you certain you want to delete this farm?</v-card-title>
        <v-card-text>This will delete the farm on the chain, this action is
          irreversible</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="grey lighten-2 black--text"
            text
            @click="openDeleteFarmDialog = false"
          >Cancel</v-btn>
          <v-btn
            color="primary white--text"
            text
            :loading="loadingDeleteFarm"
            @click="callDeleteFarm()"
          >OK</v-btn>
          <v-spacer></v-spacer>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import FarmNodesTable from "../components/FarmNodesTable.vue";
import PublicIPTable from "../components/PublicIPTable.vue";
import { Component, Vue, Watch } from "vue-property-decorator";
import {
  createFarm,
  createIP,
  deleteFarm,
  deleteIP,
  getFarm,
  getNodesByFarmID,
  setFarmPayoutV2Address,
} from "../lib/farms";
@Component({
  name: "FarmsView",
  components: { PublicIPTable, FarmNodesTable },
})
export default class FarmsView extends Vue {
  headers = [
    { text: "Farm ID", value: "id" },
    { text: "Farm name", value: "name" },
    { text: "Linked Twin ID", value: "twin_id" },
    { text: "Certification type", value: "certification" },
    { text: "Pricing Policy ID", value: "pricing_policy_id" },
    { text: "Actions", value: "actions" },
  ];
  farms: any = [];
  id: any = [];
  singleExpand = true;
  expanded: any = [];
  $api: any;
  openV2AddressDialog = false;
  openCreateFarmDialog = false;
  v2_address = "";
  farmName = "";
  address = "";
  farmNameErrorMessage = "";
  loadingCreateIP = false;
  loadingDeleteIP = false;
  nodes: any = [];
  loadingNodes = false;
  loadingNodeDelete = false;
  loadingAddNodePublicConfig = false;
  loadingDeleteFarm = false;
  openDeleteFarmDialog = false;
  farmToDelete: any = {};
  searchTerm = "";
  loadingCreateFarm = false;
  async mounted() {
    this.address = this.$route.params.accountID;
    this.id = this.$route.query.twinID;
    if (this.$api) {
      this.farms = await getFarm(this.$api, this.id);
      this.nodes = this.getNodes();
    } else {
      this.$router.push({
        name: "accounts",
        path: "/",
      });
    }
  }
  @Watch("$route.query.twinID") async onPropertyChanged(
    value: number,
    oldValue: number
  ) {
    console.log(
      `switching from account ${oldValue} farms to account ${value} farms`
    );
    this.farms = await getFarm(this.$api, value);
    this.nodes = this.getNodes();
  }
  @Watch("farms.length") async onFarmCreation(value: number, oldValue: number) {
    console.log(`there were ${oldValue} farms, now there is ${value} farms`);
  }
  @Watch("nodes.length") async onNodeDeleted(value: number, oldValue: number) {
    console.log(`there were ${oldValue} nodes, now there is ${value} nodes`);
  }
  async updated() {
    this.address = this.$route.params.accountID;
    this.id = this.$route.query.twinID;
    if (this.$api) {
      this.farms = await getFarm(this.$api, this.id);
    } else {
      this.$router.push({
        name: "accounts",
        path: "/",
      });
    }
    this.v2_address;
    this.farmName;
  }
  public filteredFarms() {
    if (this.farms.length > 0) {
      return this.farms.filter(
        (farm: { name: string; id: any }) =>
          farm.name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
          `${farm.id}`.includes(this.searchTerm)
      );
    }
    return this.farms;
  }
  async getNodes() {
    this.nodes = await getNodesByFarmID(this.farms);
  }
  openDeleteFarm(farm: any) {
    this.farmToDelete = farm;
    this.openDeleteFarmDialog = true;
  }
  callDeleteFarm() {
    this.loadingDeleteFarm = true;
    deleteFarm(
      this.address,
      this.$api,
      this.farmToDelete.id,
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
          if (!events.length) {
            this.$toasted.show("Deleting a farm failed");
            this.loadingDeleteFarm = false;
          } else {
            // Loop through Vec<EventRecord> to display all events
            events.forEach(({ phase, event: { data, method, section } }) => {
              console.log(`\t' ${phase}: ${section}.${method}:: ${data}`);
              if (section === "tfgridModule" && method === "FarmDeleted") {
                this.$toasted.show("Farm deleted!");
                this.loadingDeleteFarm = false;
                this.openDeleteFarmDialog = false;
                this.farms = getFarm(this.$api, this.id);
              } else if (section === "system" && method === "ExtrinsicFailed") {
                this.$toasted.show("Deleting a farm failed");
                this.loadingDeleteFarm = false;
              }
            });
          }
        }
      }
    ).catch((err: { message: string }) => {
      this.$toasted.show(err.message);
      this.loadingDeleteFarm = false;
    });
  }
  deletePublicIP(publicIP: any) {
    this.loadingDeleteIP = true;
    deleteIP(
      this.$route.params.accountID,
      this.$api,
      this.expanded[0].id,
      publicIP,
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
          if (!events.length) {
            this.$toasted.show("IP deletion failed!");
            this.loadingDeleteIP = false;
          } else {
            // Loop through Vec<EventRecord> to display all events
            events.forEach(({ phase, event: { data, method, section } }) => {
              console.log(`\t' ${phase}: ${section}.${method}:: ${data}`);
              if (section === "tfgridModule" && method === "FarmUpdated") {
                this.$toasted.show("IP deleted!");
                getFarm(this.$api, this.id).then((farms) => {
                  this.farms = farms;
                  this.loadingDeleteIP = false;
                });
              } else if (section === "system" && method === "ExtrinsicFailed") {
                this.$toasted.show("IP deletion failed!");
                this.loadingDeleteIP = false;
              }
            });
          }
        }
      }
    ).catch((err) => {
      this.$toasted.show(err.message);
      this.loadingDeleteIP = false;
    });
  }
  public createPublicIP(publicIP: string, gateway: string) {
    this.loadingCreateIP = true;
    createIP(
      this.$route.params.accountID,
      this.$api,
      this.expanded[0].id,
      publicIP,
      gateway,
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
          if (!events.length) {
            this.$toasted.show("Adding an IP failed!");
          } else {
            // Loop through Vec<EventRecord> to display all events
            events.forEach(({ phase, event: { data, method, section } }) => {
              console.log(`\t' ${phase}: ${section}.${method}:: ${data}`);
              if (section === "tfgridModule" && method === "FarmUpdated") {
                this.$toasted.show("IP created!");
                getFarm(this.$api, this.id).then((farms) => {
                  this.farms = farms;
                  this.loadingCreateIP = false;
                });
              } else if (section === "system" && method === "ExtrinsicFailed") {
                this.$toasted.show("Adding an IP failed!");
              }
            });
          }
        }
      }
    ).catch((err) => {
      this.$toasted.show(err.message);
    });
  }
  public farmNameCheck() {
    const nameRegex = new RegExp("^[a-zA-Z0-9_-]*$");
    if (nameRegex.test(this.farmName)) {
      this.farmNameErrorMessage = "";
      return true;
    } else {
      this.farmNameErrorMessage =
        "Name is not formatted correctly (All letters + numbers and (-,_) are allowed";
      return false;
    }
  }
  public createFarmFromName() {
    this.loadingCreateFarm = true;
    createFarm(
      this.address,
      this.$api,
      this.farmName,
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
            this.openCreateFarmDialog = false;
        }
        if (status.isFinalized) {
          console.log(
            `Transaction included at blockHash ${status.asFinalized}`
          );
          if (!events.length) {
            this.$toasted.show("Farm creation failed!");
            this.openCreateFarmDialog = false;
            this.loadingCreateFarm = false;
          } else {
            // Loop through Vec<EventRecord> to display all events
            events.forEach(({ phase, event: { data, method, section } }) => {
              console.log(`\t' ${phase}: ${section}.${method}:: ${data}`);
              if (section === "tfgridModule" && method === "FarmStored") {
                this.$toasted.show("Farm created!");
                this.loadingCreateFarm = false;
                this.farmName = "";
                getFarm(this.$api, this.id).then((farms) => {
                  this.farms = farms;
                });
                this.openCreateFarmDialog = false;
              } else if (section === "system" && method === "ExtrinsicFailed") {
                this.$toasted.show("Farm creation failed!");
                this.openCreateFarmDialog = false;
                this.loadingCreateFarm = false;
              }
            });
          }
        }
      }
    ).catch((err) => {
      this.$toasted.show(err.message);
      this.openCreateFarmDialog = false;
      this.loadingCreateFarm = false;
    });
  }
  public addV2Address() {
    setFarmPayoutV2Address(
      this.$route.params.accountID,
      this.$api,
      this.expanded[0].id, //farm ID
      this.v2_address,
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
          if (!events.length) {
            this.$toasted.show("Adding a V2 address failed!");
            this.openV2AddressDialog = false;
          } else {
            // Loop through Vec<EventRecord> to display all events
            events.forEach(({ phase, event: { data, method, section } }) => {
              console.log(`\t' ${phase}: ${section}.${method}:: ${data}`);
              if (
                section === "tfgridModule" &&
                method === "FarmPayoutV2AddressRegistered"
              ) {
                this.$toasted.show("Address added!");
                getFarm(this.$api, this.id).then((farms) => {
                  this.farms = farms;
                });
                this.openV2AddressDialog = false;
              } else if (section === "system" && method === "ExtrinsicFailed") {
                this.$toasted.show("Adding a V2 address failed!");
                this.openV2AddressDialog = false;
              }
            });
          }
        }
      }
    ).catch((err) => {
      this.$toasted.show(err.message);
      this.openV2AddressDialog = false;
    });
  }
}
</script>
<style scoped>
.v2address {
  overflow: hidden;
  text-overflow: ellipsis;
}

.theme--dark.v-btn.v-btn--has-bg {
  background-color: #064663;
}
.farm {
  font-weight: 500 !important;
}
</style>
