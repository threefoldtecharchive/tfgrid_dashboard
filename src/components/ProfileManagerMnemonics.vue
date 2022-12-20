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
    @blur.once="onInput($event.target.value)"
  >
    <template #append-outer>
      <v-btn color="primary" small> Create Account </v-btn>
    </template>
  </v-text-field>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { isMnemonicsExist } from "@/utils";
import { validateMnemonic } from "bip39";
import debounce from "lodash/debounce.js";

@Component({
  name: "ProfileManagerMnemonics",
})
export default class ProfileManagerMnemonics extends Vue {
  showPassword = false;
  loading = false;
  error: string | null = null;

  constructor() {
    super();
    this.__onInput = debounce(this.__onInput.bind(this), 1000) as any;
  }

  onInput(value: string) {
    this.$emit("update:value", value);
    this.loading = true;
    this.__onInput(value);
    this.$emit("update:valid", false);
  }

  private async __onInput(value: string) {
    if (value === "") {
      this.error = "Mnemonics is required.";
    } else if (!validateMnemonic(value)) {
      this.error = "Mnemonic doesn't seem to be valid.";
    } else if (!(await isMnemonicsExist(value))) {
      this.error = "Couldn't load grid using these mnemonic.";
    } else {
      this.error = null;
      this.$emit("update:valid", true);
    }
    this.loading = false;
  }
}
</script>
