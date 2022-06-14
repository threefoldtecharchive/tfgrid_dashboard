<template>
  <v-container>
    <router-view style="padding: 6% 5% 5% 10%; margin: 4% 0" />
  </v-container>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({
  name: "PortalView",
})
export default class PortalView extends Vue {
  async mounted() {
    this.$store.dispatch("portal/subscribeAccounts");
  }

  public unmounted() {
    this.$store.dispatch("portal/unsubscribeAccounts");
  }
}
</script>
