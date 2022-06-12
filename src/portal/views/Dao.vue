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

    <v-container v-if="proposals.length > 0">
      <v-card
        class="my-3 pa-3"
        v-for="(proposal,i) in proposals"
        :key="i"
      >
        <v-card-title>
          {{proposal.action.toUpperCase()}}
        </v-card-title>
        <v-card-subtitle>
          {{proposal.hash}}
        </v-card-subtitle>
        <v-card-text>
          {{proposal.description}}
          <a
            v-bind:href="proposal.link"
            v-bind:target="'blank'"
          >More details</a>

        </v-card-text>

        <v-container>
          <div class="d-flex justify-center py-5 ">
            <v-btn
              color="green"
              class="mx-5 "
              style="padding:2.5% 5%"
            >Yes <br>{{ proposal.ayes.length}}</v-btn>
            <v-btn
              color="red"
              class=" mx-5"
              style="padding:2.5% 5%"
            >No <br>{{proposal.nayes.length}}</v-btn>
          </div>
          <div>
            <v-progress-linear
              height="25"
              v-bind:value="getProgress(proposal.hash)"
            >
              <strong>{{ getProgress(proposal.hash)  }}%</strong>
            </v-progress-linear>
            <p>You can vote until: {{proposal.end}}</p>
          </div>

        </v-container>

      </v-card>

    </v-container>

    <v-container v-else>
      <v-card class="my-3 pa-3 d-flex justify-center">
        <h3>No Active proposals at this time</h3>
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

  percentageVoted = 0;
  async mounted() {
    if (this.$api) {
      this.proposals = await getProposals(this.$api);
    }
  }
  getProgress(hash: any) {
    const proposal = this.proposals.filter(
      (p: { hash: any }) => p.hash === hash
    )[0];

    const totalAyeWeight = proposal.ayes.reduce(
      (total: number, v: { weight: number }) => total + v.weight,
      0
    );
    const totalNayeWeight = proposal.nayes.reduce(
      (total: number, v: { weight: number }) => total + v.weight,
      0
    );

    const total = totalAyeWeight + totalNayeWeight;
    if (total > 0) {
      return (totalAyeWeight / total) * 100;
    }
    return 0;
  }
}
</script>
