<template>
  <v-container style="padding-top: 100px; padding-bottom: 100px">
    <v-row justify="end" style="color: #333">
      <tf-profiles></tf-profiles>
    </v-row>

    <p v-html="getHtml()" />
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

interface IDeployment {
  symbol: string;
  deployment: string;
}

@Component({
  name: "Playground",
})
export default class Playground extends Vue {
  elements = new Map<string, IDeployment>([
    ["full-vm", { symbol: "fullvm", deployment: "fullvm" }],
    ["vm", { symbol: "vm", deployment: "vm" }],
    ["kubernetes", { symbol: "kubernetes", deployment: "k8s" }],
    ["capRover", { symbol: "caprover", deployment: "caprover" }],
    ["peertube", { symbol: "peertube", deployment: "peertube" }],
    ["funkwhale", { symbol: "funkwhale", deployment: "funkwhale" }],
    ["mattermost", { symbol: "mattermost", deployment: "mattermost" }],
    ["discourse", { symbol: "discourse", deployment: "discourse" }],
    ["taiga", { symbol: "taiga", deployment: "taiga" }],
    ["owncloud", { symbol: "owncloud", deployment: "owncloud" }],
    ["presearch", { symbol: "presearch", deployment: "presearch" }],
    ["casperlabs", { symbol: "casperlabs", deployment: "casperlabs" }],
    ["nodepilot", { symbol: "nodepilot", deployment: "nodepilot" }],
  ]);

  getHtml() {
    const deployment = this.elements.get(this.$route.params.name);
    if (!deployment) return "";
    return `
      <tf-${deployment.symbol}></tf-${deployment.symbol}>
      <tf-deployedlist tab="${deployment.deployment}"></tf-deployedlist>
    `;
  }
}
</script>
