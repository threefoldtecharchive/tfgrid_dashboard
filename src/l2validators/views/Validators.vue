<template>
  <div>
    <v-card>
      <v-card-title>my little pony</v-card-title>
    </v-card>
  </div>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { getValidatorApplications } from "../lib/validators";
@Component({
  name: "ValidatorsView",
})
export default class ValidatorsView extends Vue {
  validatorApplications: any;
  async mounted() {
    this.validatorApplications = await getValidatorApplications();
    console.log(this.validatorApplications);
  }
}
</script>