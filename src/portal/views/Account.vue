<template>
  <v-container
    fluid
    v-if="openDialog"
    height="100%"
  >
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
      <v-btn
        @click="acceptTC"
        :loading="loadingAcceptedTC"
      >
        accept terms and conditions
      </v-btn>

    </v-dialog>
  </v-container>

  <v-container v-else-if="$store.state.portal.accounts.length === 0">
    <v-card
      transparent
      outlined
    >
      <WelcomeWindow />
    </v-card>
  </v-container>

  <v-container v-else-if="!twinCreated">
    <v-card class="text-center primary white--text py-5 my-3">
      <h2>
        Welcome aboard {{ $route.query.accountName }}, <br />
        Let’s get you connected to the TF Grid !
      </h2>
    </v-card>
    <v-card class="text-center pa-5">
      <h3>Choose your preferred method to create a Twin:</h3>
    </v-card>
    <v-container
      fluid
      class="px-0"
    >
      <v-row>
        <v-col>
          <v-card
            class="pa-5 text-center"
            height="175"
          >
            <h3>Planetary using Yggdrasil IPV6</h3>
            <v-text-field
              label="Twin IP ::1"
              v-model="ip"
              :error-messages="ipErrorMessage"
              :rules="[() => !!ip || 'This field is required', ipcheck]"
            >
            </v-text-field>
            <v-btn
              class="primary"
              :loading="loadingTwinCreate"
              @click="createTwinFunc(ip)"
            >create</v-btn>
          </v-card>
        </v-col>
        <v-col>
          <v-card
            class="pa-5 text-center d-flex align-center justify-center"
            height="175"
          >
            <v-btn
              class="primary"
              :loading="loadingTwinCreate"
              @click="createTwinFunc('::1')"
            >automatically</v-btn>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-card class="pa-5 text-center d-flex align-center justify-center">
            <v-btn
              class="primary"
              :target="'blank'"
              :href="'https://library.threefold.me/info/manual/#/manual__yggdrasil_client'"
            >why do i even need a twin?</v-btn>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-container>
</template>

<script lang="ts">
import axios from "axios";
import { Component, Vue } from "vue-property-decorator";
import { getBalance } from "../lib/balance";
import { createTwin, getTwin, getTwinID } from "../lib/twin";
import blake from "blakejs";
import {
  acceptTermsAndCondition,
  userAcceptedTermsAndConditions,
} from "../lib/accepttc";
import WelcomeWindow from "../../components/WelcomeWindow.vue";
import { activateThroughActivationService } from "../lib/activation";
import Twin from "./Twin.vue";

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
  balance: any;
  twinID = 0;
  ip = "";
  twin: any;
  loadingTC = true;
  loadingTwinCreate = false;
  ipErrorMessage = "";
  loadingAcceptedTC = false;

  async updated() {
    if (this.$api) {
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
            twinIP: this.twin.ip,
            balanceFree: `${this.balance.free}`,
            balanceReserved: `${this.balance.reserved}`,
          },
        });
      }
    }
    this.openDialog = !(await userAcceptedTermsAndConditions(
      this.$api,
      this.address
    ));
  }
  async mounted() {
    if (this.$api) {
      this.address = this.$route.params.accountID;
      this.balance = await getBalance(this.$api, this.address);
      this.twinID = await getTwinID(this.$api, this.address);
      if (this.twinID) {
        this.twinCreated = true;
      }
      this.openDialog = !(await userAcceptedTermsAndConditions(
        this.$api,
        this.address
      ));
      let document = await axios.get(this.documentLink);
      this.documentHash = blake.blake2bHex(document.data);
    } else {
      this.$toasted.show(
        `Can't connect to Polkadot API right now, please refresh the page or try again later`
      );
      this.$router.push({
        name: "accounts",
        path: "/",
      });
    }
  }
  unmounted() {
    this.address = "";
    this.balance = 0;
    this.twinID = 0;
  }
  ipcheck() {
    if (this.ip === "") return true;
    const ip4Regex = new RegExp(
      "^([0-9]{1,3}.){3}[0-9]{1,3}(/([0-9]|[1-2][0-9]|3[0-2]))$"
    );
    const ip6Regex = new RegExp(
      "(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]).){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]).){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"
    );
    if (ip4Regex.test(this.ip)) {
      this.ipErrorMessage = "";
      return true;
    } else if (ip6Regex.test(this.ip)) {
      this.ipErrorMessage = "";
      return true;
    } else {
      this.ipErrorMessage = "IP address is not formatted correctly";
      return false;
    }
  }
  public async createTwinFunc(ip: string) {
    this.loadingTwinCreate = true;
    await createTwin(
      this.address,
      this.$api,
      ip,
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
            if (section === "tfgridModule" && method === "TwinStored") {
              this.loadingTwinCreate = false;
              this.$toasted.show("Twin created!");
              this.twinCreated = true;
            } else if (section === "system" && method === "ExtrinsicFailed") {
              this.$toasted.show("Twin creation failed!");
              this.loadingTwinCreate = false;
            }
          });
        }
      }
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
            this.openDialog = false;
        }
        if (status.isFinalized) {
          console.log(
            `Transaction included at blockHash ${status.asFinalized}`
          );
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
    ).catch((err: { message: string }) => {
      this.$toasted.show(err.message);
      this.loadingAcceptedTC = false;
    });
  }
}
</script>

