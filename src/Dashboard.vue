<template>
  <v-app>
    <div>
      <v-app-bar
        color="#064663"
        dense
        dark
        fixed
        height="65"
      >
        <v-app-bar-nav-icon></v-app-bar-nav-icon>

        <v-toolbar-title
          class="font-weight-bold"
          @click="redirectToHomePage"
        >THREEFOLD CHAIN</v-toolbar-title>

        <v-spacer></v-spacer>
        <v-btn
          icon
          @click="toggle_dark_mode"
        >
          <v-icon>mdi-theme-light-dark</v-icon>
        </v-btn>
        <v-card
          class="mx-2 px-1"
          color="transparent"
          v-if="$store.state.portal.accounts.length === 0"
        >
          <v-btn icon>
            <v-icon
              class=""
              color="#F44336"
              @click="$store.dispatch('portal/subscribeAccounts')"
            >mdi-lan-disconnect</v-icon>
          </v-btn>
        </v-card>
        <v-card
          v-else
          color="transparent"
          class="mx-2 px-1"
        >
          <v-btn icon>
            <v-tooltip>
              <template v-slot:activator="{ on, attrs }">
                <v-icon
                  color="#4CAF50"
                  class=""
                  @click="disconnectWallet"
                  v-bind="attrs"
                  v-on="on"
                >mdi-lan-connect</v-icon>
              </template>
              <span>Disconnect Wallet</span>

            </v-tooltip>
          </v-btn>
        </v-card>
      </v-app-bar>
    </div>

    <v-navigation-drawer
      app
      color="#333"
      class="white--text"
      permanent
      v-model="drawer"
      width="300"
      :mini-variant.sync="mini"
    >
      <v-list>
        <v-list-item class="px-2">
          <v-list-item-avatar>
            <v-img src="./assets/logo.png"></v-img>
          </v-list-item-avatar>

          <v-list-item-title
            class="white--text"
            @click="redirectToHomePage"
          >THREEFOLD CHAIN</v-list-item-title>

          <v-btn
            icon
            @click.stop="mini = !mini"
          >
            <v-icon class="white--text">mdi-chevron-left</v-icon>
          </v-btn>
        </v-list-item>
        <v-divider></v-divider>
        <v-list-group
          v-model="route.active"
          v-for="route in routes"
          :key="route.label"
          class="white--text"
        >
          <template v-slot:activator>
            <v-list-item-icon>
              <v-icon
                class="white--text"
                v-text="'mdi-' + route.icon"
              />
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title class="white--text">
                <strong>
                  {{ route.label }}
                </strong>
              </v-list-item-title>
            </v-list-item-content>
          </template>
          <div
            class="white--text px-5 d-flex row justify-center"
            v-if="
              route.label.toLocaleLowerCase() === 'portal' &&
              $store.state.portal.accounts.length !== 0
            "
          >
            <v-text-field
              append-icon="mdi-account-search"
              v-model="searchTerm"
              color="primary darken-2"
              class="white--text pl-3 pr-2 mr-2"
              label="Account name/address"
              dark
            />
          </div>

          <div v-if="route.prefix === '/'">
            <v-list-group
              :value=false
              no-action
              sub-group
              v-for="account in filteredAccounts()"
              :key="account.address"
            >
              <template v-slot:activator>
                <v-list-item-content dark>
                  <v-list-item-title
                    class="white--text"
                    v-text="account.meta.name.toUpperCase()"
                  >
                  </v-list-item-title>
                </v-list-item-content>
                <v-list-item-icon>
                  <v-icon
                    class="white--text"
                    v-text="'mdi-' + route.children[0].icon"
                  />
                </v-list-item-icon>
              </template>

              <v-list-item
                v-for="subchild in route.children[0].children"
                :key="subchild.label"
                @click="
                  redirectToSubchild(
                    subchild.label,
                    account.address,
                    account.meta.name
                  )
                "
                class="white--text"
              >
                <v-list-item-icon>
                  <v-icon
                    class="white--text"
                    v-text="'mdi-' + subchild.icon"
                  />
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title
                    class="white--text text-capitalize"
                    v-text="subchild.label"
                  >
                  </v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list-group>
          </div>
          <div v-else>
            <v-list-item
              active
              v-for="child in route.children"
              :key="child.label"
              :to="route.prefix + child.path"
            >
              <v-list-item-icon>
                <v-icon
                  class="white--text"
                  v-text="'mdi-' + child.icon"
                />
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title
                  class="white--text"
                  v-text="child.label"
                >
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </div>
        </v-list-group>
      </v-list>
    </v-navigation-drawer>

    <router-view />
    <v-footer
      padless
      fixed
    >
      <v-card
        class="flex"
        flat
        tile
      >
        <v-card-text class="py-2 text-center">
          {{ new Date().getFullYear() }} — <strong>ThreeFoldTech</strong>
        </v-card-text>
      </v-card>
    </v-footer>
  </v-app>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { getBalance } from "./portal/lib/balance";
import { connect } from "./portal/lib/connect";
import { getTwin, getTwinID } from "./portal/lib/twin";
import { accountInterface } from "./portal/store/state";

interface SidenavItem {
  label: string;
  icon: string;
  prefix: string;
  active?: boolean;
  children: Array<{
    label?: string;
    path?: string;
    icon: string;
    active?: boolean;
    showBeforeLogIn: boolean; //i.e loginto the polkadot.js
    children?:
      | Array<{
          label: string;
          icon: string;
          path?: string;
        }>
      | [];
  }>;
}

