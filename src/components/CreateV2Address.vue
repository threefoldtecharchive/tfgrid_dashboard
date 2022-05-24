<template>
  <div>
    <v-dialog
      v-model="open"
      width="500"
    >
      <template v-slot:activator="{ on, attrs }">
        <a
          v-bind="attrs"
          v-on="on"
          class="link"
        >
          {{ text }}
        </a>
      </template>

      <v-card>
        <v-card-title class="text-h5">
          Add V2 Stellar address
        </v-card-title>

        <v-card-text>
          <div class="text">
            <v-text-field
              label="Stellar wallet address"
              v-model="address"
              required
              :error-messages="errorMessages"
              :rules="[
                () => !!address || 'This field is required',
                addressCheck
              ]"
            ></v-text-field>
          </div>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            text
            @click="open = false"
          >
            Close
          </v-btn>
          <v-btn
            :disabled="!!errorMessages"
            color="primary"
            text
            @click="addAddress()"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
<script >
import stellar from "stellar-sdk";
import config from "../../config";

const TFT_ASSET = "TFT";
const server = new stellar.Server(config.horizonUrl);

export default {
  name: "CreateV2Address",
  props: ["addV2Address", "loading", "text"],

  data: () => {
    return {
      open: false,
      address: "",
      errorMessages: "",
    };
  },
  methods: {
    addAddress() {
      this.open = false;
      console.log(this.address);
      this.addV2Address(this.address);
    },
    async addressCheck() {
      try {
        // check if the account provided exists on stellar
        const account = await server.loadAccount(this.address);
        // check if the account provided has the appropriate trustlines
        const includes = account.balances.find(
          (b) =>
            b.asset_code === TFT_ASSET &&
            b.asset_issuer === config.tftAssetIssuer
        );
        if (!includes) {
          this.errorMessages = "Address does not have a valid trustline to TFT";
          return false;
        }
      } catch (error) {
        this.errorMessages = "Address not found";
        return false;
      }

      this.errorMessages = "";
      return true;
    },
  },
};
</script>
<style scoped>
.v-main {
  background-color: rgb(236, 236, 236) !important;
}
.text {
  margin-top: 2em !important;
}
.link {
  color: white !important;
  text-decoration: underline;
}
.v-card {
  background: #252c48 !important;
}
</style>