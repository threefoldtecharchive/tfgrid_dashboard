<template>
  <v-container>
    <router-view style="padding: 6% 5% 5% 10%; margin: 4% 0" />
  </v-container>
</template>
<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";

@Component({
  name: "PortalView",
})
export default class PortalView extends Vue {
  @Watch("$store.state.credentials.twin.id") async onPropertyChanged() {
    if (!this.$store.state.credentials.twin.id) return;
    console.log(`logged in,`, this.$store.state.credentials.twin.id);
    await this.$store.dispatch("portal/getProposal", this.$store.state.credentials.twin.id);
    console.log(this.$store.state.portal.proposals);
  }
}
</script>
