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

    <v-container v-if="proposals.length">
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
              @click="openVoteDialog(proposal.hash, true)"
              :loading="loadingVote"
            >Yes <br>{{ proposal.ayes.length}}</v-btn>
            <v-btn
              color="red"
              class=" mx-5"
              style="padding:2.5% 5%"
              @click="openVoteDialog(proposal.hash, false)"
              :loading="loadingVote"
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

      <v-dialog
        v-model="openVDialog"
        max-width="600"
      >
        <v-card>
          <v-card-title>Cast Vote</v-card-title>
          <v-card-text>
            <v-select
              :items="farms"
              label="Select a farm"
              outlined
              item-text="name"
              item-value="id"
              v-model="selectedFarm"
            >
            </v-select>
          </v-card-text>
          <v-card-actions class="justify-end">
            <v-btn
              @click="castVote"
              :loading="loadingVote"
            >Submit</v-btn>
            <v-btn @click="openVDialog = false">Close</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

    </v-container>

    <v-container v-else>
      <v-card class="my-3 pa-3 d-flex justify-center">
        <h3>No Active proposals at this time</h3>
      </v-card>
    </v-container>

  </v-container>
</template>
<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import { getProposals, vote } from "../lib/dao";
import { getFarm, getNodesByFarm } from "../lib/farms";

@Component({
  name: "Dao",
})
export default class DaoView extends Vue {
  openInfoModal = false;
  proposals: any = [];
  $api: any;
  balance: any = 0;
  percentageVoted = 0;
  openVDialog = false;
  id: any = [];
  selectedFarm: any = [];
  farms: any = [];
  vote = false;
  loadingVote = false;
  selectedProposal: any = "";

  async mounted() {
    if (this.$api) {
      this.balance = this.$route.query.balance;
      this.id = this.$route.query.twinID;
      this.proposals = await getProposals(this.$api);
      this.farms = await getFarm(this.$api, this.id);
    } else {
      this.$router.push({
        name: "accounts",
        path: "/",
      });
    }
  }
  @Watch("proposals") async onProposalUpdate(value: any, oldValue: any) {
    console.log(
      `there were ${oldValue.length} proposals, now there is ${value.length} proposals`
    );
  }
  async updated() {
    this.balance = this.$route.query.balance;

    this.id = this.$route.query.twinID;
  }
  openVoteDialog(hash: any, vote: boolean) {
    this.openVDialog = true;
    this.vote = vote;
    this.selectedProposal = hash;
  }
  async castVote() {
    const nodes = await getNodesByFarm(this.selectedFarm);

    if (nodes.length === 0) {
      alert("no nodes in farm");
      return;
    }
    this.loadingVote = true;
    vote(
      this.$route.params.accountID,
      this.$api,
      this.selectedFarm,
      this.selectedProposal,
      this.vote,
      (res: { events?: never[] | undefined; status: any }) => {
        console.log(res);
        if (res instanceof Error) {
          console.log(res);
          return;
        }

        const { events = [], status } = res;
        console.log(`Current status is ${status.type}`);
        switch (status.type) {
          case "Ready":
            this.$toasted.show(`Transaction submitted`);
        }

        if (status.isFinalized) {
          console.log(
            `Transaction included at blockHash ${status.asFinalized}`
          );

          // Loop through Vec<EventRecord> to display all events
          events.forEach(({ phase, event: { data, method, section } }) => {
            console.log(`\t' ${phase}: ${section}.${method}:: ${data}`);
            if (section === "dao" && method === "Voted") {
              this.$toasted.show("Voted for proposal!");
              this.loadingVote = false;
              this.openVDialog = false;
              getProposals(this.$api).then(
                (proposals) => (this.proposals = proposals)
              );
            } else if (section === "system" && method === "ExtrinsicFailed") {
              this.$toasted.show("Vote failed");
              this.loadingVote = false;
              this.openVDialog = false;
            }
          });
        }
      }
    ).catch((err) => {
      this.$toasted.show(err.message);
      this.loadingVote = false;
      this.openVDialog = false;
    });
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
