<template>
  <v-container fluid>

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

          <v-container
            fluid
            class="text-left"
          >
            <v-row>
              <v-col>
                <v-flex class="text-left pr-2">Farm ID</v-flex>
              </v-col>
              <v-col>
                <v-flex class="text-truncate font-weight-bold">
                  <span>{{ item.id }}</span>
                </v-flex>
              </v-col>

            </v-row>
            <v-row>
              <v-col>
                <v-flex class="text-left pr-2">Farm Name</v-flex>
              </v-col>
              <v-col>
                <v-flex class="text-truncate font-weight-bold">
                  <span>{{ item.name }}</span>
                </v-flex>
              </v-col>

            </v-row>
            <v-row>
              <v-col>
                <v-flex class="text-left pr-2">Linked Twin ID</v-flex>
              </v-col>
              <v-col>
                <v-flex class="text-truncate font-weight-bold">
                  <span>{{ item.twin_id }}</span>
                </v-flex>
              </v-col>

            </v-row>
            <v-row>
              <v-col>
                <v-flex class="text-left pr-2">Certification Type</v-flex>
              </v-col>
              <v-col>
                <v-flex class="text-truncate font-weight-bold">
                  <span>{{ item.certification_type }}</span>
                </v-flex>
              </v-col>

            </v-row>
            <v-row>
              <v-col>
                <v-flex class="text-left">Linked Pricing Policy ID</v-flex>
              </v-col>
              <v-col>
                <v-flex class="text-truncate font-weight-bold">
                  <span>{{ item.pricing_policy_id }}</span>
                </v-flex>
              </v-col>

            </v-row>
            <v-row>
              <v-col>
                <v-flex class="text-left">Stellar Payout Address</v-flex>
              </v-col>
              <v-col>
                <v-flex v-if="item.v2address">

                  <span class="stellarv2address">
                    {{ item.v2address }}

                  </span>

                </v-flex>
                <v-dialog>

                </v-dialog>
                <v-flex else>
                  <v-btn
                    x-small
                    @click="openV2AddressDialog = true"
                  >Add V2 Address</v-btn>
                </v-flex>

                <v-flex>
                  <span>
                    {{ item.v2address }}
                  </span>
                </v-flex>
              </v-col>

            </v-row>
            <v-row>
              <v-col>
                <v-flex class="text-left">Bootstrap Node Image</v-flex>
              </v-col>
              <v-col>
                <v-flex>
                  <v-btn
                    x-small
                    v-bind:href="'https://v3.bootstrap.grid.tf/'"
                    target="blank"
                  >view bootstrap</v-btn>

                </v-flex>
              </v-col>

            </v-row>

          </v-container>

        </td>
      </template>
    </v-data-table>

  </v-container>
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
  farms: any = [];
  id: any = [];

  singleExpand = true;
  expanded = [];
  $api: any;
  openV2AddressDialog = false;
  async mounted() {
    this.id = this.$route.query.twinID;

    this.farms = await getFarm(this.$api, this.id);
  }
  async updated() {
    this.id = this.$route.query.twinID;
  }
}
</script>