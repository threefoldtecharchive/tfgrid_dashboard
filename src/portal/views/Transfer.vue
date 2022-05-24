<template>
  <v-container>
    <v-container v-if="openDepositDialog">
      <v-dialog
        transition="dialog-bottom-transition"
        max-width="900"
        v-model="openDepositDialog"
      >

        <v-card>
          <v-toolbar
            color="primary"
            dark
          >Deposit TFT</v-toolbar>
          <v-card-text>
            <v-container>

              <v-row>
                <v-col>
                  Send a {{items.filter(item => item.id ===selectedItem.item_id)[0].name}} transaction with your TFT's to deposit to:
                  <ul>
                    <li>Destination: <b>{{ depositWallet }}</b></li>
                    <li>Memo Text: <b>twin_{{id}}</b></li>
                  </ul>
                </v-col>
                <v-divider
                  class="mx-4"
                  vertical
                ></v-divider>
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
              <v-row class="d-flex row justify-center">Amount: should be larger than {{depositFee}}TFT
                (deposit fee is: {{depositFee}}TFT)</v-row>
            </v-container>
          </v-card-text>
          <v-card-actions class="justify-end">
            <v-btn @click="openDepositDialog = false">Close</v-btn>
          </v-card-actions>
        </v-card>

      </v-dialog>
    </v-container>
    <v-card
      color="#388E3C"
      class="pa-5 my-5"
    >
      <h3 class="text-center">We use bridges for transfer to and from the following:</h3>

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
        color="#512DA8"
        class="mx-5 pa-5"
        @click="openDepositDialog = true"
      >deposit</v-btn>

      <v-btn
        color="#303F9F"
        class="mx-5 pa-5"
      >withdraw</v-btn>
    </v-container>
    <v-container class="d-flex justify-center pa-5 my-3">
      <v-btn
        :target="'blank'"
        :href="'https://library.threefold.me/info/manual/#/manual__tfchain_portal_home?id=transfer-tft'"
      >why do we use bridges?</v-btn>
    </v-container>

  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import config from "../config";
import { getDepositFee } from "../lib/transfer";
import QrcodeVue from "qrcode.vue";
@Component({
  name: "TransferView",
  components: { QrcodeVue },
})
export default class TransferView extends Vue {
  openDepositDialog = false;
  selectedItem = {
    item_id: 1,
  };

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
  value = "";
  async mounted() {
    this.address = this.$route.params.accountID;
    if (this.$route.query.twinIP && this.$route.query.twinID) {
      this.ip = this.$route.query.twinIP;
      this.id = this.$route.query.twinID;
      this.accountName = this.$route.query.accountName;
    }
    this.balance = this.$route.query.balance;
    this.depositWallet = config.bridgeTftAddress;
    this.depositFee = await getDepositFee(this.$api);
    this.qrCodeText = `TFT:${this.depositWallet}?message=twin_${this.id}&sender=me`;
  }
  async updated() {
    this.id = this.$route.query.twinID;
    this.ip = this.$route.query.twinID;
    if (this.$route.query.balance !== this.balance) {
      this.balance = this.$route.query.balance;
    }
    console.log(this.selectedItem.item_id);
  }
  unmounted() {
    this.balance = 0;
    this.address = "";
  }
}
</script>