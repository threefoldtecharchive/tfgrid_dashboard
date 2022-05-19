<template>
  <v-card flat color="transparent">
    <v-subheader>{{ label.toLocaleUpperCase() }}</v-subheader>
    <v-text-field
      type="number"
      :label="label"
      solo
      :prefix="prefix"
      clearable
      v-model="value"
    />
  </v-card>
</template>
<script lang="ts">
import { MutationTypes } from "../store/mutations";
import { IState } from "../store/state";
import { IOP } from "../utils/filters";
import { Component, Prop, Vue } from "vue-property-decorator";

@Component({})
export default class ComparisonFilter extends Vue {
  @Prop({ required: true }) key1!: keyof IState["filters"];
  @Prop({ required: true }) key2!: string;
  @Prop({ required: true }) label!: string;
  @Prop({ required: true }) prefix!: IOP;

  get value() {
    return this.$store.getters["explorer/getFilter"](this.key1, this.key2)
      .value;
  }

  set value(value: number) {
    this.$store.commit(MutationTypes.SET_FILTER_VALUE, {
      key1: this.key1,
      key2: this.key2,
      value,
    });
  }

  created() {
    this.$store.commit(MutationTypes.SET_FILTER_ENABLE, {
      key1: this.key1,
      key2: this.key2,
      value: true,
    });
  }

  destroyed() {
    this.$store.commit(MutationTypes.SET_FILTER_ENABLE, {
      key1: this.key1,
      key2: this.key2,
      value: false,
    });
  }
}
</script>
