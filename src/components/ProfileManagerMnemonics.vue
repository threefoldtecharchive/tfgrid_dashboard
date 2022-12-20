<template>
  <v-text-field
    label="Mnemonics"
    placeholder="Mnemonics"
    :type="showPassword ? 'text' : 'password'"
    :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
    @click:append="showPassword = !showPassword"
    autofocus
    dense
    @input="onInput"
    :error-messages="loading ? undefined : error"
    :loading="loading"
    :disabled="loading"
    v-model="mnemonics"
  >
    <template #append-outer>
      <v-btn @click="onCreateAccount" color="primary" small :loading="loading" :disabled="valid || loading">
        Create Account
      </v-btn>
    </template>
  </v-text-field>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import { isMnemonicsExist } from "@/utils";
import { validateMnemonic } from "bip39";
import debounce from "lodash/debounce.js";
import { GridClient, NetworkEnv } from "grid3_client";
import { HTTPMessageBusClient } from "ts-rmb-http-client";

@Component({
  name: "ProfileManagerMnemonics",
})
export default class ProfileManagerMnemonics extends Vue {
  showPassword = false;
  loading = false;
  error: string | null = null;
  valid = false;
  mnemonics = "";

  constructor() {
    super();
    this.__onInput = debounce(this.__onInput.bind(this), 1000) as any;
  }

  mounted() {
    const mnemonics = sessionStorage.getItem("mnemonics");
    if (mnemonics) {
      this.mnemonics = mnemonics;
      this.$emit("update:value", mnemonics);
      this.valid = true;
    }
  }

  onInput(value: string) {
    this.$emit("update:value", value);
    this.__onInput(value);
    this.valid = false;
  }

  private async __onInput(value: string) {
    this.loading = true;
    sessionStorage.removeItem("mnemonics");
    if (value === "") {
      this.error = "Mnemonics is required.";
    } else if (!validateMnemonic(value)) {
      this.error = "Mnemonic doesn't seem to be valid.";
    } else if (!(await isMnemonicsExist(value))) {
      this.error = "Couldn't load grid using these mnemonic.";
    } else {
      this.error = null;
      this.valid = true;
      sessionStorage.setItem("mnemonics", value);
    }
    this.loading = false;
  }

  @Watch("valid", { immediate: true })
  onValidChange(valid: boolean) {
    this.$emit("update:valid", valid);
  }

  async onCreateAccount() {
    this.loading = true;
    const grid = new GridClient(
      window.configs.APP_NETWORK as unknown as NetworkEnv,
      "",
      "test",
      new HTTPMessageBusClient(0, "", "", ""),
    );
    grid._connect();
    await grid.tfchain
      .createAccount("::1")
      .then(({ mnemonic }) => {
        this.mnemonics = mnemonic;
        this.onInput(mnemonic);
      })
      .catch(err => {
        console.error({ err });
        this.loading = false;
      });
  }
}
</script>
