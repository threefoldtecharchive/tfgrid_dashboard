<template>
  <Layout pageName="Calculator" :noFilter="true">
    <h1>
      Resources Pricing Calculator
      <i class="fa fa-calculator" aria-hidden="true"></i>
    </h1>
    <v-divider />
    <br />
    <v-card ref="form">
      <div class="card">
        <v-row>
          <v-col cols="5" class="mx-auto">
            <v-text-field
              placeholder="Enter number of CPUs"
              :rules="[...inputValidators]"
              label="CRU"
              suffix="cores"
              v-model="CRU"
              outlined
            ></v-text-field>
          </v-col>
          <v-col cols="5" class="mx-auto">
            <v-text-field
              placeholder="Memory"
              :rules="[...inputValidators]"
              label="MRU"
              suffix="GB"
              v-model="MRU"
              outlined
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="5" class="mx-auto">
            <v-text-field
              placeholder="SSD Storage"
              :rules="[...inputValidators]"
              label="SRU"
              suffix="GB"
              v-model="SRU"
              outlined
            ></v-text-field>
          </v-col>
          <v-col cols="5" class="mx-auto">
            <v-text-field
              placeholder="HDD Storage"
              :rules="[...inputValidators]"
              label="HRU"
              suffix="GB"
              v-model="HRU"
              outlined
            ></v-text-field>
          </v-col>
        </v-row>
      </div>
      <div class="total">
        <span>Total : $ {{ calculate }}</span>
      </div>
    </v-card>
  </Layout>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Layout from "../components/Layout.vue";

@Component({
  components: {
    Layout,
  },
})
export default class Calculator extends Vue {
  CRU = "0";
  SRU = "0";
  MRU = "0";
  HRU = "0";
  formHasErrors = false;

  inputValidators = [
    (val: string) =>
      !isNaN(Number(val)) || "This field must be a number and required",

    (val: string) => Number(val) >= 0 || "This field must be a positive number",
  ];
  get formHasErrrs() {
    return this.$refs.form;
  }
  get calculate() {
    if (
      isNaN(Number(this.CRU)) ||
      isNaN(Number(this.HRU)) ||
      isNaN(Number(this.SRU)) ||
      isNaN(Number(this.MRU)) ||
      Number(this.CRU) < 0 ||
      Number(this.HRU) < 0 ||
      Number(this.SRU) < 0 ||
      Number(this.MRU) < 0
    )
      return 0;
    const cu1 = Math.max(Number(this.CRU) / 2, Number(this.MRU) / 4);
    const cu2 = Math.max(Number(this.CRU), Number(this.MRU) / 8);
    const cu3 = Math.max(Number(this.CRU) / 2, Number(this.MRU) / 4);
    const CU = Math.min(cu1, cu2, cu3);
    const SU = Number(this.HRU) / 1200 + Number(this.SRU) / 200;
    const usd_month = CU * 30.56 + (SU * 19.44 * 24 * 30) / 1000;
    return usd_month.toFixed(3);
  }
}
</script>
<style>
.calc_input {
  width: 100px;
  border-bottom: 1px solid rgb(175, 47, 47);
  padding: 10px;
  font-size: 1.5em;
  font-weight: bold;
  color: #000;
  background-color: #fff;
  outline: none;
}
.card {
  padding: 5rem;
}
.total {
  font-size: 1.7em;
  font-weight: bold;
  color: #000;
  background-color: #fff;
  padding-bottom: 5rem;
  text-align: center;
}
.total span {
  border-bottom: #888 1px solid;
}
</style>
