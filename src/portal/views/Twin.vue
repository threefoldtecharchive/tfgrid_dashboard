<!-- eslint-disable no-dupe-class-members -->
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
          <div class="text-h2 pa-10">
            <v-form>
              <v-select
                :items="items"
                label="Please select a relay:"
                v-model="selectedItem.item_id"
                item-text="name"
                item-value="id"
              >
              </v-select>
            </v-form>
          </div>
          <v-card-actions class="justify-end pa-5">
            <v-btn @click="editingTwin = false" :disabled="loadingEditTwin" class="grey lighten-2 black--text"
              >Close</v-btn
            >
            <v-btn class="primary white--text" @click="updateTwin" :loading="loadingEditTwin">Submit</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
    <v-container>
      <template v-if="twin.relay == 'null'">
        <div class="mt-4">
          <v-alert color="rgb(25, 130, 177)" dense type="info">
            You should <strong>edit</strong> your twin details to change your relay
          </v-alert>
        </div>
      </template>
      <v-card color="primary white--text" class="my-3 pa-3 text-center">
        <h2>Twin Details</h2>
      </v-card>
      <v-card class="my-3 pa-3 text-center">
        <v-list>
          <v-list-item> ID: {{ twin.id }} </v-list-item>

          <v-list-item> Address: {{ twin.address }} </v-list-item>

          <v-list-item> Relay: {{ twin.relay }} </v-list-item>
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
import { deleteTwin, getTwin, getTwinID, updateRelay } from "../lib/twin";
import { UserCredentials } from "../store/state";
import config from "@/portal/config";

@Component({
  name: "Twin",
  components: { WelcomeWindow },
})
export default class TwinView extends Vue {
  $api: any;
  $credentials!: UserCredentials;
  editingTwin = false;
  twin: { relay: string | null; pk: string | null; address: string; id: string | null } = {
    relay: "",
    pk: null,
    id: "",
    address: "",
  };
  accountName: string | (string | null)[] = "";
  isValidTwinIP = false;
  loadingDeleteTwin = false;
  openDeleteTwinDialog = false;
  loadingEditTwin = false;
  items = [{ id: 1, name: config.relay }];
  selectedItem = {
    item_id: 1,
  };
  selectedName = "";
  updated() {
    this.twin.address = this.$credentials.accountAddress;
    this.twin.id = String(this.$credentials.twinID);
    this.accountName = this.$credentials.accountName;
    this.twin.relay = this.$credentials.relayAddress;
    this.twin.pk = this.$credentials.publicKey;
    this.selectedName = this.items.filter(item => item.id === this.selectedItem.item_id)[0].name;
  }
  mounted() {
    if (this.$api && this.$credentials && this.$credentials.relayAddress !== "" && this.$credentials.twinID != 0) {
      this.twin.address = this.$credentials.accountAddress;
      this.twin.relay = this.$credentials.relayAddress;
      this.twin.id = String(this.$credentials.twinID);
      this.accountName = this.$credentials.accountName;
      this.selectedName = this.items.filter(item => item.id === this.selectedItem.item_id)[0].name;
    } else {
      this.$router.push({
        name: "accounts",
        path: "/",
      });
    }
  }
  unmounted() {
    this.twin.address = "";
  }
  public editTwin() {
    console.log("editing a twin");
    this.editingTwin = true;
  }
  public updateTwin() {
    this.loadingEditTwin = true;
    updateRelay(
      this.$route.params.accountID,
      this.$api,
      this.selectedName,
      this.twin.pk,
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
                this.twin.id = await getTwinID(this.$api, this.$route.params.accountID);
                this.twin = await getTwin(this.$api, parseFloat(`${this.twin.id}`));
                this.editingTwin = false;
                this.$credentials.relayAddress = this.selectedName;
                this.$credentials.publicKey = this.twin.pk;
              } else if (section === "system" && method === "ExtrinsicFailed") {
                this.$toasted.show("Twin creation/update failed!");
                this.loadingEditTwin = false;
                this.twin.relay = this.$credentials.relayAddress;
                this.twin.pk = this.$credentials.publicKey;
              }
            });
          }
        }
      },
    ).catch((err: { message: string }) => {
      console.log(err.message);
      this.$toasted.show("Twin creation/update failed!");
      this.loadingEditTwin = false;
      this.twin.relay = this.$credentials.relayAddress;
      this.twin.pk = this.$credentials.publicKey;
    });
  }
  openDeleteTwin() {
    this.openDeleteTwinDialog = true;
  }
  public callDeleteTwin() {
    this.loadingDeleteTwin = true;
    this.openDeleteTwinDialog = false;
    deleteTwin(
      this.twin.address,
      this.$api,
      `${this.twin.id}`,
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
                  params: { accountID: `${this.twin.address}` },
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
