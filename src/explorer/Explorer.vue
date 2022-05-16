<template>
  <v-container>
    <router-view />
    {{ $store.state.explorer.name }}
  </v-container>
</template>

<script>
import { Component, Vue } from "vue-property-decorator";

@Component({
  name: "ExplorerView",
})
export default class ExplorerView extends Vue {}
</script>
