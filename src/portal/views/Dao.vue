<template>
  <v-container fluid>
    <v-card
      class="my-3 pa-3 d-flex justify-center"
      color="#512DA8"
    >
      <h2> Howdy {{$route.query.accountName}}, you can now vote on proposals!</h2>
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-icon
            dark
            right
            v-bind="attrs"
            v-on="on"
            @click="openInfoModal = true"
          >
            mdi-information-outline
          </v-icon>
        </template>
        <span>
          Click for more info
        </span>
      </v-tooltip>
    </v-card>
    <v-container v-if="proposals.length === 0">
      <v-card class="my-3 pa-3 d-flex justify-center">
        <h3>No Active proposals at this time</h3>
      </v-card>
    </v-container>
    <v-container v-else>
      <v-card
        v-for="proposal in proposals"
        :key="proposal.hash"
      >
        <v-title>
          {{proposal.hash}}
        </v-title>
        <v-text>
          {{proposals.description}}
        </v-text>
      </v-card>

    </v-container>

  </v-container>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { getProposals } from "../lib/dao";

@Component({
  name: "Dao",
})
export default class DaoView extends Vue {
  openInfoModal = false;
  proposals: any = [];
  $api: any;

  async mounted() {
    if (this.$api) {
      this.proposals = await getProposals(this.$api);
    }
  }
}
</script>
