<template>
  <v-app>
    <v-navigation-drawer app width="300">
      <v-list>
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
            <v-list-item-icon />
            <v-list-item-content>
              <v-list-item-title v-text="child.label"></v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-group>
      </v-list>
    </v-navigation-drawer>
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
  }>;
}

@Component({
  name: "Dashboard",
})
export default class Dashboard extends Vue {
  routes: SidenavItem[] = [
    {
      label: "Portal",
      icon: "account-convert-outline",
      prefix: "/",
      children: [
        { label: "Twin", path: "" },
        { label: "Transfer", path: "transfer" },
        { label: "Farms", path: "farms" },
        { label: "Dedicated Nodes", path: "dedicated-nodes" },
        { label: "Capacity", path: "capacity" },
      ],
    },
    {
      active: true,
      label: "Explorer",
      icon: "database-search-outline",
      prefix: "/explorer/",
      children: [
        { label: "Statistics", path: "statistics" },
        { label: "Nodes", path: "nodes" },
        { label: "Farms", path: "farms" },
      ],
    },
    {
      label: "Hub",
      icon: "axis-arrow-info",
      prefix: "/hub/",
      children: [
        { label: "Send To Cosmos", path: "send-to-cosmos" },
        { label: "Send To BSC", path: "send-to-bsc" },
        { label: "Pending BSC Transactions", path: "pending-bsc-transactions" },
        { label: "Add Proposal", path: "add-proposal" },
        { label: "Proposals", path: "proposals" },
        { label: "Validators", path: "validators" },
      ],
    },
  ];
}
</script>
