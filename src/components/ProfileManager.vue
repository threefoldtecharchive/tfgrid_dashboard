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
          <ProfileManagerMnemonics :value.sync="form.mnemonics.value" :valid.sync="form.mnemonics.valid" />
          <ProfileManagerSSH
            :value.sync="form.ssh.value"
            :valid.sync="form.ssh.valid"
            :disabled="!form.mnemonics.valid"
          />
        </form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import ProfileManagerMnemonics from "./ProfileManagerMnemonics.vue";
import ProfileManagerSSH from "./ProfileManagerSSH.vue";

class ProfileForm {
  mnemonics = { value: "", valid: false };
  ssh = { value: "", valid: false };

  get valid(): boolean {
    return this.mnemonics.valid && this.ssh.valid;
  }

  get value() {
    const { mnemonics, ssh } = this;
    return { mnemonics: mnemonics.value, ssh: ssh.value };
  }
}

@Component({
  name: "ProfileManager",
  components: { ProfileManagerMnemonics, ProfileManagerSSH },
})
export default class ProfileManager extends Vue {
  open = true;
  form = new ProfileForm();
}
</script>
