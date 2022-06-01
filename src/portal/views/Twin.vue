<template>

  <v-container v-if="$store.state.portal.accounts.length === 0">
    <v-card>
      <WelcomeWindow />
    </v-card>
  </v-container>

  <div
    style="padding-top:100ox"
    v-else
  >
    <v-container v-if="editingTwin">
      <v-dialog
        transition="dialog-bottom-transition"
        max-width="600"
        v-model="editingTwin"
      >

        <v-card>
          <v-toolbar
            color="primary"
            dark
          >Edit Twin</v-toolbar>
          <v-card-text>
            <div class="text-h2 pa-12">
              <v-text-field
                v-model="ipv"
                label="Twin IP ::1"
                :error-messages="ipErrorMessage"
                :rules="[
              () => !!ip || 'This field is required',
              ipcheck
            ]"
              ></v-text-field>
            </div>
          </v-card-text>
          <v-card-actions class="justify-end">
            <v-btn @click="editingTwin = false">Close</v-btn>
            <v-btn
              @click="updateTwin"
              :loading="loadingEditTwin"
            >Submit</v-btn>
          </v-card-actions>
        </v-card>

      </v-dialog>
    </v-container>
    <v-container>
      <v-card
        color="#388E3C"
        class="my-3 pa-3 text-center"
      >
        <h2> Congratulations {{$route.query.accountName}} on creating a twin! <br />
          You can now interact with the TF Grid</h2>

      </v-card>
      <v-card
        color="#512DA8"
        class="my-3 pa-3 text-center"
      >
        <h3>Twin Details</h3>

        <v-list>
          <v-list-item>
            ID: {{id}}
          </v-list-item>

          <v-list-item>
            IP: {{ip}}
          </v-list-item>

          <v-list-item>
            ADDRESS: {{address}}
          </v-list-item>
        </v-list>
        <v-card-actions class="justify-end">
          <v-btn
            @click="editTwin"
            color="#388E3C"
          >Edit</v-btn>
          <v-btn
            @click="openDeleteTwin"
            :loading="loadingDeleteTwin"
            color="red"
          >Delete</v-btn>
        </v-card-actions>

      </v-card>
      <h4 class="text-center my-5 pa-5">What do you wish to do?</h4>
      <div class="d-flex row justify-center align-center">
        <v-card
          v-for="link in links"
          :key="link.label"
          class="pa-5 mx-3"
          @click="redirectToLabelRoute(link.path, address)"
        >{{link.label.toUpperCase()}}</v-card>

      </div>

    </v-container>
    <v-dialog
      max-width="600"
      v-model="openDeleteTwinDialog"
    >
      <v-card>
        <v-card-title class="text-h5">Are you certain you want to delete this twin?</v-card-title>
        <v-card-text>This will delete the twin on the chain, this action is irreversible</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue darken-1"
            text
            @click="openDeleteTwinDialog = false"
          >Cancel</v-btn>
          <v-btn
            color="blue darken-1"
            text
            @click="callDeleteTwin()"
          >OK</v-btn>
          <v-spacer></v-spacer>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>

</template>

<script lang="ts">
import WelcomeWindow from "@/components/WelcomeWindow.vue";
import { Component, Vue } from "vue-property-decorator";
import { getBalance } from "../lib/balance";
import { deleteTwin, getTwin, getTwinID, updateTwinIP } from "../lib/twin";

@Component({
  name: "Twin",
  components: { WelcomeWindow },
})
export default class TwinView extends Vue {
  $api: any;
  editingTwin = false;
  ip: any = [];
  ipv = "";
  id: any = [];
  address = "";
  twin: any;
  accountName: any;
  balance: any = 0;
  loadingDeleteTwin = false;
  openDeleteTwinDialog = false;
  ipErrorMessage = "";
  loadingEditTwin = false;
  links = [
    {
      label: "transfer tft",
      path: "account-transfer",
    },
    {
      label: "manage farms",
      path: "account-farms",
    },
    {
      label: "manage nodes",
      path: "account-nodes",
    },
  ];
  updated() {
    this.address = this.$route.params.accountID;
    if (this.$route.query.twinIP && this.$route.query.twinID) {
      this.id = this.$route.query.twinID;
      this.accountName = this.$route.query.accountName;
    }
    if (this.$route.query.balance !== this.balance) {
      this.balance = this.$route.query.balance;
    }
  }
  mounted() {
    this.address = this.$route.params.accountID;
    if (this.$route.query.twinIP && this.$route.query.twinID) {
      this.ip = this.$route.query.twinIP;
      this.id = this.$route.query.twinID;
      this.accountName = this.$route.query.accountName;
    }
    this.balance = this.$route.query.balance;
  }
  unmounted() {
    this.balance = 0;
    this.address = "";
  }
  ipcheck() {
    if (this.ipv === "") return true;

    const ip4Regex = new RegExp(
      "^([0-9]{1,3}.){3}[0-9]{1,3}(/([0-9]|[1-2][0-9]|3[0-2]))$"
    );
    const ip6Regex = new RegExp(
      "(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]).){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]).){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"
    );
    if (ip4Regex.test(this.ipv)) {
      this.ipErrorMessage = "";
      return true;
    } else if (ip6Regex.test(this.ipv)) {
      this.ipErrorMessage = "";
      return true;
    } else {
      this.ipErrorMessage = "IP address is not formatted correctly";
      return false;
    }
  }
  public redirectToLabelRoute(path: string, address: string) {
    this.$router.push({
      name: `${path}`,
      path: `/:accountID/${path}`,
      params: { accountID: `${address}` },
      query: {
        accountName: `${this.accountName}`,
        twinID: this.id,
        balance: `${this.balance}`,
      },
    });
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
      this.ip,
      (res: { events?: never[] | undefined; status: any }) => {
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
          events.forEach(
            async ({ phase, event: { data, method, section } }) => {
              console.log(`\t' ${phase}: ${section}.${method}:: ${data}`);
              if (section === "tfgridModule" && method === "TwinUpdated") {
                this.loadingEditTwin = false;
                this.$toasted.show("Twin updated!");

                this.id = await getTwinID(
                  this.$api,
                  this.$route.params.accountID
                );
                this.balance = await getBalance(this.$api, this.address);
                this.twin = await getTwin(this.$api, this.id);
                this.ip = this.twin.ip;
                this.editingTwin = false;
              } else if (section === "system" && method === "ExtrinsicFailed") {
                this.$toasted.show("Twin creation/update failed!");
                this.loadingEditTwin = false;
              }
            }
          );
        }
      }
    ).catch((err: { message: any }) => {
      this.$toasted.show(err.message);
      this.loadingEditTwin = false;
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
      this.id,
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
    ).catch((err: { message: any }) => {
      this.$toasted.show(err.message);
      this.loadingDeleteTwin = false;
    });
  }
}
</script>