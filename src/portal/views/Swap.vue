<template>
  <v-container>
    <v-container v-if="openDepositDialog">
      <v-dialog
        transition="dialog-bottom-transition"
        max-width="900"
        v-model="openDepositDialog"
      >
        <v-card>
          <v-toolbar color="primary" dark>Deposit TFT</v-toolbar>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col>
                  Send a {{ selectedName.toUpperCase() }} transaction with your
                  TFT's to deposit to:
                  <ul>
                    <li>
                      Destination: <b>{{ depositWallet }}</b>
                    </li>
                    <li>
                      Memo Text: <b>twin_{{ id }}</b>
                    </li>
                  </ul>
                </v-col>
                <v-divider class="mx-4" vertical></v-divider>
                <v-col>
                  Or use Threefold connect to scan this qr code:
                  <div class="d-flex justify-center">
                    <qrcode-vue
                      :value="qrCodeText"
                      :size="200"
                      level="M"
                      render-as="svg"
                    />
                  </div>
                </v-col>
              </v-row>
              <v-row class="d-flex row justify-center"
                >Amount: should be larger than {{ depositFee }}TFT (deposit fee
                is: {{ depositFee }}TFT)</v-row
              >
            </v-container>
          </v-card-text>
          <v-card-actions class="justify-end">
            <v-btn @click="openDepositDialog = false">Close</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
    <v-container v-if="openWithdrawDialog">
      <v-dialog
        transition="dialog-bottom-transition"
        max-width="900"
        v-model="openWithdrawDialog"
      >
        <v-card>
          <v-toolbar color="primary" dark>Withdraw TFT</v-toolbar>
          <v-card-title>
            Interact with the bridge in order to withdraw your TFT to
            {{ selectedName.toUpperCase() }} (withdraw fee is:
            {{ withdrawFee }} TFT)
          </v-card-title>
          <v-card-text>
            <v-text-field
              v-model="target"
              :label="selectedName.toUpperCase() + ' Target Wallet Address'"
            >
            </v-text-field>
            <v-text-field label="Amount" v-model="amount"></v-text-field>
          </v-card-text>
          <v-card-actions class="justify-end">
            <v-btn @click="openWithdrawDialog = false">Close</v-btn>
            <v-btn
              class="primary white--text"
              @click="withdrawTFT(target, amount)"
              >Submit</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
    <v-card color="primary" class="pa-5 my-5 white--text">
      <h3 class="text-center">
        We use bridges for transfer to and from the following:
      </h3>
    </v-card>
    <v-card class="pa-5 my-5">
      <v-select
        :items="items"
        label="Please select one:"
        v-model="selectedItem.item_id"
        item-text="name"
        item-value="id"
      >
      </v-select>
    </v-card>
    <v-container class="d-flex justify-center pa-5 my-2">
      <v-btn
        color="primary"
        class="white--text mx-5 pa-5"
        @click="openDepositDialog = true"
        >deposit</v-btn
      >

      <v-btn
        color="primary"
        class="mx-5 pa-5 white--text"
        @click="openWithdrawDialog = true"
        >withdraw</v-btn
      >
    </v-container>

    <v-container class="d-flex justify-center pa-5 my-3">
      <a
        color="primary"
        :target="'blank'"
        class="text-decoration-none"
        :href="'https://library.threefold.me/info/manual/#/manual__tfchain_portal_home?id=transfer-tft'"
        >why do we use bridges?</a
      >
    </v-container>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import config from "../config";
import { getDepositFee, getWithdrawFee, withdraw } from "../lib/swap";
import QrcodeVue from "qrcode.vue";
import { getBalance } from "../lib/balance";

@Component({
  name: "TransferView",
  components: { QrcodeVue },
})
export default class TransferView extends Vue {
  openDepositDialog = false;
  openWithdrawDialog = false;

  selectedItem = {
    item_id: 1,
  };
  addressErrorMessages = "";
  selectedName = "";

  items = [
    { id: 1, name: "stellar" },
    {
      id: 2,
      name: "cosmos",
    },
  ];
  balance: any = 0;
  $api: any;
  address = "";
  ip: any = [];
  accountName: any;
  id: any = [];
  depositWallet = "";
  depositFee = 0;
  qrCodeText = "";
  withdrawFee = 0;
  amount = 0;
  target = "";

  mounted() {
    if (this.$api) {
      this.address = this.$route.params.accountID;
      if (this.$route !== undefined) {
        this.ip = this.$route.query.twinIP;
        this.id = this.$route.query.twinID;
        this.accountName = this.$route.query.accountName;
      }
      this.balance = this.$route.query.balance;
      this.depositWallet = config.bridgeTftAddress;

      this.qrCodeText = `TFT:${this.depositWallet}?message=twin_${this.id}&sender=me`;
      this.selectedName = this.items.filter(
        (item) => item.id === this.selectedItem.item_id
      )[0].name;
    } else {
      this.$router.push({
        name: "accounts",
        path: "/",
      });
    }
  }
  async updated() {
    this.id = this.$route.query.twinID;
    this.ip = this.$route.query.twinIP;
    if (this.$route.query.balance !== this.balance) {
      this.balance = this.$route.query.balance;
    }
    this.selectedName = this.items.filter(
      (item) => item.id === this.selectedItem.item_id
    )[0].name;
    this.target;
    this.amount;
    this.depositFee = await getDepositFee(this.$api);
    this.withdrawFee = await getWithdrawFee(this.$api);
  }
  unmounted() {
    this.balance = 0;
    this.address = "";
  }

  public async withdrawTFT(target: string, amount: number) {
    withdraw(
      this.address,
      this.$api,
      target,
      amount,
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
            if (
              section === "tftBridgeModule" &&
              method === "BurnTransactionCreated"
            ) {
              this.$toasted.show("Withdraw sumbitted!");
              this.openWithdrawDialog = false;
              getBalance(this.$api, this.address).then((balance: number) => {
                this.balance = balance / 1e7;
              });
            } else if (section === "system" && method === "ExtrinsicFailed") {
              this.$toasted.show("Withdraw failed!");
            }
          });
        }
      }
    ).catch((err) => {
      console.log(err.message);
    });
  }
}
</script>

<style scoped>
.theme--dark.v-application a {
  color: white;
}
</style>
