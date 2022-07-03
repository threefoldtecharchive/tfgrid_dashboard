<template>
  <v-container fluid>
    <v-card
      class="my-3 pa-3 d-flex justify-center"
      color="primary white--text"
    >
      <h2>
        Howdy {{ $route.query.accountName }}, you can now vote on proposals!
      </h2>
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
        <span> Click for more info </span>
      </v-tooltip>
    </v-card>
    <v-container v-if="!proposals.length">
      <v-card class="my-3 pa-3 d-flex justify-center">
        <h3>No Active proposals at this time</h3>
      </v-card>
    </v-container>
    <v-container v-else>
      <v-text-field
        v-model="searchTerm"
        color="primary darken-2"
        label="Search by proposal action or description"
      ></v-text-field>

      <v-card
        class="my-3 pa-3"
        v-for="(proposal, i) in filteredProposals()"
        :key="i"
      >
        <v-card-title>
          {{ proposal.action.toUpperCase() }}
        </v-card-title>
        <v-card-subtitle>
          {{ proposal.hash }}
        </v-card-subtitle>
        <v-card-text>
          {{ proposal.description }}
          <a
            v-bind:href="proposal.link"
            v-bind:target="'blank'"
          >More details</a>
        </v-card-text>

        <v-container
          fluid
          class="d-flex justify-space-between my-5"
        >
          <v-btn
            color="primary"
            @click="openVoteDialog(proposal.hash, true)"
            :loading="loadingVote"
            :width="`${(proposal.ayes.length)/(proposal.ayes.length+ proposal.nayes.length) *100 + 100}`"
          >Yes
            <v-divider
              class="mx-3"
              vertical
            />{{ proposal.ayes.length }}
          </v-btn>

          <div class="d-flex align-center text-center threshold">
            <v-divider vertical />
            <span>Threshold: <br />{{
                proposal.nayes.length + proposal.ayes.length
              }}/{{ proposal.threshold }}
            </span>
            <v-divider vertical />
          </div>
          <v-btn
            color="grey lighten-2 black--text"
            @click="openVoteDialog(proposal.hash, false)"
            :width="`${proposal.nayes.length /(proposal.ayes.length+ proposal.nayes.length) *100 + 100}`"
            :loading="loadingVote"
          >No
            <v-divider
              class="mx-3"
              vertical
            />{{ proposal.nayes.length }}
          </v-btn>
        </v-container>
        <v-container v-if="proposal.ayesProgress > 0 || proposal.nayesProgress > 0">
          <v-row justify="center">
            <v-progress-linear
              :value="proposal.ayesProgress"
              height="25"
              :style="{
                width: proposal.ayesProgress + '%',
                marginRight: 'auto',
                backgroundColor: '#1982b1',
                color: '#fff',
              }"
            >
              <template>
                <strong>{{ proposal.ayesProgress }}%</strong>
              </template>
            </v-progress-linear>
            <v-progress-linear
              :value="proposal.nayesProgress"
              color="grey lighten-2"
              height="25"
              :style="{
                width: proposal.nayesProgress + '%',
                marginRight: 'auto',
                color: '#333',
              }"
            >
              <template>
                <strong>{{ proposal.nayesProgress }}%</strong>
              </template>
            </v-progress-linear>
          </v-row>
        </v-container>

        <p>You can vote until: {{ proposal.end }}</p>
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
              color="primary white--text"
            >Submit</v-btn>
            <v-btn
              @click="openVDialog = false"
              color="grey lighten-2 black--text"
            >Close</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </v-container>
</template>
<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import { ayesAndNayesInterface, getProposals, vote } from "../lib/dao";
import { getFarm, getNodesByFarm } from "../lib/farms";
import DaoBarChart from "../components/DaoBarChart.vue";

interface proposalInterface {
  action: string;
  hash: string;
  description: string;
  link: string;
  ayes: ayesAndNayesInterface[];
  nayes: ayesAndNayesInterface[];
  end: number;
  threshold: number;
  ayesProgress: number;
  nayesProgress: number;
}
@Component({
  name: "Dao",
  components: { DaoBarChart },
})
export default class DaoView extends Vue {
  openInfoModal = false;
  proposals: proposalInterface[] = [];
  $api: any;
  percentageVoted = 0;
  openVDialog = false;
  id: string | (string | null)[] = "";
  selectedFarm = "";
  farms: any[] = [];
  vote = false;
  loadingVote = false;
  selectedProposal = "";
  searchTerm = "";

  async mounted() {
    if (this.$api) {
      this.id = this.$route.query.twinID;
      this.proposals = await getProposals(this.$api);
      console.log(this.proposals);
      this.farms = await getFarm(this.$api, parseFloat(`${this.id}`));
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
    this.id = this.$route.query.twinID;
    if (this.$api) {
      this.id = this.$route.query.twinID;
      this.farms = await getFarm(this.$api, parseFloat(`${this.id}`));
    } else {
      this.$router.push({
        name: "accounts",
        path: "/",
      });
    }
  }
  filteredProposals() {
    if (this.searchTerm.length) {
      return this.proposals.filter(
        (proposal: { action: string; description: string }) =>
          proposal.action
            .toLowerCase()
            .includes(this.searchTerm.toLowerCase()) ||
          proposal.description
            .toLowerCase()
            .includes(this.searchTerm.toLowerCase())
      );
    }
    return this.proposals;
  }

  openVoteDialog(hash: any, vote: boolean) {
    this.openVDialog = true;
    this.vote = vote;
    this.selectedProposal = hash;
  }
  async castVote() {
    const nodes = await getNodesByFarm(this.selectedFarm);
    console.log(this.selectedFarm);
    if (!nodes.length) {
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
          if (!events.length) {
            this.$toasted.show("Vote failed");
            this.loadingVote = false;
            this.openVDialog = false;
          } else {
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
      }
    ).catch((err) => {
      this.$toasted.show(err.message);
      this.loadingVote = false;
      this.openVDialog = false;
    });
  }
}
</script>
<style scoped>
.chart {
  width: 50%;
}
.threshold {
  position: absolute;
  left: 46%;
}
</style>
