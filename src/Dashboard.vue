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

        <v-toolbar-title class="font-weight-bold">THREEFOLD CHAIN</v-toolbar-title>

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
              @click="$store.dispatch('portal/unsubscribeAccounts')"
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
            <v-img
              @click="redirectToHomePage"
              src="https://i.ibb.co/k39ThGn/3fold-logo.png"
            ></v-img>
          </v-list-item-avatar>

          <v-list-item-title>THREEFOLD CHAIN</v-list-item-title>

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
                  {{ route.label }}
                </strong>
              </v-list-item-title>
            </v-list-item-content>
          </template>
          <div v-if="route.prefix==='/'">
            <v-list-group
              :value="true"
              no-action
              sub-group
              v-for="account in $store.state.portal.accounts"
              :key="account.address"
            >
              <template v-slot:activator>

                <v-list-item-content>

                  <v-list-item-title v-text="account.meta.name">
                  </v-list-item-title>

                </v-list-item-content>
                <v-list-item-icon>
                  <v-icon
                    @click="routeToAccount(account.address, account.meta.name)"
                    v-text="'mdi-' + route.children[0].icon"
                  />
                </v-list-item-icon>

              </template>
              <v-list-item
                v-for="subchild in route.children[0].children"
                :key="subchild.label"
                :to="route.prefix + account.address + '/'+ subchild.path"
              >
                <v-list-item-icon>
                  <v-icon v-text="'mdi-' + subchild.icon" />
                </v-list-item-icon>
                <v-list-item-content>

                  <v-list-item-title v-text="subchild.label">
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

    <router-view style="padding-top: 8.5%; padding-left: 10%; padding-right: 10%;" />
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
    </v-footer>
  </v-app>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import FundsCard from "./components/FundsCard.vue";

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
  components: { FundsCard },
})
export default class Dashboard extends Vue {
  collapseOnScroll = true;
  mini = true;
  drawer = true;
  public redirectToHomePage() {
    this.$router.push({
      name: "Accounts",
      path: "/",
    });
  }
  public routeToAccount(address: string, name: string) {
    this.$router.push({
      name: "Account",
      path: "account",
      params: { accountID: `${address}`, accountName: `${name}` },
    });
  }
  routes: SidenavItem[] = [
    {
      //label and path will be retrieved from accounts fetched from store (polkadot)
      active: true,
      label: "Portal",
      icon: "account-convert-outline",
      prefix: "/",
      children: [
        {
          icon: "account",
          showBeforeLogIn: true,
          active: true,
          children: [
            {
              label: "Twin",
              icon: "account-box-multiple-outline",
              path: "twin",
            },
            {
              label: "Transfer",
              icon: "swap-horizontal",
              path: "transfer",
            },
            { label: "Farms", icon: "silo", path: "farms" },
            {
              label: "Dedicated Nodes",
              icon: "resistor-nodes",
              path: "nodes",
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