@Component({
  name: "Dashboard",
})
export default class Dashboard extends Vue {
  collapseOnScroll = true;
  mini = true;
  drawer = true;
  twinID: any;
  $api: any;
  twin: any;
  balance: any = 0;
  accounts: accountInterface[] = [];
  searchTerm = "";

  async created() {
    if (this.$route.path === "/" && !this.$api) {
      Vue.prototype.$api = await connect(); //declare global variable api
      console.log(`connecting to api`);
    }
  }
  mounted() {
    this.accounts = this.$store.state.portal.accounts;

    const theme = localStorage.getItem("dark_theme");
    if (theme) {
      if (theme === "true") {
        this.$vuetify.theme.dark = true;
      } else {
        this.$vuetify.theme.dark = false;
      }
    } else if (
      window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches
    ) {
      this.$vuetify.theme.dark = true;
      localStorage.setItem("dark_theme", this.$vuetify.theme.dark.toString());
    }
  }

  updated() {
    this.accounts = this.$store.state.portal.accounts;
  }
  async unmounted() {
    console.log(`disconnecting from api`);
    await this.$api.disconnect();
  }
  public filteredAccounts() {
    if (this.searchTerm.length !== 0) {
      return this.accounts.filter(
        (account) =>
          account.meta.name
            .toLowerCase()
            .includes(this.searchTerm.toLowerCase()) ||
          account.address.toLowerCase().includes(this.searchTerm.toLowerCase())
      );
    }
    return this.accounts;
  }

  public disconnectWallet() {
    this.$store.dispatch("portal/unsubscribeAccounts");
    if (this.$route.query.twinID) {
      this.$router.push({
        name: "accounts",
        path: `/`,
      });
    }
  }
  public redirectToHomePage() {
    if (this.$route.path !== "/") {
      this.$router.push({
        name: "accounts",
        path: "/",
      });
    }
  }

  public async redirectToSubchild(
    label: string,
    address: string,
    name: string
  ) {
    //

    this.twinID = await getTwinID(this.$api, address);
    this.balance = (await getBalance(this.$api, address)) / 1e7;
    if (this.twinID) {
      this.twin = await getTwin(this.$api, this.twinID);
      if (
        !this.$route.path.includes(label) ||
        this.$route.params.accountID !== address
      ) {
        this.$router.push({
          name: `${label}`,
          path: `/:accountID/${label}`,
          params: { accountID: `${address}` },
          query: {
            accountName: `${name}`,
            twinID: this.twin.id,
            twinIP: this.twin.ip,
            balance: `${this.balance}`,
          },
        });
      }
    } else {
      if (!this.$route.path.includes(address)) {
        this.$router.push({
          name: "account",
          path: "account",
          params: { accountID: `${address}` },
          query: { accountName: `${name}` },
        });
      }
    }
  }

  public toggle_dark_mode() {
    this.$vuetify.theme.dark = !this.$vuetify.theme.dark;
    localStorage.setItem("dark_theme", this.$vuetify.theme.dark.toString());
  }

  routes: SidenavItem[] = [
    {
      //label and path will be retrieved from accounts fetched from store (polkadot)
      label: "Portal",
      icon: "account-convert-outline",
      prefix: "/",
      children: [
        {
          icon: "account",
          showBeforeLogIn: true,
          children: [
            {
              label: "account-twin",
              icon: "account-supervisor-outline",
            },
            {
              label: "account-swap",
              icon: "swap-horizontal",
            },
            {
              label: "account-transfer",
              icon: "account-arrow-right-outline",
            },
            { label: "account-farms", icon: "silo" },
            { label: "account-dao", icon: "note-check-outline" },
            {
              label: "account-nodes",
              icon: "resistor-nodes",
            },
          ],
        },
      ],
    },
    {
      label: "Explorer",
      icon: "database-search-outline",
      prefix: "/explorer/",
      children: [
        {
          label: "Statistics",
          path: "statistics",
          icon: "chart-scatter-plot",
          showBeforeLogIn: true,
        },
        {
          label: "Nodes",
          path: "nodes",
          icon: "access-point",
          showBeforeLogIn: true,
        },
        {
          label: "Farms",
          path: "farms",
          icon: "lan-connect",
          showBeforeLogIn: true,
        },
      ],
    },
    {
      label: "Hub",
      icon: "axis-arrow-info",
      prefix: "/hub/",
      children: [
        {
          label: "Send To Cosmos",
          path: "send-to-cosmos",
          icon: "",
          showBeforeLogIn: true,
        },
        {
          label: "Send To BSC",
          path: "send-to-bsc",
          icon: "",
          showBeforeLogIn: true,
        },
        {
          label: "Pending BSC Transactions",
          path: "pending-bsc-transactions",
          icon: "",
          showBeforeLogIn: true,
        },
        {
          label: "Add Proposal",
          path: "add-proposal",
          icon: "",
          showBeforeLogIn: true,
        },
        {
          label: "Proposals",
          path: "proposals",
          icon: "",
          showBeforeLogIn: true,
        },
        {
          label: "Validators",
          path: "validators",
          icon: "",
          showBeforeLogIn: true,
        },
      ],
    },
  ];
}
</script>

<style>
@import "./assets/css/styles.css";
#app {
  background-color: var(--v-background-base);
}
.v-navigation-drawer {
  background-color: #333;
}

.v-list-item__icon .theme--light.fa-chevron-down,
.v-list-item__icon .theme--light.fa-caret-down,
.v-list-item__icon .theme--light.fa-chevron-up,
.v-list-item__icon .theme--light.fa-caret-up {
  color: white !important;
}

.v-list .v-list-item--link:hover,
.v-list-item--link:before {
  background-color: #1982b1 !important;
  color: white !important;
}
</style>
