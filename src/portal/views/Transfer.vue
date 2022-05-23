<template>
  <v-container>
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
      >deposit</v-btn>

      <v-btn
        color="#303F9F"
        class="mx-5 pa-5"
      >withdraw</v-btn>
    </v-container>
    <v-container class="d-flex justify-center pa-5 my-3">
      <v-btn>why do we use bridges?</v-btn>
    </v-container>

    <FundsCard :balance="balance" />
  </v-container>
</template>

<script lang="ts">
import FundsCard from "@/components/FundsCard.vue";
import { Component, Vue } from "vue-property-decorator";
import { getBalance } from "../lib/balance";

@Component({
  name: "TransferView",
  components: { FundsCard },
})
export default class TransferView extends Vue {
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
  async mounted() {
    this.address = this.$route.params.accountID;
    this.balance = (await getBalance(this.$api, this.address)) / 1e7;
  }
  updated() {
    console.log(this.selectedItem.item_id);
    this.balance = this.$route.query.balance;
  }
}
</script>