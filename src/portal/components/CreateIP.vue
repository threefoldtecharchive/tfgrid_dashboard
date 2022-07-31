<template>
  <v-container>
    <v-dialog
      v-model="open"
      width="500"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="primary"
          v-bind="attrs"
          v-on="on"
          :loading="loadingCreate"
          x-small
        >
          Add IP
        </v-btn>
      </template>

      <v-card>
        <v-card-title class="text-h5">
          Add Public IP to Farm
        </v-card-title>

        <v-card-text class="text">
          <v-text-field
            label="IP"
            v-model="publicIP"
            required
            outlined
            dense
            hint="IP address in CIDR format xxx.xx.xx.xx/xx"
            persistent-hint
            :rules="[
              () => !!publicIP || 'This field is required',
              () => ipcheck() || 'incorrect format'
            ]"
          ></v-text-field>
          <v-text-field
            label="Gateway"
            v-model="gateway"
            required
            outlined
            dense
            hint="Gateway for the IP in ipv4 format"
            persistent-hint
            :error-messages="gatewayErrorMessage"
            :rules="[
              () => !!gateway || 'This field is required',
              gatewayCheck
            ]"
          ></v-text-field>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="grey lighten-2 black--text"
            @click="open = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="primary white--text"
            text
            @click="createPublicIP()"
            :disabled="!!ipErrorMessage || !!gatewayErrorMessage || publicIP === '' || gateway === ''"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>
<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";

@Component({
  name: "CreateIP",
})
export default class CreateIP extends Vue {
  publicIP = "";
  gateway = "";
  ipErrorMessage = "";
  gatewayErrorMessage = "";
  open = false;

  @Prop({ required: true }) loadingCreate!: boolean;
  createPublicIP() {
    this.open = false;
    this.$emit("create", this.publicIP, this.gateway);
  }
  ipcheck() {
    const ipRegex = new RegExp("^(?:[0-9]{1,3}.){3}[0-9]{1,3}/(16|24)$");
    if (ipRegex.test(this.publicIP)) {
      return true;
    }
    return false;
  }
  gatewayCheck() {
    if (this.gateway === "") {
      this.ipErrorMessage = "";
      return true;
    }

    const gatewayRegex = new RegExp("^(?:[0-9]{1,3}.){3}[0-9]{1,3}$");
    if (gatewayRegex.test(this.gateway)) {
      this.gatewayErrorMessage = "";
      return true;
    } else {
      this.gatewayErrorMessage = "Gateway is not formatted correctly";
      return false;
    }
  }
}
</script>
