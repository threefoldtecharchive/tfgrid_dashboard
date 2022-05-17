<template>
  <v-app>

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
        </v-list-group>
      </v-list>
    </v-navigation-drawer>

    <router-view style="padding-left: 70px" />
    <v-footer
      dark
      padless
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

interface SidenavItem {
  label: string;
  icon: string;
  prefix: string;
  active?: boolean;
  children: Array<{
    label: string;
    path: string;
    icon: string;
  }>;
}

@Component({
  name: "Dashboard",
})
export default class Dashboard extends Vue {
  collapseOnScroll = true;
  mini = true;
  drawer = true;
  routes: SidenavItem[] = [
    {
      label: "Portal",
      icon: "account-convert-outline",
      prefix: "/",
      children: [
        { label: "Twin", path: "", icon: "account-multiple" },
        {
          label: "Transfer",
          path: "transfer",
          icon: "swap-horizontal",
        },
        { label: "Farms", path: "farms", icon: "silo" },
        {
          label: "Dedicated Nodes",
          path: "dedicated-nodes",
          icon: "resistor-nodes",
        },
      ],
    },
    {
      active: true,
      label: "Explorer",
      icon: "database-search-outline",
      prefix: "/explorer/",
      children: [
        {
          label: "Statistics",
          path: "statistics",
          icon: "chart-scatter-plot",
        },
        { label: "Nodes", path: "nodes", icon: "access-point" },
        { label: "Farms", path: "farms", icon: "lan-connect" },
      ],
    },
    {
      label: "Hub",
      icon: "axis-arrow-info",
      prefix: "/hub/",
      children: [
        { label: "Send To Cosmos", path: "send-to-cosmos", icon: "" },
        { label: "Send To BSC", path: "send-to-bsc", icon: "" },
        {
          label: "Pending BSC Transactions",
          path: "pending-bsc-transactions",
          icon: "",
        },
        { label: "Add Proposal", path: "add-proposal", icon: "" },
        { label: "Proposals", path: "proposals", icon: "" },
        { label: "Validators", path: "validators", icon: "" },
      ],
    },
  ];
}
</script>
