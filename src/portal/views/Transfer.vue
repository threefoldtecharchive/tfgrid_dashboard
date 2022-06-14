<template>
  <v-container>
    <v-container>
      <FundsCard :balance="balance" />
    </v-container>

    <v-card
      color="#388E3C"
      class="pa-5 my-5"
    >
      <h2 class="text-center"> Howdy {{accountName}}, want to transfer TFTs? </h2>
    </v-card>

    <v-card
      color="#388E3C"
      class="pa-5 my-5"
    >
      <h3 class="text-center">You can also transfer from one account to another on the TFCHAIN:</h3>

    </v-card>
    <v-card class="pa-5 my-5">

      <v-combobox
        v-model="receipientAddress"
        :items="accountsAddresses"
        dense
        filled
        label="Receipient:"
        :error-messages="addressErrorMessages"
        :rules="[
            () => !!receipientAddress || 'This field is required',
            addressCheck()
          ]"
      ></v-combobox>
      <v-text-field
        v-model="amount"
        label="Amount (TFT)"
        type="number"
        :rules="[
            () => !!amount || 'This field is required',
            () => amount < balance || 'Amount cannot exceed balance',
          ]"
      >

      </v-text-field>
      <v-card-actions>
        <v-spacer>
        </v-spacer>
        <v-btn @click="clearInput">Clear</v-btn>
        <v-btn
          @click="transferTFT"
          :loading="loadingTransfer"
        >Submit</v-btn>
      </v-card-actions>

    </v-card>
  </v-container>

</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { checkAddress, transfer } from "../lib/transfer";
import QrcodeVue from "qrcode.vue";
import { accountInterface } from "../store/state";
import FundsCard from "@/components/FundsCard.vue";

@Component({
  name: "TransferView",
  components: { QrcodeVue, FundsCard },
})
export default class TransferView extends Vue {
  receipientAddress = "";
  accountsAddresses: any = [];
  addressErrorMessages = "";
  balance: any = 0;
  $api: any;
  address = "";
  ip: any = [];
  accountName: any = "";
  id: any = [];
  amount = 0;
  loadingTransfer = false;

  mounted() {
    if (this.$api) {
      this.address = this.$route.params.accountID;
      if (this.$route !== undefined) {
        this.ip = this.$route.query.twinIP;
        this.id = this.$route.query.twinID;
        this.accountName = this.$route.query.accountName;
      }
      this.balance = +this.$route.query.balance;

      this.accountsAddresses = this.$store.state.portal.accounts
        .filter((account: accountInterface) => account.address !== this.address)
        .map((account: accountInterface) => `${account.address}`);
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
      this.balance = +this.$route.query.balance;
    }
  }

  unmounted() {
    this.balance = 0;
    this.address = "";
  }
  addressCheck() {
    const isValid = checkAddress(this.receipientAddress);
    if (isValid) {
      this.addressErrorMessages = "";
      return true;
    } else {
      this.addressErrorMessages = "invalid address";
      return false;
    }
  }
  clearInput() {
    this.receipientAddress = "";
    this.amount = 0;
  }
  transferTFT() {
    if (this.amount === 0 || this.receipientAddress === "") {
      this.addressErrorMessages = "No target specified";
      return;
    }
    transfer(
      this.address,
      this.$api,
      this.receipientAddress,
      this.amount,
      (res: {
        events?: never[] | undefined;
        status: { type: string; asFinalized: string; isFinalized: string };
      }) => {
        this.loadingTransfer = true;
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
              this.$toasted.show("Transfer succeeded!");
              this.loadingTransfer = false;
            } else if (section === "system" && method === "ExtrinsicFailed") {
              this.$toasted.show("Transfer failed!");
              this.loadingTransfer = false;
            }
          });
        }
      }
    ).catch((err) => {
      this.$toasted.show(err.message);
      this.loadingTransfer = false;
    });
  }
}
</script>