<template>
  <v-container>


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

}
</script>
<style scoped>
</style>
