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
          style="cursor: pointer;"
        >Threefold Chain</v-toolbar-title>

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
          outlined
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
          outlined
          v-else
          color="transparent"
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
        <v-btn
          icon
          class="mr-2"
          @click="redirectToHomePage"
          v-if="isAccountSelected()"
        >
          <v-icon>mdi-logout theme-light-dark</v-icon>
        </v-btn>
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
            style="cursor: pointer;"
          >Threefold Chain</v-list-item-title>

          <v-btn
            icon
            @click.stop="toggle()"
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
          :style= "mini ? '' : 'margin: 10px !important;'"
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

          <div v-if="route.prefix === '/'">
            <v-list-group
              :value="account.active"
              no-action
              sub-group
              v-for="account in filteredAccounts()"
              :key="account.address"
            >
              <template v-slot:activator>
                <v-list-item-content dark>
                  <v-list-item-title
                    class="white--text"
                    v-text="account.meta.name"
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
                v-for="subchild in getRouteSubChildren(route)"
                :key="subchild.label"
                @click="
                  redirectToSubchild(
                    subchild.label,
                    subchild.path || '',
                    account.address,
                    account.meta.name
                  )
                "
                class="white--text pl-16"
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
              class="pl-16"
            >
              <v-list-item-icon
                class="mr-4"
                v-if="child.icon"
              >
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
    <v-dialog
      v-model="loadingAPI"
      persistent
      class="loadingDialog"
    >
      <div
        class="d-flex justify-center"
        style="display: block; padding: 10%"
      >
        <v-progress-circular
          indeterminate
          color="green"
          :size="335"
          :width="7"
        >
          <span style="font-size: large; color: black">Connecting to Polkadot</span>
        </v-progress-circular>
      </div>
    </v-dialog>

    <div :style="'padding-left:' + (mini ? 0 : '300px')">
      <router-view />
    </div>

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
import { balanceInterface, getBalance } from "./portal/lib/balance";
import { connect } from "./portal/lib/connect";
import { getTwin, getTwinID } from "./portal/lib/twin";
import { accountInterface } from "./portal/store/state";
import WelcomeWindow from "./portal/components/WelcomeWindow.vue";
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
          path?: string;
          icon: string;
        }>
      | [];
  }>;
}
@Component({
  name: "Dashboard",
  components: { WelcomeWindow },
})
export default class Dashboard extends Vue {
  collapseOnScroll = true;
  mini = true;
  drawer = true;
  twinID = 0;
  $api: any;
  twin: { id: string; ip: string } = { id: "", ip: "" };
  balance: balanceInterface = { free: 0, reserved: 0 };
  accounts: accountInterface[] = [];
  loadingAPI = true;
  async mounted() {
    this.accounts = this.$store.state.portal.accounts;
    if (this.$route.path === "/" && !this.$api) {
      Vue.prototype.$api = await connect(); //declare global variable api
      console.log(`connecting to api`);
      this.loadingAPI = false;
    }
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
    this.$root.$on('selectAccount', () => { 
      this.routes[0].active = true;
      this.mini = false;
    })
  }
  updated() {
    this.accounts = this.$store.state.portal.accounts;
    if (this.$api) {
      this.loadingAPI = false;
    }
  }
  async unmounted() {
    console.log(`disconnecting from api`);
    await this.$api.disconnect();
  }
  public filteredAccounts() {
    return this.accounts.filter(
      (account) => account.active
    );
  }
  public isAccountSelected() {
    if (this.$route.query.accountName) {
      return true;
    }
    return false;
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
    path: string,
    address: string,
    name: string
  ) {
    //
    this.twinID = await getTwinID(this.$api, address);
    this.balance = await getBalance(this.$api, address);
    if (this.twinID) {
      this.twin = await getTwin(this.$api, this.twinID);
      if (
        !this.$route.path.includes(path) ||
        this.$route.params.accountID !== address
      ) {
        this.$router.push({
          name: `${path}`,
          params: { accountID: `${address}` },
          query: {
            accountName: `${name}`,
            twinID: this.twin.id,
            twinIP: this.twin.ip,
            balanceFree: `${this.balance.free}`,
            balanceReserved: `${this.balance.reserved}`,
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
              label: "twin",
              path: "account-twin",
              icon: "account-supervisor-outline",
            },
            {
              label: "swap",
              path: "account-swap",
              icon: "swap-horizontal",
            },
            {
              label: "transfer",
              path: "account-transfer",
              icon: "account-arrow-right-outline",
            },
            { label: "farms", path: "account-farms", icon: "silo" },
            {
              label: "dedicated nodes",
              path: "account-nodes",
              icon: "resistor-nodes",
            },
            { label: "dao", path: "account-dao", icon: "note-check-outline" },
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
  ];
  getRouteSubChildren(route: SidenavItem) {
    return route.children[0].children || [];
  }
  toggle(){
    this.mini = !this.mini;
    if (this.mini) this.routes[1].active = false;
  }
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
.loadingDialog {
  overflow: hidden;
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
  border-radius: 20px;
}

.v-list .v-list-item--active{
  border-radius: 20px;
}

</style>