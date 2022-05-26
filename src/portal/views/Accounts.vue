<template>
  <v-container v-if="$store.state.portal.accounts.length === 0">

    <WelcomeWindow />

  </v-container>
  <v-container
    v-else
    style=""
  >
    <h1 class="text-center">Connected Accounts</h1>

    <v-container fluid>
      <v-row>
        <v-col>
          <v-text-field
            v-model="searchTerm"
            color="purple darken-2"
            label="Search by account name or address"
          ></v-text-field>

        </v-col>
      </v-row>

      <v-card
        v-for="account in filteredAccounts()"
        :key="account.address"
        color="#448AFF"
        @click="addAccountRoute(account)"
        class="my-4"
      >

        <div class="d-flex justify-space-between">
          <div class="d-inline-block text-truncate">
            <v-card-title>{{account.meta.name.toUpperCase()}}</v-card-title>
            <v-card-subtitle>
              {{account.address}}
            </v-card-subtitle>
          </div>
          <v-icon>mdi-chevron-right</v-icon>
        </div>

      </v-card>

    </v-container>

  </v-container>

</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { accountInterface } from "../store/state";
import WelcomeWindow from "../../components/WelcomeWindow.vue";
import Account from "./Account.vue";

@Component({
  name: "AccountsView",
  components: { WelcomeWindow, Account },
})
export default class AccountsView extends Vue {
  searchTerm = "";
  accounts: accountInterface[] = [];
  mounted() {
    this.accounts = this.$store.state.portal.accounts;
  }
  public filteredAccounts() {
    return this.accounts.filter(
      (account) =>
        account.meta.name
          .toLowerCase()
          .includes(this.searchTerm.toLowerCase()) ||
        account.address.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }
  public addAccountRoute(account: accountInterface) {
    this.$router.push({
      name: "account",
      path: "account",
      params: { accountID: `${account.address}` },
      query: { accountName: `${account.meta.name}` },
    });
  }
}
</script>