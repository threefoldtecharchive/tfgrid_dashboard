<template>
  <v-container fluid>

    <v-card
      class="my-3 pa-3 text-center"
      color="#512DA8"
    >
      <h2>Greetings {{$route.query.accountName}}, you can now manage your farms!</h2>
    </v-card>
    <v-card
      color="#388E3C"
      class="my-3 pa-3 text-center d-flex justify-center align-baseline"
    >
      <h3> Don't have any farms? Start by creating one: </h3>

      <v-btn
        @click="openCreateFarmDialog = true"
        class="my-3 mx-5"
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
          dark
        >Create Farm</v-toolbar>
        <v-card-text>
          <v-text-field
            label="Farm Name"
            v-model="farmName"
            required
            :error-messages="farmNameErrorMessage"
            :rules="[
                () => !!farmName || 'This field is required',
                farmNameCheck
              ]"
          ></v-text-field>

        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn @click="openCreateFarmDialog = false">Close</v-btn>
          <v-btn @click="createFarmFromName">Submit</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-text-field
      v-model="searchTerm"
      color="purple darken-2"
      label="Search by farm name or ID"
    ></v-text-field>
    <v-data-table
      :headers="headers"
      :items="filteredFarms()"
      :single-expand="singleExpand"
      :expanded.sync="expanded"
      item-key="name"
      show-expand
      class="elevation-1"
      dark
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Your Farms</v-toolbar-title>
          <v-spacer></v-spacer>

        </v-toolbar>
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
                  <span>{{ item.certification_type }}</span>
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
                <v-row>

                  <span>
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
                  <v-toolbar
                    color="primary"
                    dark
                  >Add/Edit V2 Stellar Address</v-toolbar>
                  <v-card-text>
                    <v-text-field
                      v-model="v2_address"
                      label="Stellar Wallet Address"
                    >

                    </v-text-field>
                  </v-card-text>
                  <v-card-actions class="justify-end">
                    <v-btn @click="openV2AddressDialog = false">Close</v-btn>
                    <v-btn @click="addV2Address">Submit</v-btn>
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
            <v-row>
              <PublicIPTable
                :ips="item.public_ips"
                :deleteIP="deletePublicIP"
                :loadingDelete="loadingDeleteIP"
                :createIP="createPublicIP"
                :loadingCreate="loadingCreateIP"
              />
            </v-row>

          </v-container>

        </td>
      </template>
    </v-data-table>

  </v-container>
</template>

<script lang="ts">
import PublicIPTable from "@/components/PublicIPTable.vue";
import { Component, Vue, Watch } from "vue-property-decorator";
import {
  createFarm,
  createIP,
  deleteIP,
  deleteNode,
  getFarm,
  getNodesByFarmID,
  setFarmPayoutV2Address,
} from "../lib/farms";

