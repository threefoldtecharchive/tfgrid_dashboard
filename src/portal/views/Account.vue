<template>
  <v-container
    fluid
    v-if="termsNotAccepted"
    height="100%"
  >
    <v-dialog
      v-model="termsNotAccepted"
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
      <h3>Choose your preferred method : </h3>
    </v-card>
    <v-container fluid>
      <v-row>

        <v-col>
          <v-card
            class="pa-5 text-center"
            height="150"
          >
            <h3>
              Create a Twin using Planetary
              using Yggdrasil IPV6
            </h3>
            <v-text-field label="Twin IP ::1">

            </v-text-field>
          </v-card>
        </v-col>
        <v-col>
          <v-card
            class="pa-5 text-center"
            height="150"
          >
            <h3>
              Create a Twin automatically
            </h3>

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
import { connect } from "../lib/connect";
import blake from "blakejs";
import { acceptTermsAndCondition, checkTCAcceptance } from "../lib/accepttc";
@Component({
  name: "AccountView",
})
export default class AccountView extends Vue {
  dialog = false;
  termsNotAccepted = true;
  documentLink = "https://library.threefold.me/info/legal/#/";
  documentHash = "";

  address = "";
  api: any;
  activated = true;
  acceptedTC: boolean | undefined;
  async mounted() {
    this.address = this.$route.params.accountID;
    this.api = await connect();
    const balance = (await getBalance(this.api, this.address)) / 1e7;
    this.$store.dispatch("portal/setBalanceAction", balance);
    let document = await axios.get(this.documentLink);
    this.documentHash = blake.blake2bHex(document.data);
  }

  public acceptTC() {
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
              this.termsNotAccepted = false;
              console.log("accepted!");
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