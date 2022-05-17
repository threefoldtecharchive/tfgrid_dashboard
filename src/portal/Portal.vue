<template>

  <v-container>
    <router-view />
  </v-container>

</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({
  name: "PortalView",
})
export default class PortalView extends Vue {
  public mounted() {
    setInterval(() => {
      this.$store.dispatch("portal/getAccounts");
    }, 1000);
  }
}
</script>