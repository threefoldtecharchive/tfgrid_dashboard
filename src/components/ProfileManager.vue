<template>
  <v-dialog v-model="open" width="800">
    <template v-slot:activator="{ on, attrs }">
      <v-btn outlined rounded v-bind="attrs" v-on="on">
        <v-icon left> mdi-account </v-icon>
        Profile Manager
      </v-btn>
    </template>

    <v-card>
      <v-card-title class="text-h3"> Profile Manager </v-card-title>
      <v-card-subtitle>
        Please visit
        <a
          class="text-decoration-none"
          href="https://library.threefold.me/info/manual/#/manual__weblets_profile_manager"
          target="_blank"
        >
          the manual
        </a>
        to get started.
      </v-card-subtitle>
      <v-divider />

      <v-card-text class="mt-2 text-body-1">
        <form>
          <v-text-field
            label="Mnemonics"
            placeholder="Mnemonics"
            :type="showPassword ? 'text' : 'password'"
            :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
            @click:append="showPassword = !showPassword"
            autofocus
          />

          <v-textarea label="SSH Key" placeholder="Your Public SSH Key" no-resize />
        </form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({
  name: "ProfileManager",
})
export default class ProfileManager extends Vue {
  open = false;
  showPassword = false;
}
</script>
