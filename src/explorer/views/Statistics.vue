<template>
  <Layout pageName="Statistics" v-if="stats" :noFilter="true">
    <v-container>
      <section class="items" v-if="statistics.length > 0">
        <div v-for="item of statistics" :key="item.title">
          <StatisticsCard :item="item" />
        </div>
      </section>

      <section class="loader" v-if="statistics.length === 0">
        <v-progress-circular size="150" indeterminate />
      </section>

      <v-divider class="mt-2 mb-2" />

      <h2>Nodes Distribution</h2>
      <tf-map :nodes="nodesDistribution"></tf-map>
    </v-container>
  </Layout>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { req } from "../plugins/axios";
import toTeraOrGigaOrPeta from "../filters/toTeraOrGigaOrPeta";

import Layout from "../components/Layout.vue";
import StatisticsCard from "../components/StatisticsCard.vue";

interface Stats {
  nodes: number;
  farms: number;
  countries: number;
  totalCru: number;
  totalSru: number;
  totalMru: number;
  totalHru: number;
  publicIps: number;
  accessNodes: number;
  gateways: number;
  twins: number;
  contracts: number;
  nodesDistribution: { [key: string]: number };
}

interface IStatistics {
  data: number | string;
  title: string;
  icon: string;
}

@Component({
  name: "Statistics",
  components: {
    Layout,
    StatisticsCard,
  },
})
export default class Statistics extends Vue {
  loading = true;
  stats: Stats | null = null;

  get statistics(): IStatistics[] {
    const { loading, stats } = this;
    if (loading || !stats) return [];

    // prettier-ignore
    return [
      { data: stats.nodes, title: "Nodes Online", icon: "mdi-laptop" },
      { data: stats.farms, title: "Farms", icon: "mdi-tractor" },
      { data: stats.countries, title: "Countries", icon: "mdi-earth" },
      { data: stats.totalCru, title: "CPUs Online", icon: "mdi-cpu-64-bit" },
      { data: toTeraOrGigaOrPeta(stats.totalSru.toString()), title: "SSD Storage", icon: "mdi-nas" },
      { data: toTeraOrGigaOrPeta(stats.totalHru.toString()), title: "HDD Storage", icon: "mdi-harddisk" },
      { data: toTeraOrGigaOrPeta(stats.totalMru.toString()), title: "RAM Online", icon: "mdi-memory" },
      { data: stats.accessNodes, title: "Access Nodes", icon: "mdi-gate" },
      { data: stats.gateways, title: "Gateways Online", icon: "mdi-boom-gate-outline" },
      { data: stats.twins, title: "Twins", icon: "mdi-brain" },
      { data: stats.publicIps, title: "Public IPs", icon: "mdi-access-point" },
      { data: stats.contracts, title: "Contracts", icon: "mdi-file-document-edit-outline" },
    ];
  }

  get nodesDistribution(): string {
    const { loading, stats } = this;
    if (loading || !stats) return "{}";

    return JSON.stringify(stats.nodesDistribution);
  }

  created() {
    req
      .get("/stats")
      .then(({ data }) => (this.stats = data))
      .catch(console.log)
      .finally(() => (this.loading = false));
  }
}
</script>

<style lang="scss" scoped>
.items {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  > div {
    padding: 15px;
    width: 16.5%;

    @media (max-width: 1910px) {
      width: calc(100% / 3);
    }

    @media (max-width: 1270px) {
      width: 50%;
    }

    @media (max-width: 800px) {
      width: 100%;
    }
  }
}
</style>
