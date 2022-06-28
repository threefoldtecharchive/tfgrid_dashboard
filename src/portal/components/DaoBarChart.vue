<template>
  <Bar
    :chart-options="chartOptions"
    :chart-data="chartData"
    :width="width"
    :height="height"
  />
</template>
<script lang="ts">
import { Bar } from "vue-chartjs/legacy";
import Vue from "vue";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
);
export default Vue.extend({
  name: "DaoBarChart",
  components: { Bar },
  props: {},
  data() {
    return {
      chartData: {
        labels: ["Yes", "No"],
        datasets: [{ data: [40, 20] }],
      },
      chartOptions: {
        responsive: true,
      },
    };
  },
});
</script>
