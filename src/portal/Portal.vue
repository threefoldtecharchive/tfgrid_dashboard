<template>
  <v-container>
    <FundsCard
      v-if="$route.path !='/' && $route.query.balance"
      :balance.sync='balance'
      @update:balance="$route.query.balance=$event"
    />

    <router-view style="padding: 6% 5% 5% 10%; margin: 4% 0" />
  </v-container>
</template>
<script lang="ts">
import FundsCard from "@/components/FundsCard.vue";
import { Component, Vue, Watch } from "vue-property-decorator";

@Component({
  name: "PortalView",
  components: { FundsCard },
})
export default class PortalView extends Vue {
  balance: any = 0;
  $api: any;
  @Watch("this.$route.query.balance") async onBalanceUpdate(
    value: number,
    oldValue: number
  ) {
    this.balance = this.$route.query.balance;
    console.log(`balance went from ${oldValue}, to ${value}`);
  }
  mounted() {
    this.$store.dispatch("portal/subscribeAccounts");
    this.balance = this.$route.query.balance;
  }
  updated() {
    this.balance = this.$route.query.balance;
  }

  unmounted() {
    this.$store.dispatch("portal/unsubscribeAccounts");
  }
}
</script>
<style scoped>
</style>
