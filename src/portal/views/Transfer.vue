<template>
  <v-container>

    <v-container>
      <v-card
        color="#388E3C"
        class="pa-5 my-5"
      >
        <h3 class="text-center">You can also transfer from one account to another on the TFCHAIN:</h3>

      </v-card>
      <v-card class="pa-5 my-5">

        <v-autocomplete
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
        ></v-autocomplete>
      </v-card>
    </v-container>

  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { checkAddress } from "../lib/transfer";
import QrcodeVue from "qrcode.vue";
import { accountInterface } from "../store/state";
@Component({
  name: "TransferView",
  components: { QrcodeVue },
})
export default class TransferView extends Vue {
  receipientAddress = "";
  accountsAddresses: any = [];

  addressErrorMessages = "";

  balance: any = 0;
  $api: any;
  address = "";
  ip: any = [];
  accountName: any;
  id: any = [];

  amount = 0;
  target = "";

  mounted() {
    this.address = this.$route.params.accountID;
    if (this.$route !== undefined) {
      this.ip = this.$route.query.twinIP;
      this.id = this.$route.query.twinID;
      this.accountName = this.$route.query.accountName;
    }
    this.balance = this.$route.query.balance;

    this.accountsAddresses = this.$store.state.portal.accounts
      .filter((account: accountInterface) => account.address !== this.address)
      .map(
        (account: accountInterface) =>
          `${account.meta.name}: ${account.address}`
      );
    console.log(this.accountsAddresses);
  }
  async updated() {
    this.id = this.$route.query.twinID;
    this.ip = this.$route.query.twinIP;
    if (this.$route.query.balance !== this.balance) {
      this.balance = this.$route.query.balance;
    }

    this.target;
    this.amount;
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
      this.addressErrorMessages = "incorrect format";
      return false;
    }
  }
}
</script>