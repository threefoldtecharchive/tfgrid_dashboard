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
      <v-btn @click="acceptTC">
        accept terms and conditions
      </v-btn>

    </v-dialog>
  </v-container>
  <v-container v-else-if="$store.state.portal.accounts.length === 0">
    <v-card>
      <WelcomeWindow />
    </v-card>
  </v-container>
  <v-container v-else>
    <v-card
      color="#388E3C"
      class="text-center py-5 my-3 "
    >
      <h2>
        Welcome aboard {{$route.query.accountName}}, <br>
        Let’s get you connected to the TF Grid !

      </h2>
    </v-card>
    <v-card
      color="#512DA8"
      class="text-center pa-5"
    >
      <h3>Choose your preferred method to create a Twin: </h3>
    </v-card>
    <v-container fluid>
      <v-row>

        <v-col>
          <v-card
            class="pa-5 text-center"
            height="175"
          >
            <h3>
              Planetary
              using Yggdrasil IPV6
            </h3>
            <v-text-field label="Twin IP ::1">

            </v-text-field>
            <v-btn>create</v-btn>
          </v-card>
        </v-col>
        <v-col>
          <v-card
            class="pa-5 text-center d-flex align-center justify-center"
            height="175"
          >
            <v-btn @click="addAutoTwin">automatically</v-btn>

          </v-card>
        </v-col>

      </v-row>
      <v-row>
        <v-col>
          <v-card class="pa-5 text-center d-flex align-center justify-center">
            <v-btn>why do i even need a twin?</v-btn>
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
import { connect } from "../lib/connect";
import blake from "blakejs";
import {
  acceptTermsAndCondition,
  userAcceptedTermsAndConditions,
} from "../lib/accepttc";
import WelcomeWindow from "../../components/WelcomeWindow.vue";
import { activateThroughActivationService } from "../lib/activation";

@Component({
  name: "AccountView",
  components: { WelcomeWindow },
})
export default class AccountView extends Vue {
  documentLink = "https://library.threefold.me/info/legal/#/";
  documentHash = "";
  openDialog = true;
  address = "";
  api: any;
  activated = true;
  balance = 0;
  twinID = 0;
  components = ["WelcomeWindow"];
  async mounted() {
    this.address = this.$route.params.accountID;
    this.api = await connect();
    this.$store.dispatch("portal/setAPIAction", this.api);

    this.openDialog = !(await userAcceptedTermsAndConditions(
      this.api,
      this.address
    ));
    this.balance = (await getBalance(this.api, this.address)) / 1e7;
    this.$store.dispatch("portal/setBalanceAction", this.balance);
    this.$store.dispatch("portal/setCurrentAccountIDAction", this.address);
    let document = await axios.get(this.documentLink);
    this.documentHash = blake.blake2bHex(document.data);
    this.twinID = await getTwinID(this.api, this.address);
    this.twinID !== 0
      ? getTwin(this.api, this.twinID)
      : console.log("no twin ID available");
  }
  unmounted() {
    this.$store.dispatch("portal/setBalanceAction", 0);
    this.$store.dispatch("portal/setCurrentAccountIDAction", "");
  }
  public async addAutoTwin() {
    await createTwin(
      this.address,
      this.api,
      "::1",
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
            if (section === "tfgridModule" && method === "TwinStored") {
              console.log("Twin created!");
              const twinStoredEvent = data[0];
              console.log(twinStoredEvent);
            } else if (section === "system" && method === "ExtrinsicFailed") {
              console.log("Twin creation failed!");
            }
          });
        }
      }
    );
  }
  public acceptTC() {
    activateThroughActivationService(this.address);
    acceptTermsAndCondition(
      this.api,
      this.address,
      this.documentLink,
      this.documentHash,
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

          events.forEach(({ phase, event: { data, method, section } }) => {
            console.log(`\t' ${phase}: ${section}.${method}:: ${data}`);
            if (section === "system" && method === "ExtrinsicSuccess") {
              console.log("accepted!");
              this.openDialog = false;
            } else if (section === "system" && method === "ExtrinsicFailed") {
              console.log("rejected");
            }
          });
        }
      }
    );
  }
}
</script>
<style scoped>
</style>