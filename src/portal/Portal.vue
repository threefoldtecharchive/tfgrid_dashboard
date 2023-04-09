<template>
  <v-container>
    <router-view style="padding: 6% 5% 5% 10%; margin: 4% 0" />
    <v-dialog v-model="openProposalDialog" persistent max-width="350">
      <template v-slot:default="dialog">
        <v-card>
          <v-toolbar color="primary" dark dense elevation="4" outlined rounded>Vote now!</v-toolbar>
          <div class="d-flex align-center">
            <v-card-text>
              <div class="text-subtitle-1 text-center">{{ voteMsg }}</div>
            </v-card-text>
          </div>
          <v-card-actions class="justify-space-around">
            <v-btn text @click="dialog.value = false">Close</v-btn>
            <v-btn text @click="daoRedirect">Vote</v-btn>
          </v-card-actions>
        </v-card>
      </template>
    </v-dialog>
  </v-container>
</template>
<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";

@Component({
  name: "PortalView",
})
export default class PortalView extends Vue {
  openProposalDialog = false;
  proposals = 0;
  voteMsg = "You have a pending proposal to vote!";
  @Watch("$store.state.credentials.twin.id")
  async getProposals() {
    if (!this.$store.state.credentials.twin.id) return;
    await this.$store.dispatch("portal/getProposal", this.$store.state.credentials.twin.id);
    this.proposals = this.$store.state.portal.proposals;
    if (!this.proposals) return;
    this.voteMsg =
      this.proposals > 1
        ? `You have ${this.proposals} pending proposals to vote!`
        : `You have a pending proposal to vote!`;
    this.openProposalDialog = true;
  }
  daoRedirect() {
    this.openProposalDialog = false;
    this.$router.push({
      path: "account-dao",
    });
  }
}
</script>
