<template>
  <v-container>
    <v-card class="fund d-flex align-center font-weight-bold mr-4 primary" style="margin-right: 7% !important;">
      <v-card-text
        style="padding: 5px;"
        class="pr-0"
      >
        <v-tooltip>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              @click="openBalance = true"
              v-bind="attrs"
              v-on="on"
              class="d-flex align-center"
            >
              <p class="mr-1">{{ balanceFree }}</p>
              <p class="font-weight-black">TFT</p>
            </v-btn>
          </template>
          <span>View Balance Summary</span>
        </v-tooltip>
      </v-card-text>
      <v-card-actions class="px-0">
        <v-btn
          @click="addTFT()"
          style="max-width: 60px"
          :loading="loadingAddTFT"
        >+</v-btn>
      </v-card-actions>
    </v-card>
    <v-dialog
      v-model="openBalance"
      max-width="600"
    >
      <v-card>
        <v-toolbar color="primary"> Balance Summary </v-toolbar>
        <v-card-text class="pa-5">
          <v-container>
            <v-row> Free: {{ balanceFree }} TFT </v-row>
            <v-row> Reserved (Locked): {{ balanceReserved }} TFT </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn
            @click="openBalance = false"
            color="grey lighten-2 black--text"
          >Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>
<script lang="ts">
import config from "@/portal/config";
import { getBalance, getMoreFunds } from "@/portal/lib/balance";
import { Component, Prop, Vue } from "vue-property-decorator";
@Component({
  name: "FundsCard",
})
export default class FundsCard extends Vue {
  loadingAddTFT = false;
  $api: any;
  @Prop({ required: true }) balanceFree!: number;
  @Prop({ required: true }) balanceReserved!: number;
  openBalance = false;
  mounted() { 
    this.$root.$on('updateBalance', (balance: number) => { 
     this.balanceFree = balance;
    })
  }
  async addTFT() {
    if (config.network !== "dev" && config.network !== "qa") {
      window.open(
        "https://gettft.com/auth/login?next_url=/gettft/shop/#/buy",
        "_blank"
      );
    } else {
      this.loadingAddTFT = true;
      getMoreFunds(
        this.$route.params.accountID,
        this.$api,
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
              this.$toasted.show("Get more TFT failed!");
              this.loadingAddTFT = false;
            } else {
              // Loop through Vec<EventRecord> to display all events
              events.forEach(({ phase, event: { data, method, section } }) => {
                console.log(`\t' ${phase}: ${section}.${method}:: ${data}`);
                if (section === "balances" && method === "Transfer") {
                  this.$toasted.show("Success!");
                  this.loadingAddTFT = false;
                  getBalance(this.$api, this.$route.params.accountID).then(
                    (balance) => {
                      this.$emit("update:balanceFree", balance.free);
                      this.$emit("update:balanceReserved", balance.reserved);
                    }
                  );
                } else if (
                  section === "system" &&
                  method === "ExtrinsicFailed"
                ) {
                  this.$toasted.show("Get more TFT failed!");
                  this.loadingAddTFT = false;
                }
              });
            }
          }
        }
      ).catch((err: { message: string }) => {
        console.log(err.message);
        this.loadingAddTFT = false;
        this.$toasted.show("Get more TFT failed!");
      });
    }
  }
}
</script>
<style scoped>
.fund {
  background-color: transparent;
  box-shadow: none !important;
  position: fixed;
  top: 7px;
  right: 8.5%;
  z-index: 1000;
}
</style>