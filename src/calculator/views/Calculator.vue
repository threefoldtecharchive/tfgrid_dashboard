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
        <v-row>
          <v-col cols="5" class="mx-auto">
            <v-text-field
              placeholder="Your Balance"
              :rules="[...inputValidators]"
              label="Your Balance"
              suffix="TFT"
              v-model="balance"
              outlined
            ></v-text-field>
          </v-col>
          <v-col cols="5" class="mx-auto">
            <v-switch
              color="primary"
              :label="`${switchLabel ? 'Dedicated Nodes' : 'Shared Nodes'}`"
              v-model="switchLabel"
            ></v-switch>
          </v-col>
        </v-row>
      </div>
      <div class="row pb-5 px-4 mx-5">
        <div
          class="col-5 price-box"
          v-for="price in prices"
          :key="price.price"
          :style="{ color: price.color, background: price.backgroundColor }"
        >
          <span class="price">
            <span class="name">{{ price.packageName }}</span>
            : $ {{ price.price }}
          </span>
        </div>
      </div>
    </v-card>
  </Layout>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Layout from "../components/Layout.vue";
import { getPrices } from "../../portal/lib/nodes";

type priceType = {
  color: string;
  price: string;
  packageName: string;
  backgroundColor: string;
};

@Component({
  components: {
    Layout,
  },
})
export default class Calculator extends Vue {
  CRU = "0";
  SRU = "0";
  switchLabel = "Dedicated Nodes";
  MRU = "0";
  HRU = "0";
  balance = "0";
  prices: priceType[] | [] = [];
  $api: any;
  discountPackages: any = {
    none: {
      backgroundColor: "#CCCCCC",
      color: "#868686",
      discount: 0,
    },
    default: {
      backgroundColor: "#3b3b3b",
      color: "black",
      discount: 20,
    },
    bronze: {
      backgroundColor: "#F7B370",
      color: "#C17427",
      discount: 30,
    },
    silver: {
      backgroundColor: "#eeeeee",
      color: "#a9a9a9",
      discount: 40,
    },
    gold: {
      backgroundColor: "#ffed8b",
      color: "#FFD700",
      discount: 60,
    },
  };

  formHasErrors = false;

  inputValidators = [
    (val: string) =>
      !isNaN(Number(val)) || "This field must be a number and required",

    (val: string) => Number(val) >= 0 || "This field must be a positive number",
  ];
  get formHasErrrs() {
    return this.$refs.form;
  }
  updated(){
    this.calculate();
  }
  async calculate(){
    // todo: calculate the price
    console.log(this.$api + "sss");
    console.log(this.$store.state.portal.accounts);

    if (this.$api) {
      if (
        isNaN(Number(this.balance)) ||
        isNaN(Number(this.CRU)) ||
        isNaN(Number(this.HRU)) ||
        isNaN(Number(this.SRU)) ||
        isNaN(Number(this.MRU)) ||
        Number(this.CRU) < 0 ||
        Number(this.HRU) < 0 ||
        Number(this.SRU) < 0 ||
        Number(this.MRU) < 0
      )
        this.prices= [
          {
            price: "0.0",
            color: "black",
            packageName: "none",
            backgroundColor: "#DaDaDa",
          },
        ];
      const cu1 = Math.max(Number(this.CRU) / 2, Number(this.MRU) / 4);
      const cu2 = Math.max(Number(this.CRU), Number(this.MRU) / 8);
      const cu3 = Math.max(Number(this.CRU) / 2, Number(this.MRU) / 4);
      const CU = Math.min(cu1, cu2, cu3);
      const SU = Number(this.HRU) / 1200 + Number(this.SRU) / 200;
      const usd_month = ((CU * 30.56 + SU * 19.44) * 24 * 30) / 1000;

      /*   for (const key in this.discountPackages) {
        prices.push({
          price: `${(
            (usd_month * (100 - this.discountPackages[key].discount)) /
            100
          ).toFixed(3)}`,
          color: this.discountPackages[key].color,
          packageName: key,
          backgroundColor: this.discountPackages[key].backgroundColor,
        });
      } */
      const [priceNumber, selectedPackage] = await this.calDiscount(usd_month);
      const price = [
        {
          price: `${priceNumber}`,
          color: this.discountPackages[selectedPackage].color,
          packageName: selectedPackage,
          backgroundColor:
            this.discountPackages[selectedPackage].backgroundColor,
        },
      ];

      this.prices = price;
    } else {
      this.$router.push({
        name: "accounts",
        path: "/",
      });
      return [];
    }
  }
  async calDiscount(price: number): Promise<[string, string]> {
    // discount for Dedicated Nodes

    const pricing = await getPrices(this.$api);
    const discount = pricing.discountForDedicationNodes;
    let totalPrice = price - price * (discount / 100);

    // discount for Twin Balance

    const discountPackages: any = {
      none: {
        duration: 0,
        discount: 0,
      },
      default: {
        duration: 3,
        discount: 20,
      },
      bronze: {
        duration: 6,
        discount: 30,
      },
      silver: {
        duration: 12,
        discount: 40,
      },
      gold: {
        duration: 36,
        discount: 60,
      },
    };

    let selectedPackage = "none";

    for (const pkg in discountPackages) {
      if (Number(this.balance) > totalPrice * discountPackages[pkg].duration) {
        selectedPackage = pkg;
      }
    }

    totalPrice =
      totalPrice -
      totalPrice * (discountPackages[selectedPackage].discount / 100);

    return [totalPrice.toFixed(2), selectedPackage];
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
.price-box {
  font-size: 1.3rem;
  font-weight: bold;
  text-align: center;

  margin: 0.2rem auto;
  border-radius: 5px;
}
.price {
  display: block;
  padding: 0.7rem;
  display: inline-block;
  margin: 0 auto;
  text-align: center;
}

.name {
  font-weight: 900;
  text-transform: capitalize;
}
</style>
