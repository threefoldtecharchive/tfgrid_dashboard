<template>
  <div>Farms
    Lorem ipsum dolor sit amet consectetur, adipisicing elit. Reiciendis ut consequatur vitae enim ab magnam recusandae, quam necessitatibus amet a nulla similique perferendis officia quidem debitis aperiam dignissimos veritatis explicabo.
    {{$store.state.portal.name}}
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({
  name: "FarmsView",
})
export default class FarmsView extends Vue {}
</script>