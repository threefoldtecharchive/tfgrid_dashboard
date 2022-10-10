<template>
  <v-card flat color="transparent">
    <v-subheader>{{ label.toLocaleUpperCase() }}</v-subheader>
    <v-combobox
      v-model="items"
      :items="_values"
      chips
      clearable
      :label="label"
      multiple
      solo
      type="text"
      @input.native="validated($event.srcElement.value, filterKey)"
    >
      <template v-slot:selection="{ attrs, item, select, selected }">
        <v-chip
          v-bind="attrs"
          :input-value="selected"
          close
          @click="select"
          @click:close="remove(item)"
        >
          <strong>{{ item }}</strong>
        </v-chip>
      </template>
    </v-combobox>
    <v-alert dense type="error" v-if="errorMsg">
      {{ errorMsg }}
    </v-alert>
  </v-card>
</template>


<script lang="ts">
import { MutationTypes } from "../store/mutations";
import { Component, Prop, Vue } from "vue-property-decorator";
import { inputValidation } from "../utils/validations";

@Component({})
export default class InFilter extends Vue {
  @Prop({ required: true }) label!: string;
  @Prop({ required: true }) filterKey!: string;
  @Prop() value?: string[];

  get _values(): (string | number)[] {
    // values are the suggested options
    return [];
  }

  get filters(): string[] {
    return this.$store.getters["explorer/getNodesFilter"][this.filterKey];
  }

  set filters(payload: any) {
    this.$store.commit("explorer/" + MutationTypes.SET_NODES_FILTER, {
      key: this.filterKey,
      value: this.value,
    });
  }

  get items(): string[] {
    return [];
  }

  set items(value: string[]) {
    this.$store.commit("explorer/" + MutationTypes.SET_NODES_FILTER, {
      key: this.filterKey,
      value,
    });
    this.$store.dispatch("explorer/loadNodesData");
  }

  // UI creation/deletion

  remove(item: string): void {
    // remove from UI, clearing a single filter value
    const filters = this.filters;
    const idx = filters.findIndex((i) => i == item);
    if (idx > -1) {
      filters.splice(idx, 1);
      this.filters = filters;
    }

    // remove from store
    this.$store.commit("explorer/" + MutationTypes.CLEAR_NODES_FILTER_KEY, this.filterKey)

    // reload nodes
    this.$store.dispatch("explorer/loadNodesData");
  }

  errorMsg: any = "";
  validated(value: string, key: string): string {
    this.errorMsg = inputValidation(value, key);
    return this.errorMsg;
  }

  created() {
    this.$store.commit("explorer/" + MutationTypes.SET_FILTER_ENABLE, {
      key1: "nodes",
      key2: this.filterKey,
      value: true,
    });
  }

  destroyed() {
    // Destroying is clearing the filed.
    this.$store.commit("explorer/" + MutationTypes.SET_FILTER_ENABLE, {
      key1: "nodes",
      key2: this.filterKey,
      value: false,
    });

    this.$store.commit("explorer/" + MutationTypes.CLEAR_NODES_FILTER)

    // reload nodes
    this.$store.dispatch("explorer/loadNodesData");
  }
}
</script>