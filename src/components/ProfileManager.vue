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
        <form class="pt-2">
          <ProfileManagerMnemonics :value.sync="form.mnemonic.value" :valid.sync="form.mnemonic.valid" />

          <v-textarea label="SSH Key" placeholder="Your Public SSH Key" no-resize>
            <template #append-outer>
              <v-btn color="primary" small> Generate SSH Key </v-btn>
            </template>
          </v-textarea>
          {{ form }}
        </form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import ProfileManagerMnemonics from "./ProfileManagerMnemonics.vue";

class ProfileForm {
  mnemonic = { value: "", valid: false };
  ssh = { value: "", valid: false };

  get valid(): boolean {
    return this.mnemonic.valid && this.ssh.valid;
  }

  get value() {
    const { mnemonic, ssh } = this;
    return { mnemonic: mnemonic.value, ssh: ssh.value };
  }
}

@Component({
  name: "ProfileManager",
  components: { ProfileManagerMnemonics },
})
export default class ProfileManager extends Vue {
  open = false;

  form = new ProfileForm();
}
</script>
