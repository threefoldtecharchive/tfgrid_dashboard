<template>
  <v-container>
    <FundsCard
      v-if="$route.path !='/' && $route.query.balanceFree"
      :balanceFree.sync='balanceFree'
      :balanceReserved.sync='balanceReserved'
      @update:balanceFree="$route.query.balanceFree=$event"
      @update:balanceReserved="$route.query.balanceReserved=$event"
    />

    <router-view style="padding: 6% 5% 5% 10%; margin: 4% 0" />
  </v-container>

</template>
<script lang="ts">
import FundsCard from "./components/FundsCard.vue";
import { Component, Vue, Watch } from "vue-property-decorator";

@Component({
  name: "PortalView",
  components: { FundsCard },
})
export default class PortalView extends Vue {
  balanceFree: string | (string | null)[] = "";
  balanceReserved: string | (string | null)[] = "";

  @Watch("this.$route.query.balance") async onBalanceUpdate(
    value: number,
    oldValue: number
  ) {
    this.balanceFree = this.$route.query.balanceFree;
    this.balanceReserved = this.$route.query.balanceReserved;
    console.log(`balance went from ${oldValue}, to ${value}`);
  }
  mounted() {
    this.$store.dispatch("portal/subscribeAccounts");
    this.balanceFree = this.$route.query.balanceFree;
    this.balanceReserved = this.$route.query.balanceReserved;
  }
  updated() {
    this.balanceFree = this.$route.query.balanceFree;
    this.balanceReserved = this.$route.query.balanceReserved;
  }
  unmounted() {
    this.$store.dispatch("portal/unsubscribeAccounts");
  }
}
</script>
<style scoped>
</style>
