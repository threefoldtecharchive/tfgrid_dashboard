<template>
  <v-card flat color="transparent">
    <v-subheader>{{ label.toLocaleUpperCase() }}</v-subheader>
    <v-combobox
      v-model="items"
      :items="_values"
      chips
      clearable
      :label="label"
      :multiple="multiple"
      solo
      type="text"
      @input.native="validated($event.srcElement.value, filterKey)"
    >
      <template v-slot:selection="{ attrs, item, select, selected, index }">
        <v-chip
          v-bind="attrs"
          :input-value="selected"
          :close="multiple"
          @click="select"
          @click:close="remove(index)"
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
import { ActionTypes } from "../store/actions";

@Component({})
export default class InFilter extends Vue {
  @Prop({ required: true }) label!: string;
  @Prop({ required: true }) filterKey!: string;
  @Prop() value?: string[];

  get multiple() {
    return this.filterKey == "farm_ids";
  }

  get _values(): (string | number)[] {
    // values are the suggested options; not needed for now.
    return [];
  }

  get items(): string[] {
    return this.$store.getters["explorer/getNodesFilter"][this.filterKey];
  }

  set items(value: string[]) {
    this.$store.commit("explorer/" + MutationTypes.SET_NODES_FILTER, {
      key: this.filterKey,
      value,
    });
    this.$store.dispatch(ActionTypes.REQUEST_NODES);
  }

  remove(index: number): void {
    this.$store.getters["explorer/getNodesFilter"][this.filterKey].splice(
      index,
      1
    );

    this.$store.dispatch(ActionTypes.REQUEST_NODES);
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
    this.$store.commit("explorer/" + MutationTypes.SET_FILTER_ENABLE, {
      key1: "nodes",
      key2: this.filterKey,
      value: false,
    });
    this.$store.commit(
      "explorer/" + MutationTypes.CLEAR_NODES_FILTER_KEY,
      this.filterKey
    );
    this.$store.dispatch(ActionTypes.REQUEST_NODES);
  }
}
</script>