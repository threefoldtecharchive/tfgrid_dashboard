<template>
  <v-card
    color="#0D47A1"
    class=" funds px-3 d-flex align-baseline font-weight-bold"
  > {{$store.state.portal.currentAccountBalance }} TFT
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
  @Prop({ required: true }) api!: any;
  address = "";
  balance = 0;
  balanceInUSD = 0;

  async updated() {
    this.address = this.$route.params.accountID;
    this.balance = (await getBalance(this.api, this.address)) / 1e7;
    this.$store.dispatch("portal/setBalanceAction", this.balance);
    this.$store.dispatch("portal/setCurrentAccountIDAction", this.address);
    if (config.network !== "dev") {
      const res = await axios.get(
        "https://min-api.cryptocompare.com/data/price?fsym=3ft&tsyms=USD"
      );
      this.balanceInUSD = res.data.USD * this.balance;
      //don't forget to display this
    }
  }

  public async addTFT() {
    if (config.network !== "dev") {
      //redirect to https://gettft.com/auth/login?next_url=/gettft/shop/#/buy
    } else {
      getMoreFunds(
        this.address,
        this.api,
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

                getBalance(this.api, this.address).then((balance) => {
                  this.balance = (this.balance + balance) / 1e7;
                  this.$store.dispatch("portal/setBalanceAction", this.balance);
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
