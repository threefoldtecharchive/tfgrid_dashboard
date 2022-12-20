<template>
  <v-textarea
    label="SSH Key"
    placeholder="Your Public SSH Key"
    no-resize
    @input="onInput"
    @blur.once="onInput($event.target.value)"
    :error-messages="error"
    :spellcheck="false"
    v-model="ssh"
    :disabled="loading || disabled"
  >
    <template #append-outer>
      <v-btn color="primary" small :loading="loading" :disabled="valid || loading || disabled">
        Generate SSH Key
      </v-btn>
    </template>
  </v-textarea>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import { isValidSSH, getGrid } from "@/utils";

function loadSSH(mnemonics: string): Promise<string | null> {
  return getGrid(mnemonics)
    .then(grid => grid.kvstore.get({ key: "metadata" }))
    .then(value => JSON.parse(value).sshkey)
    .catch(() => null);
}

function storeSSH(mnemonics: string, sshkey: string): Promise<boolean> {
  return getGrid(mnemonics)
    .then(grid => grid.kvstore.set({ key: "metadata", value: JSON.stringify({ sshkey }) }))
    .then(() => true)
    .catch(() => false);
}

@Component({
  name: "ProfileManagerSSH",
})
export default class ProfileManagerSSH extends Vue {
  @Prop({ default: false }) disabled!: boolean;
  error: string | null = null;
  valid = false;
  ssh = "";
  loading = false;

  onInput(value: string) {
    this.$emit("update:value", value);
    this.error = null;
    if (value === "") {
      this.error = "Public SSH Key is required.";
    } else if (!isValidSSH(value)) {
      this.error = "Public SSH Key doesn't seem to be valid.";
    }
    this.valid = !this.error;
  }

  @Watch("valid", { immediate: true })
  onValidChange(valid: boolean) {
    this.$emit("update:valid", valid);
  }

  @Watch("ssh")
  async onSSHChange() {
    this.loading = true;
    const mnemonics = sessionStorage.getItem("mnemonics");
    if (mnemonics && this.valid) {
      const value = await loadSSH(mnemonics);
      if (value !== this.ssh) {
        await storeSSH(mnemonics, this.ssh);
      }
    }
    this.loading = false;
  }

  @Watch("disabled", { immediate: true })
  async onDisabledChange() {
    if (!this.disabled) {
      requestAnimationFrame(async () => {
        try {
          this.loading = true;
          const mnemonics = sessionStorage.getItem("mnemonics");
          const value = await loadSSH(mnemonics!);
          if (value) {
            this.ssh = value;
            this.$emit("update:value", value);
            this.valid = true;
          }
        } catch {
          /* pass */
        }
        this.loading = false;
      });
    }
  }
}
</script>
