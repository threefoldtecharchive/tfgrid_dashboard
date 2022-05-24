<template>
  <v-expansion-panels
    v-model="panel"
    :disabled="disabled"
  >
    <v-expansion-panel>
      <v-expansion-panel-header>Public IPs</v-expansion-panel-header>
      <v-expansion-panel-content>
        <v-simple-table class="table">
          <template v-slot:top>
            <v-toolbar flat>
              <v-spacer></v-spacer>
              <CreateIP
                :loadingCreate="loadingCreate"
                @create="createPublicIP"
              />
            </v-toolbar>
          </template>
          <template v-slot:default>
            <thead>
              <tr>
                <th class="text-left">
                  IP
                </th>
                <th class="text-left">
                  Gateway
                </th>
                <th class="text-left">
                  Deployed Contract ID
                </th>
                <th>
                  Actions
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="ip in ips"
                :key="ip.ip"
              >
                <td>{{ decodeHex(ip.ip) }}</td>
                <td>{{ decodeHex(ip.gateway) }}</td>
                <td>{{ ip.contract_id }}</td>
                <td>

                </td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</template>
<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import CreateIP from "./createIP.vue";
import { hex2a } from "@/portal/lib/util";
@Component({
  name: "PublicIPTable",
  components: { CreateIP },
})
export default class PublicIPTable extends Vue {
  panel = [0];
  disabled = false;

  publicIP = "";
  gateway = "";
  ipErrorMessage = "";
  gatewayErrorMessage = "";

  @Prop({ required: true }) ips!: any;
  @Prop({ required: true }) deleteIP!: any;
  @Prop({ required: true }) createIP!: any;
  @Prop({ required: true }) loadingCreate!: boolean;
  public decodeHex(input: string) {
    return hex2a(input);
  }
  createPublicIP(ip: string, gateway: string) {
    this.createIP(ip, gateway);
  }
}
</script>
