<template>
  <v-container>

    <v-card
      color="#388E3C"
      class="text-center py-5 my-3 "
    >
      <h2>
        Welcome aboard {{$route.query.accountName}}, <br>
        Let’s get you connected to the TF Grid !

      </h2>
    </v-card>
    <v-card
      color="#512DA8"
      class="text-center pa-5"
    >
      <h3>Choose your preferred method : </h3>
    </v-card>
    <v-container fluid>
      <v-row>

        <v-col>
          <v-card
            class="pa-5 text-center"
            height="150"
          >
            <h3>
              Create a Twin using Planetary
              using Yggdrasil IPV6
            </h3>
            <v-text-field label="Twin IP ::1">

            </v-text-field>
          </v-card>
        </v-col>
        <v-col>
          <v-card
            class="pa-5 text-center"
            height="150"
          >
            <h3>
              Create a Twin automatically
            </h3>

          </v-card>
        </v-col>

      </v-row>

    </v-container>
  </v-container>

</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { getBalance } from "../lib/balance";
import { connect } from "../lib/connect";
@Component({
  name: "AccountView",
})
export default class AccountView extends Vue {
  async mounted() {
    const address = this.$route.params.accountID;
    const api = await connect();
    const balance = (await getBalance(api, address)) / 1e7;
    this.$store.dispatch("portal/setBalanceAction", balance);
  }
}
</script>