<template>
  <div>

  </div>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({
  name: "NodesTable",
})
export default class NodesTable extends Vue {
  headers = [
    { text: "Node ID", value: "nodeId" },
    { text: "Location", value: "location.country" },
    { text: "CRU", value: "resources.cru" },
    { text: "MRU", value: "resources.mru" },
    { text: "SRU", value: "resources.sru" },
    { text: "HRU", value: "resources.hru" },
    { text: "Price in USD", value: "discount" },
    { text: "Actions", value: "actions" },
  ];
}
</script>
