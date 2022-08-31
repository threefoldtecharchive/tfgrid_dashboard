<template>
  <div>

    <router-view style="padding: 6% 5% 5% 10%; margin: 4% 0"></router-view>
  </div>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({
  name: "L2ValidatorsView",
})
export default class L2ValidatorsView extends Vue {}
</script>
