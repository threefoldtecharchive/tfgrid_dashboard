<template>
  <v-container v-if="$store.state.portal.accounts.length === 0">

    <v-card
      color="black"
      dark
      flat
      tile
    >
      <v-window v-model="onboarding">
        <v-window-item
          v-for="(card, index) in cards"
          :key="`card-${index}`"
        >
          <v-card
            color="transparent"
            height="825"
          >
            <v-row
              class="fill-height"
              align="center"
              justify="center"
            >

              <v-card-text
                class="text-center"
                style="font-size: 2rem"
              >
                <v-img
                  width="450"
                  style="margin:auto"
                  v-bind:src="card.img"
                >

                </v-img>
                <v-card-subtitle style="font-size: 1.5rem">
                  {{card.text}}
                </v-card-subtitle>
                <v-btn
                  color="primary"
                  x-large
                  style="margin-top:1.25rem"
                  v-bind:href="card.link"
                  v-bind:target="blank"
                >
                  {{card.button}}
                </v-btn>

              </v-card-text>
            </v-row>
          </v-card>
        </v-window-item>

      </v-window>

      <v-card-actions class="justify-space-between">
        <v-btn
          text
          @click="prev"
        >
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
        <v-item-group
          v-model="onboarding"
          class="text-center"
          mandatory
        >
          <v-item
            v-for="n in cards.length"
            :key="`btn-${n}`"
            v-slot="{ active, toggle }"
          >
            <v-btn
              :input-value="active"
              icon
              @click="toggle"
            >
              <v-icon>mdi-record</v-icon>
            </v-btn>
          </v-item>
        </v-item-group>
        <v-btn
          text
          @click="next"
        >
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>

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
            v-model=" searchAccount"
            color="purple darken-2"
            label="Search by account name"
          ></v-text-field>
        </v-col>
      </v-row>

      <v-card
        v-for="account in $store.state.portal.accounts"
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

interface WelcomeCard {
  text: string;
  button: string;
  img: string;
  link: string;
}
interface accountInterface {
  address: string;
  meta: { genesisHash: string; name: string; source: string };
  type: string;
}
@Component({
  name: "AccountsView",
})
export default class AccountsView extends Vue {
  onboarding = 0;
  blank = "blank";
  searchAccount = "";
  cards: WelcomeCard[] = [
    {
      text: "The Decentralized Cloud Awaits!",
      button: "Sign in to your polkadot{.js} account to access the Portal",
      link: "https://polkadot.js.org/extension/",
      img: "https://i.ibb.co/vVL5jwN/threefold-registered.png",
    },
    {
      text: "Discover the ThreeFold Grid",
      button: "View ThreeFold Capacity ",
      link: "https://explorer.dev.grid.tf/",
      img: "https://i.ibb.co/fkDqVsh/png-world-map-world-map-png-2638-3455212594.png",
    },
    {
      text: "Your Guide to The ThreeFold Grid",
      button: "Learn More",
      link: "https://library.threefold.me/info/manual/#/",
      img: "https://i.ibb.co/1Q8Py99/networking-538-149353815.png",
    },
  ];

  public next() {
    this.onboarding =
      this.onboarding + 1 === this.cards.length ? 0 : this.onboarding + 1;
  }
  public prev() {
    this.onboarding =
      this.onboarding - 1 < 0 ? this.cards.length - 1 : this.onboarding - 1;
  }

  public addAccountRoute(account: accountInterface) {
    this.$router.push({
      name: "Account",
      path: "account",
      params: { accountID: `${account.address}` },
      query: { accountName: `${account.meta.name}` },
    });
  }
}
</script>