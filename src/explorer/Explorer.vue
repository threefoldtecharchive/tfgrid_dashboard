<template>
  <v-container>
    <router-view />
  </v-container>
</template>

<script>
import { Component, Vue } from "vue-property-decorator";

@Component({
  name: "ExplorerView",
})
export default class ExplorerView extends Vue {}
</script>
