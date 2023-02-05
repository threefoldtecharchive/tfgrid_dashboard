<template>
  <v-container v-if="$store.state.portal.accounts.length === 0">
    <v-card>
      <WelcomeWindow />
    </v-card>
  </v-container>

  <div style="padding-top: 100px" v-else>
    <v-container v-if="editingTwin">
      <v-dialog transition="dialog-bottom-transition" max-width="600" v-model="editingTwin">
        <v-card>
          <v-toolbar color="primary" dark>Edit Twin</v-toolbar>
          <v-card-text>
            <div class="text-h2 pa-12">
              <v-form v-model="isValidTwinIP">
                <v-text-field
                  v-model="relay"
                  label="Twin Relay"
                  :rules="[() => !!relay || 'This field is required']"
                ></v-text-field>
              </v-form>
            </div>
          </v-card-text>
          <v-card-actions class="justify-end">
            <v-btn @click="editingTwin = false" class="grey lighten-2 black--text">Close</v-btn>
            <v-btn class="primary white--text" @click="updateTwin" :loading="loadingEditTwin" :disabled="!isValidTwinIP"
              >Submit</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
    <v-container>
      <v-card color="primary white--text" class="my-3 pa-3 text-center">
        <h2>Twin Details</h2>
      </v-card>
      <v-card class="my-3 pa-3 text-center">
        <v-list>
          <v-list-item> ID: {{ id }} </v-list-item>

          <v-list-item> ADDRESS: {{ address }} </v-list-item>

          <v-list-item> RELAY: {{ relay }} </v-list-item>
        </v-list>
        <v-card-actions class="justify-end">
          <v-btn @click="editTwin" color="primary">Edit</v-btn>
          <!-- <v-btn @click="openDeleteTwin" :loading="loadingDeleteTwin" color="red" class="white--text">Delete</v-btn> -->
        </v-card-actions>
      </v-card>
    </v-container>
    <v-dialog max-width="600" v-model="openDeleteTwinDialog">
      <v-card>
        <v-card-title class="text-h5">Are you certain you want to delete this twin?</v-card-title>
        <v-card-text>This will delete the twin on the chain, this action is irreversible</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey lighten-2 black--text" @click="openDeleteTwinDialog = false">Cancel</v-btn>
          <v-btn color="primary white--text" @click="callDeleteTwin()">OK</v-btn>
          <v-spacer></v-spacer>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import WelcomeWindow from "../components/WelcomeWindow.vue";
import { Component, Vue } from "vue-property-decorator";
import { deleteTwin, getTwin, getTwinID, updateTwinIP } from "../lib/twin";
import { hex2a } from "@/portal/lib/util";
import { UserCredentials } from "../store/state";
@Component({
  name: "Twin",
  components: { WelcomeWindow },
})
export default class TwinView extends Vue {
  $api: any;
  $credentials!: UserCredentials;
  editingTwin = false;
  relay = "";
  id: string | (string | null)[] = "";
  address = "";
  twin: { ip: string } = { ip: "" };
  accountName: string | (string | null)[] = "";
  isValidTwinIP = false;
  loadingDeleteTwin = false;
  openDeleteTwinDialog = false;
  loadingEditTwin = false;
  updated() {
    this.address = this.$credentials.accountAddress;
    this.id = String(this.$credentials.twinID);
    this.accountName = this.$credentials.accountName;
  }
  mounted() {
    if (this.$api && this.$credentials && this.$credentials.relayAddress !== "" && this.$credentials.twinID != 0) {
      this.address = this.$credentials.accountAddress;
      this.relay = this.$credentials.relayAddress;
      this.id = String(this.$credentials.twinID);
      this.accountName = this.$credentials.accountName;
    } else {
      this.$router.push({
        name: "accounts",
        path: "/",
      });
    }
  }
  unmounted() {
    this.address = "";
  }
  decodeHex(input: string) {
    return hex2a(input);
  }
  public editTwin() {
    console.log("editing a twin");
    this.editingTwin = true;
  }
  public updateTwin() {
    this.loadingEditTwin = true;
    updateTwinIP(
      this.$route.params.accountID,
      this.$api,
      `${this.relay}`,
      (res: { events?: never[] | undefined; status: { type: string; asFinalized: string; isFinalized: string } }) => {
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
          console.log(`Transaction included at blockHash ${status.asFinalized}`);
          if (!events.length) {
            this.$toasted.show("Twin creation/update failed!");
            this.loadingEditTwin = false;
          } else {
            // Loop through Vec<EventRecord> to display all events
            events.forEach(async ({ phase, event: { data, method, section } }) => {
              console.log(`\t' ${phase}: ${section}.${method}:: ${data}`);
              if (section === "tfgridModule" && method === "TwinUpdated") {
                this.loadingEditTwin = false;
                this.$toasted.show("Twin updated!");
                this.id = await getTwinID(this.$api, this.$route.params.accountID);
                this.twin = await getTwin(this.$api, parseFloat(`${this.id}`));
                this.editingTwin = false;
                this.relay = this.$credentials.relayAddress;
              } else if (section === "system" && method === "ExtrinsicFailed") {
                this.$toasted.show("Twin creation/update failed!");
                this.loadingEditTwin = false;
                this.relay = this.$credentials.relayAddress;
              }
            });
          }
        }
      },
    ).catch((err: { message: string }) => {
      console.log(err.message);
      this.$toasted.show("Twin creation/update failed!");
      this.loadingEditTwin = false;
      this.relay = this.$credentials.relayAddress;
    });
  }
  openDeleteTwin() {
    this.openDeleteTwinDialog = true;
  }
  public callDeleteTwin() {
    this.loadingDeleteTwin = true;
    this.openDeleteTwinDialog = false;
    deleteTwin(
      this.address,
      this.$api,
      `${this.id}`,
      (res: { events?: never[] | undefined; status: { type: string; asFinalized: string; isFinalized: string } }) => {
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
          console.log(`Transaction included at blockHash ${status.asFinalized}`);
          if (!events.length) {
            this.$toasted.show("Deleting a twin failed");
            this.loadingDeleteTwin = false;
          } else {
            // Loop through Vec<EventRecord> to display all events
            events.forEach(({ phase, event: { data, method, section } }) => {
              console.log(`\t' ${phase}: ${section}.${method}:: ${data}`);
              if (section === "tfgridModule" && method === "TwinDeleted") {
                this.$toasted.show("Twin deleted!");
                this.loadingDeleteTwin = false;
                this.openDeleteTwinDialog = false;
                this.$router.push({
                  name: "account",
                  path: "account",
                  params: { accountID: `${this.address}` },
                  query: { accountName: `${this.accountName}` },
                });
              } else if (section === "system" && method === "ExtrinsicFailed") {
                this.$toasted.show("Deleting a twin failed");
                this.loadingDeleteTwin = false;
              }
            });
          }
        }
      },
    ).catch((err: { message: string }) => {
      this.$toasted.show(err.message);
      this.loadingDeleteTwin = false;
    });
  }
}
</script>
