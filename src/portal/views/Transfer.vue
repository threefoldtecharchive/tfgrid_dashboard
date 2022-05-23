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
    console.log(this.selectedItem);
    this.balance = this.$route.query.balance;
  }
}
</script>