@Component({
  name: "FarmsView",
  components: { PublicIPTable },
})
export default class FarmsView extends Vue {
  headers = [
    { text: "Farm ID", value: "id" },
    { text: "Farm name", value: "name" },
    { text: "Linked Twin ID", value: "twin_id" },
    { text: "Certification type", value: "certification_type" },
    { text: "Pricing Policy ID", value: "pricing_policy_id" },
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
  nodes: any;
  loadingNodes = false;
  loadingNodeDelete = false;
  loadingAddNodePublicConfig = false;
  searchTerm = "";
  async mounted() {
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
  }
  @Watch("$route.query.twinID") async onPropertyChanged(
    value: number,
    oldValue: number
  ) {
    console.log(
      `switching from account ${oldValue} farms to account ${value} farms`
    );

    this.farms = await getFarm(this.$api, value);
  }
  updated() {
    this.address;
    this.id;

    this.v2_address;
    this.farmName;
  }
  public filteredFarms() {
    if (this.searchTerm.length !== 0) {
      return this.farms.filter(
        (farm: { name: string; id: any }) =>
          farm.name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
          `${farm.id}`.includes(this.searchTerm)
      );
    }
    return this.farms;
  }
  async getNodes() {
    console.log("getting nodes again");
    this.nodes = await getNodesByFarmID(this.$api, this.farms);
    console.log(this.nodes);
  }
  deleteNodeFarm(nodeID: any) {
    this.loadingNodeDelete = true;
    deleteNode(
      this.$route.params.accountID,
      this.$api,
      nodeID,
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
            console.log(`Transaction submitted`);
        }

        if (status.isFinalized) {
          console.log(
            `Transaction included at blockHash ${status.asFinalized}`
          );

          // Loop through Vec<EventRecord> to display all events
          events.forEach(({ phase, event: { data, method, section } }) => {
            console.log(`\t' ${phase}: ${section}.${method}:: ${data}`);
            if (section === "tfgridModule" && method === "NodeDeleted") {
              console.log("Node deleted from farm!");
              this.loadingNodeDelete = false;
              getNodesByFarmID(this.$api, this.farms).then(
                (nodes) => (this.nodes = nodes)
              );
            } else if (section === "system" && method === "ExtrinsicFailed") {
              console.log("Node deletion failed");
              this.loadingNodeDelete = false;
            }
          });
        }
      }
    ).catch((err) => {
      console.log(err.message);
      this.loadingNodeDelete = false;
    });
  }
  deletePublicIP(publicIP: any) {
    this.loadingDeleteIP = true;
    deleteIP(
      this.$route.params.accountID,
      this.$api,
      this.expanded[0].id,
      publicIP,
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
            console.log(`Transaction submitted`);
        }

        if (status.isFinalized) {
          console.log(
            `Transaction included at blockHash ${status.asFinalized}`
          );

          // Loop through Vec<EventRecord> to display all events
          events.forEach(({ phase, event: { data, method, section } }) => {
            console.log(`\t' ${phase}: ${section}.${method}:: ${data}`);
            if (section === "tfgridModule" && method === "FarmUpdated") {
              console.log("IP deleted!");
              getFarm(this.$api, this.id).then((farms) => {
                this.farms = farms;
                this.loadingDeleteIP = false;
              });
            } else if (section === "system" && method === "ExtrinsicFailed") {
              console.log("IP deletion failed!");
              this.loadingDeleteIP = false;
            }
          });
        }
      }
    ).catch((err) => {
      console.log(err.message);
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
            console.log(`Transaction submitted`);
        }

        if (status.isFinalized) {
          console.log(
            `Transaction included at blockHash ${status.asFinalized}`
          );

          // Loop through Vec<EventRecord> to display all events
          events.forEach(({ phase, event: { data, method, section } }) => {
            console.log(`\t' ${phase}: ${section}.${method}:: ${data}`);
            if (section === "tfgridModule" && method === "FarmUpdated") {
              console.log("IP created!");
              getFarm(this.$api, this.id).then((farms) => {
                this.farms = farms;
                this.loadingCreateIP = false;
              });
            } else if (section === "system" && method === "ExtrinsicFailed") {
              console.log("Adding an IP failed!");
            }
          });
        }
      }
    ).catch((err) => {
      console.log(err.message);
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
    createFarm(
      this.address,
      this.$api,
      this.farmName,
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
            console.log(`Transaction submitted`);
        }

        if (status.isFinalized) {
          console.log(
            `Transaction included at blockHash ${status.asFinalized}`
          );

          // Loop through Vec<EventRecord> to display all events
          events.forEach(({ phase, event: { data, method, section } }) => {
            console.log(`\t' ${phase}: ${section}.${method}:: ${data}`);
            if (section === "tfgridModule" && method === "FarmStored") {
              console.log("Farm created!");
              getFarm(this.$api, this.id).then((farms) => {
                this.farms = farms;
                this.openCreateFarmDialog = false;
              });
            } else if (section === "system" && method === "ExtrinsicFailed") {
              console.log("Farm creation failed!");
            }
          });
        }
      }
    ).catch((err) => {
      console.log(err.message);
    });
  }
  public addV2Address() {
    setFarmPayoutV2Address(
      this.$route.params.accountID,
      this.$api,
      this.expanded[0].id, //farm ID
      this.v2_address,
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
            console.log(`Transaction submitted`);
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
              method === "FarmPayoutV2AddressRegistered"
            ) {
              console.log("Address added!");
              getFarm(this.$api, this.id).then((farms) => {
                this.farms = farms;
              });
              this.openV2AddressDialog = false;
            } else if (section === "system" && method === "ExtrinsicFailed") {
              console.log("Adding a V2 address failed!");
            }
          });
        }
      }
    ).catch((err) => {
      console.log(err.message);
    });
  }
}
</script>
<style scoped>
.v2address {
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>