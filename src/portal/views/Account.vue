<template>
  <v-container fluid v-if="openDialog" height="100%">
    <v-dialog
      v-model="openDialog"
      persistent
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
      style="background-color: black"
      :loading="loadingTC"
    >
      <iframe
        :src="documentLink"
        frameborder="0"
        style="background-color: white"
        allow="fullscreen"
        height="95%"
        width="100px"
        sandbox="allow-forms allow-modals allow-scripts allow-popups allow-same-origin "
      ></iframe>
      <v-btn @click="acceptTC" :loading="loadingAcceptedTC"> accept terms and conditions </v-btn>
    </v-dialog>
  </v-container>

  <v-container v-else-if="$store.state.portal.accounts.length === 0">
    <v-card transparent outlined>
      <WelcomeWindow />
    </v-card>
  </v-container>

  <v-container v-else-if="!twinCreated">
    <v-card class="text-center primary white--text py-5 my-3">
      <h2>
        Welcome aboard {{ $route.query.accountName }}, <br />
        Let’s get you connected to the TF Grid by creating a twin!
      </h2>
    </v-card>

    <v-container fluid class="px-0">
      <v-card class="pa-5 text-center" height="175">
        <h3>Choose a Relay Address</h3>
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
        <v-btn class="primary" :loading="loadingTwinCreate" @click="createTwinFunc(selectedName, pk)">create</v-btn>
      </v-card>

      <!-- <v-row>
        <v-col>
          <v-card class="pa-5 text-center d-flex align-center justify-center">
            <v-btn
              class="primary"
              :target="'blank'"
              :href="'https://library.threefold.me/info/manual/#/manual__yggdrasil_client'"
              >Why do I even need a twin?</v-btn
            >
          </v-card>
        </v-col>
      </v-row> -->
    </v-container>
  </v-container>
</template>

<script lang="ts">
import axios from "axios";
import { Component, Vue } from "vue-property-decorator";
import { balanceInterface, getBalance } from "../lib/balance";
import { createTwin, getTwin, getTwinID } from "../lib/twin";
import md5 from "md5";
import { acceptTermsAndCondition, userAcceptedTermsAndConditions } from "../lib/accepttc";
import WelcomeWindow from "../components/WelcomeWindow.vue";
import { activateThroughActivationService } from "../lib/activation";
import Twin from "./Twin.vue";
import { UserCredentials } from "../store/state";
import config from "@/portal/config";

@Component({
  name: "AccountView",
  components: { WelcomeWindow, Twin },
})
export default class AccountView extends Vue {
  documentLink = "https://library.threefold.me/info/legal/#/";
  documentHash = "";
  openDialog = true;
  twinCreated = false;
  address = "";
  $api: any;
  $credentials!: UserCredentials;
  balance: balanceInterface = { free: 0, reserved: 0 };
  twinID = 0;
  twin!: { id: any; relay: any };
  loadingTC = true;
  loadingTwinCreate = false;
  loadingAcceptedTC = false;
  items = [{ id: 1, name: config.relay }];
  selectedItem = {
    item_id: 1,
  };
  selectedName = "";
  pk = "";

  async updated() {
    if (this.$api && this.$credentials) {
      this.selectedName = this.items.filter(item => item.id === this.selectedItem.item_id)[0].name;
      this.address = this.$route.params.accountID;
      this.balance = await getBalance(this.$api, this.address);
      this.twinID = await getTwinID(this.$api, this.address);
      if (this.twinID) {
        this.twinCreated = true;
        this.twin = await getTwin(this.$api, this.twinID);
        this.$router.push({
          name: "account-twin",
          path: "/:accountID/account-twin",
          params: { accountID: `${this.$route.params.accountID}` },
          query: {
            accountName: `${this.$route.query.accountName}`,
            twinID: this.twin.id,
            balanceFree: `${this.balance.free}`,
            balanceReserved: `${this.balance.reserved}`,
          },
        });
      }
    }
    this.openDialog = !(await userAcceptedTermsAndConditions(this.$api, this.address));
  }
  async mounted() {
    if (this.$api) {
      this.address = this.$route.params.accountID;
      this.balance = await getBalance(this.$api, this.address);
      this.twinID = await getTwinID(this.$api, this.address);
      if (this.twinID) {
        this.twinCreated = true;
      }
      this.openDialog = !(await userAcceptedTermsAndConditions(this.$api, this.address));
      let document = await axios.get(this.documentLink);
      this.documentHash = md5(document.data);
      this.selectedName = this.items.filter(item => item.id === this.selectedItem.item_id)[0].name;
    } else {
      this.$toasted.show(`Can't connect to Polkadot API right now, please refresh the page or try again later`);
      this.$router.push({
        name: "accounts",
        path: "/",
      });
    }
  }
  unmounted() {
    this.address = "";
    this.balance = { free: 0, reserved: 0 };
    this.twinID = 0;
  }

  public async createTwinFunc(relay: string, pk: string) {
    this.loadingTwinCreate = true;
    await createTwin(
      this.address,
      this.$api,
      relay,
      pk,
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
            this.$toasted.show("Twin creation failed!");
            this.loadingTwinCreate = false;
          } else {
            // Loop through Vec<EventRecord> to display all events
            events.forEach(({ phase, event: { data, method, section } }) => {
              console.log(`\t' ${phase}: ${section}.${method}:: ${data}`);
              if (section === "tfgridModule" && method === "TwinStored") {
                this.loadingTwinCreate = false;
                this.$credentials.relayAddress = relay;
                this.$toasted.show("Twin created!");
                this.twinCreated = true;
              } else if (section === "system" && method === "ExtrinsicFailed") {
                this.$toasted.show("Twin creation failed!");
                this.loadingTwinCreate = false;
              }
            });
          }
        }
      },
    ).catch((err: { message: string }) => {
      this.$toasted.show(err.message);
      this.loadingTwinCreate = false;
    });
  }
  public acceptTC() {
    this.loadingAcceptedTC = true;
    activateThroughActivationService(this.address);
    acceptTermsAndCondition(
      this.$api,
      this.address,
      this.documentLink,
      this.documentHash,
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
            this.openDialog = false;
        }
        if (status.isFinalized) {
          console.log(`Transaction included at blockHash ${status.asFinalized}`);
          if (!events.length) {
            this.$toasted.show("rejected");
            this.loadingAcceptedTC = false;
          } else {
            events.forEach(({ phase, event: { data, method, section } }) => {
              console.log(`\t' ${phase}: ${section}.${method}:: ${data}`);
              if (section === "system" && method === "ExtrinsicSuccess") {
                this.$toasted.show("Accepted!");
                this.loadingTC = false;
                this.loadingAcceptedTC = false;
              } else if (section === "system" && method === "ExtrinsicFailed") {
                this.$toasted.show("rejected");
                this.loadingAcceptedTC = false;
              }
            });
          }
        }
      },
    ).catch((err: { message: string }) => {
      this.$toasted.show(err.message);
      this.loadingAcceptedTC = false;
    });
  }
}
</script>
