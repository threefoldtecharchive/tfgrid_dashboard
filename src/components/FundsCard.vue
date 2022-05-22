<template>
  <v-card
    color="#0D47A1"
    class="mx-3  pa-2 d-flex align-baseline font-weight-bold"
    v-if="$route.params.accountID"
  > {{  balance.toFixed(2) }} TFT
    <v-btn
      @click="addTFT"
      class="ml-3"
    >+</v-btn>
  </v-card>
</template>
<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
@Component({
  name: "FundsCard",
})
export default class FundsCard extends Vue {
  @Prop({ required: true }) balance!: number;

  public addTFT() {
    console.log("adding tfts");
  }
}
</script>
