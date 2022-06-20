<template>
  <v-card
    color="#0D47A1"
    class="fund px-3 d-flex align-baseline font-weight-bold"
  > {{balance }} TFT
    <v-btn
      @click="addTFT()"
      class="ml-3"
      :loading="loadingAddTFT"
    >+</v-btn>

  </v-card>
</template>
<script lang="ts">
import config from "@/portal/config";
import { getBalance, getMoreFunds } from "@/portal/lib/balance";
import { Component, Emit, Prop, Vue } from "vue-property-decorator";

@Component({
  name: "FundsCard",
})
export default class FundsCard extends Vue {
  address = "";
  loadingAddTFT = false;
  $api: any;
  @Prop({ required: true }) balance!: number;

  async addTFT() {
    if (config.network !== "dev") {
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

            // Loop through Vec<EventRecord> to display all events
            events.forEach(({ phase, event: { data, method, section } }) => {
              console.log(`\t' ${phase}: ${section}.${method}:: ${data}`);
              if (section === "balances" && method === "Transfer") {
                this.$toasted.show("Success!");
                getBalance(this.$api, this.$route.params.accountID).then(
                  (balance: number) => {
                    this.$emit("update:balance", balance / 1e7);
                  }
                );
                this.loadingAddTFT = false;
              } else if (section === "system" && method === "ExtrinsicFailed") {
                this.$toasted.show("Get more TFT failed!");
                this.loadingAddTFT = false;
              }
            });
          }
        }
      ).catch((err: { message: string }) => {
        console.log(err.message);
      });
    }
  }
}
</script>
<style scoped>
.fund {
  position: fixed;
  top: 14%;
  right: 0;
}
</style>