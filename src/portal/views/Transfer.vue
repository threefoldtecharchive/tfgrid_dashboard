<template>
  <v-container>

    <v-card
      color="primary"
      class="white--text pa-5 my-5"
    >
      <h3 class="text-center">
        Transfer TFTs on the TFChain
      </h3>
    </v-card>
    <v-card class="pa-5 my-5">
      <v-form v-model="isTransferValid">
        <v-combobox
          v-model="receipientAddress"
          :items="accountsAddresses"
          dense
          filled
          label="Receipient:"
          :rules="[
          () => !!receipientAddress || 'This field is required',
          () => transferAddressCheck() || 'invalid address',
        ]"
        ></v-combobox>
        <v-text-field
          v-model="amount"
          label="Amount (TFT)"
          type="number"
          onkeydown="javascript: return event.keyCode == 69 || /^\+$/.test(event.key) ? false : true" 
          :rules="[
          () => !!amount || 'This field is required',
          () => amount.toString().split('.')[1].length <= 3 || 'Amount must have 3 decimals only',
          () => amount > 0 || 'Amount cannot be negative or 0',
          () => amount < parseFloat(balance) || 'Amount cannot exceed balance',
        ]"
        >
        </v-text-field>
      </v-form>
      <v-card-actions>
        <v-spacer> </v-spacer>
        <v-btn
          @click="clearInput"
          color="grey lighten-2 black--text"
        >Clear</v-btn>
        <v-btn
          class="primary white--text"
          @click="transferTFT"
          :loading="loadingTransfer"
          :disabled="!isTransferValid"
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
import { balanceInterface, getBalance } from "../lib/balance";
@Component({
  name: "TransferView",
  components: { QrcodeVue },
})
export default class TransferView extends Vue {
  receipientAddress = "";
  accountsAddresses: any = [];
  balance: any = 0;
  $api: any;
  address = "";
  ip: any = [];
  accountName: any = "";
  id: any = [];
  amount = 0;
  loadingTransfer = false;
  isTransferValid = false;
  mounted() {
    if (this.$api) {
      this.address = this.$route.params.accountID;
      if (this.$route !== undefined) {
        this.ip = this.$route.query.twinIP;
        this.id = this.$route.query.twinID;
        this.accountName = this.$route.query.accountName;
      }
      this.balance = +this.$route.query.balanceFree;
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
    if (this.$route.query.balanceFree !== this.balance) {
      this.balance = +this.$route.query.balanceFree;
    }
  }
  unmounted() {
    this.balance = 0;
    this.address = "";
  }
  transferAddressCheck() {
    const isValid = checkAddress(this.receipientAddress);
    if (
      isValid &&
      this.receipientAddress.length &&
      !this.receipientAddress.match(/\W/)
    ) {
      return true;
    } else {
      return false;
    }
  }
  clearInput() {
    this.receipientAddress = "";
    this.amount = 0;
  }
  transferTFT() {
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
          if (!events.length) {
            this.$toasted.show("Transfer failed!");
            this.loadingTransfer = false;
          } else {
            // Loop through Vec<EventRecord> to display all events
            events.forEach(({ phase, event: { data, method, section } }) => {
              console.log(`\t' ${phase}: ${section}.${method}:: ${data}`);
              if (section === "balances" && method === "Transfer") {
                this.$toasted.show("Transfer succeeded!");
                this.loadingTransfer = false;
                getBalance(this.$api, this.address).then(
                  (balance: balanceInterface) => {
                    this.balance = balance.free;
                    this.$root.$emit('updateBalance', this.balance);
                  }
                );
              } else if (section === "system" && method === "ExtrinsicFailed") {
                this.$toasted.show("Transfer failed!");
                this.loadingTransfer = false;
              }
            });
          }
        }
      }
    ).catch((err) => {
      this.$toasted.show(err.message);
      this.loadingTransfer = false;
    });
  }
}
</script>

<style scoped>
.theme--dark.v-application a {
  color: white;
}
</style>