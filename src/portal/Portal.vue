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
export default class PortalView extends Vue {}
</script>