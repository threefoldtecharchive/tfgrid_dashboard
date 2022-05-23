<template>
  <v-card
    v-if="currentBalance"
    color="#0D47A1"
    class=" funds px-3 d-flex align-baseline font-weight-bold"
  > {{currentBalance}} TFT
    <v-btn
      @click="addTFT"
      class="ml-3"
    >+</v-btn>
  </v-card>
  <v-card
    v-else-if="$route.path !=='/'"
    color="#0D47A1"
    class=" funds px-3 d-flex align-baseline font-weight-bold"
  > {{balance }} TFT
    <v-btn
      @click="addTFT"
      class="ml-3"
    >+</v-btn>
  </v-card>

</template>
<script lang="ts">
import config from "@/portal/config";
import { getBalance, getMoreFunds } from "@/portal/lib/balance";
import axios from "axios";
import { Component, Prop, Vue } from "vue-property-decorator";
@Component({
  name: "FundsCard",
})
export default class FundsCard extends Vue {
  address = "";
  balanceInUSD = 0;
  $api: any;
  currentBalance: any = 0;
  @Prop({ required: true }) balance!: number;

  async mounted() {
    if (this.$route.path !== "/") {
      this.address = this.$route.params.accountID;
      this.currentBalance = this.balance;
    }

    if (config.network !== "dev") {
      const res = await axios.get(
        "https://min-api.cryptocompare.com/data/price?fsym=3ft&tsyms=USD"
      );
      this.balanceInUSD = res.data.USD * this.currentBalance;
      //don't forget to display this
    }
  }
  unmounted() {
    this.currentBalance = 0;
    this.address = "";
  }

  public async addTFT() {
    if (config.network !== "dev") {
      //redirect to https://gettft.com/auth/login?next_url=/gettft/shop/#/buy
    } else {
      getMoreFunds(
        this.address,
        this.$api,
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
              if (section === "balances" && method === "Transfer") {
                console.log("Success!");

                getBalance(this.$api, this.address).then((balance) => {
                  this.currentBalance = balance / 1e7;
                });
              } else if (section === "system" && method === "ExtrinsicFailed") {
                console.log("Get more TFT failed!");
              }
            });
          }
        }
      ).catch((err: { message: any }) => {
        console.log(err.message);
      });
    }
  }
}
</script>
<style scoped>
.funds {
  position: fixed;
  bottom: 0;
  z-index: 100;
  right: 0;
}
</style>
