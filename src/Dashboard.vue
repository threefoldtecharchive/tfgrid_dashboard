<template>
  <v-app>

    <div>
      <v-app-bar
        color="deep-purple accent-4"
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

        <v-card
          class="mx-2 px-1 "
          v-if="$store.state.portal.accounts.length === 0"
        >
          <v-icon
            color="#F44336"
            class="fa-solid fa-circle-dot px-2 "
          ></v-icon>
          <v-btn icon>
            <v-icon
              class=""
              @click="$store.dispatch('portal/subscribeAccounts')"
            >mdi-lan-connect</v-icon>
          </v-btn>
        </v-card>
        <v-card
          v-else
          class="mx-2 px-1 "
        >
          <v-icon
            color="#4CAF50"
            class="fa-solid fa-circle-dot px-2 "
          ></v-icon>
          <v-btn icon>

            <v-icon
              class=""
              @click="disconnectWallet"
            >mdi-lan-disconnect</v-icon>

          </v-btn>
        </v-card>

      </v-app-bar>
    </div>

    <v-navigation-drawer
      app
      permanent
      v-model="drawer"
      width="300"
      :mini-variant.sync="mini"
    >
      <v-list>
        <v-list-item class="px-2">
          <v-list-item-avatar>
            <v-img src="https://i.ibb.co/k39ThGn/3fold-logo.png"></v-img>
          </v-list-item-avatar>

          <v-list-item-title @click="redirectToHomePage">THREEFOLD CHAIN</v-list-item-title>

          <v-btn
            icon
            @click.stop="mini = !mini"
          >
            <v-icon>mdi-chevron-left</v-icon>
          </v-btn>
        </v-list-item>
        <v-divider></v-divider>
        <v-list-group
          v-model="route.active"
          v-for="route in routes"
          :key="route.label"
        >
          <template v-slot:activator>
            <v-list-item-icon>
              <v-icon v-text="'mdi-' + route.icon" />
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>
                <strong>
                  {{ route.label.toUpperCase() }}
                </strong>
              </v-list-item-title>
            </v-list-item-content>
          </template>
          <div
            class="px-5 d-flex row justify-center"
            v-if="route.label.toLocaleLowerCase() === 'portal' && $store.state.portal.accounts.length !== 0"
          >
            <v-text-field
              append-icon="mdi-account-search"
              v-model="searchTerm"
              color="purple darken-2"
              class="pl-3 pr-2 mr-2"
              label="Account name/address"
            />

          </div>

          <div v-if="route.prefix==='/'">
            <v-list-group
              :value="false"
              no-action
              sub-group
              v-for="account in filteredAccounts()"
              :key="account.address"
            >
              <template v-slot:activator>

                <v-list-item-content>

                  <v-list-item-title v-text="account.meta.name.toUpperCase()">
                  </v-list-item-title>

                </v-list-item-content>
                <v-list-item-icon>
                  <v-icon v-text="'mdi-' + route.children[0].icon" />
                </v-list-item-icon>

              </template>

              <v-list-item
                v-for="subchild in route.children[0].children"
                :key="subchild.label"
                @click="redirectToSubchild(subchild.label, account.address, account.meta.name)"
              >

                <v-list-item-icon>
                  <v-icon v-text="'mdi-' + subchild.icon" />
                </v-list-item-icon>
                <v-list-item-content>

                  <v-list-item-title v-text="subchild.label.toUpperCase()">
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
                <v-icon v-text="'mdi-' + child.icon" />
              </v-list-item-icon>
              <v-list-item-content>

                <v-list-item-title v-text="child.label">
                </v-list-item-title>

              </v-list-item-content>
            </v-list-item>
          </div>

        </v-list-group>

      </v-list>
    </v-navigation-drawer>

    <router-view />
    <v-footer
      dark
      padless
      fixed
    >
      <v-card
        class="flex"
        flat
        tile
      >

        <v-card-text class="py-2 white--text text-center">
          {{ new Date().getFullYear() }} — <strong>ThreeFoldTech</strong>
        </v-card-text>
      </v-card>
      <v-card
        v-if="$route.path !=='/' && !$route.path.includes('explorer') && !$route.path.includes('hub')"
        color="#0D47A1"
        class=" funds px-3 d-flex align-baseline font-weight-bold"
      > {{balance }} TFT
        <v-btn
          @click="addTFT"
          class="ml-3"
          :loading="loadingAddTFT"
        >+</v-btn>
      </v-card>
    </v-footer>
  </v-app>
</template>

<script lang="ts">
import config from "@/portal/config";
import { Component, Vue, Watch } from "vue-property-decorator";
import { getBalance, getMoreFunds } from "./portal/lib/balance";
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
  address = "";
  accounts: accountInterface[] = [];
  searchTerm = "";
  loadingAddTFT = false;
  @Watch("address") async onAddressChanged(value: string, oldValue: string) {
    if (oldValue.length) {
      console.log(`removing account ${oldValue}, putting in account ${value}`);
    } else {
      console.log(`putting in account ${value}`);
    }
  }
  @Watch("balance") async onBalanceUpdate(value: number, oldValue: number) {
    console.log(`balance went from ${oldValue}, to ${value}`);
  }
  async created() {
    if (this.$route.path === "/" && !this.$api) {
      Vue.prototype.$api = await connect(); //declare global variable api
      console.log(`connecting to api`);
    }
  }
  async mounted() {
    this.accounts = this.$store.state.portal.accounts;

    if (this.$route.path !== "/") {
      if (this.$route.params.accountID) {
        this.address = this.$route.params.accountID;
        this.balance = this.$route.query.balance;
      }
    }
  }
  async updated() {
    this.accounts = this.$store.state.portal.accounts;
    if (this.$route.path !== "/") {
      if (this.$route.params.accountID) {
        this.address = await this.$route.params.accountID;
        this.balance = (await getBalance(this.$api, this.address)) / 1e7;
      }
    }
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
  public async addTFT() {
    if (config.network !== "dev") {
      //redirect to https://gettft.com/auth/login?next_url=/gettft/shop/#/buy
    } else {
      this.loadingAddTFT = true;
      getMoreFunds(
        this.address,
        this.$api,
        (res: {
          events?: never[] | undefined;
          status: { type: string; asFinalized: string; isFinalized: string };
        }) => {
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
              if (section === "balances" && method === "Transfer") {
                this.$toasted.show("Success!");

                getBalance(this.$api, this.address).then((balance) => {
                  this.balance = balance / 1e7;
                });
                this.loadingAddTFT = false;
              } else if (section === "system" && method === "ExtrinsicFailed") {
                this.$toasted.show("Get more TFT failed!");
                this.loadingAddTFT = false;
              }
            });
          }
        }
      ).catch((err: { message: string }) => {
        console.log(err.message);
      });
    }
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
