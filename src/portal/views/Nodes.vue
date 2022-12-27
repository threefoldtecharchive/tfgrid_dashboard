<template>
  <v-container>
    <v-card>
      <v-tabs v-model="activeTab" background-color="deep-blue accent-4" centered dark @change="onTabChange()">
        <v-tab v-for="tab in tabs" :key="tab.index" :value="tab.query" :href="'#' + tab.query">
          {{ tab.label }}
        </v-tab>
      </v-tabs>

      <v-tabs-items v-model="activeTab">
        <v-tab-item v-for="tab in tabs" :key="tab.index" :value="tab.query">
          <NodesTable :tab="tab" :twinId="$route.query.twinID" :trigger="trigger" />
        </v-tab-item>
      </v-tabs-items>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import NodesTable from "../components/NodesTable.vue";
import { Component, Vue } from "vue-property-decorator";
import { ITab } from "../lib/nodes";

@Component({
  name: "NodesView",
  components: { NodesTable },
})
export default class NodesView extends Vue {
  $api = "";
  address = "";
  activeTab = "";
  trigger = "";

  tabs: ITab[] = [
    {
      label: "Rentable",
      value: "rentable",
      query: "rentable",
      index: 1,
    },
    {
      label: "Rented",
      value: "rented",
      query: "rented",
      index: 2,
    },
    {
      label: "Mine",
      value: "mine",
      query: "rented_by",
      index: 3,
    },
  ];

  async mounted() {
    this.address = this.$route.params.accountID;

    if (!this.$api) {
      this.$router.push({ name: "accounts", path: "/" });
    }
  }
  updated() {
    this.address;
  }
  onTabChange() {
    this.trigger = Math.random().toString(36).slice(2);
  }
}
</script>
