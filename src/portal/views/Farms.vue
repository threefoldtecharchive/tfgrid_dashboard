<template>
  <div class="main">
    <h3>Farms</h3>
    <v-data-table
      :headers="headers"
      :items="farms"
      :single-expand="singleExpand"
      :expanded.sync="expanded"
      item-key="name"
      show-expand
      class="elevation-1"
      dark
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Your Farms</v-toolbar-title>
          <v-spacer></v-spacer>

        </v-toolbar>
      </template>
      <template v-slot:expanded-item="{ item }">
        <td :colspan="headers.length">
          <v-col>
            <v-container fluid>
              <v-row>
                <v-flex
                  xs3
                  class="text-left pr-2"
                >Farm ID</v-flex>
                <v-flex class="text-truncate font-weight-bold">
                  <span>{{ item.id }}</span>
                </v-flex>
              </v-row>
              <v-row>
                <v-flex
                  xs3
                  class="text-left pr-2"
                >Farm Name</v-flex>
                <v-flex class="text-truncate font-weight-bold">
                  <span>{{ item.name }}</span>
                </v-flex>
              </v-row>
              <v-row>
                <v-flex
                  xs3
                  class="text-left pr-2"
                >Linked Twin ID</v-flex>
                <v-flex class="text-truncate font-weight-bold">
                  <span>{{ item.twin_id }}</span>
                </v-flex>
              </v-row>
              <v-row>
                <v-flex
                  xs3
                  class="text-left pr-2"
                >Certification Type</v-flex>
                <v-flex class="text-truncate font-weight-bold">
                  <span>{{ item.certification_type }}</span>
                </v-flex>
              </v-row>
              <v-row>
                <v-flex
                  xs3
                  class="text-left"
                >Linked pricing Policy ID</v-flex>
                <v-flex class="text-truncate font-weight-bold">
                  <span>{{ item.pricing_policy_id }}</span>
                </v-flex>
              </v-row>

              <v-row>
                <v-flex
                  xs3
                  class="text-left"
                >Bootstrap node image</v-flex>
                <v-flex xs3>
                  <a
                    class="link"
                    v-bind:href="'https://v3.bootstrap.grid.tf/'"
                    target="blank"
                  >Take me to bootstrap page</a>
                </v-flex>
              </v-row>

            </v-container>
          </v-col>
        </td>
      </template>
    </v-data-table>

  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { getFarm } from "../lib/farms";

@Component({
  name: "FarmsView",
})
export default class FarmsView extends Vue {
  headers = [
    { text: "Farm ID", value: "id" },
    { text: "Farm name", value: "name" },
    { text: "Linked Twin ID", value: "twin_id" },
    { text: "Certification type", value: "certification_type" },
    { text: "Pricing Policy ID", value: "pricing_policy_id" },
  ];
  farms = [];
  id: any = [];

  singleExpand = true;
  expanded = [];
  async mounted() {
    this.id = this.$route.query.twinID;

    this.farms = await getFarm(this.$store.state.api, this.id);
  }
  async updated() {
    this.id = this.$route.query.twinID;
  }
}
</script>