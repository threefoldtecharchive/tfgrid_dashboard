<template>
  <Layout pageName="Calculator" :noFilter="true">
    <!-- <div class="d-flex">
      <h1>
        Resources Pricing Calculator
        <i class="fa fa-calculator" aria-hidden="true"></i>
      </h1>
      <span class="link">
        <a href="https://library.threefold.me/info/threefold/#/tfgrid/pricing/threefold__pricing" target="_blank"
          >Threefold Pricing</a
        >
      </span>
    </div>

    <v-divider /> -->

    <v-card class="card ma-md-14 max-w-2xl">
      <v-form v-model="isValidInputs">
        <div>
          <v-row no-gutters>
            <v-col cols="12" md="7" class="mx-auto calcLeft pa-lg-16 pa-4">
              <div class="d-flex mx-lg-10 mb-6">
                <div class="text-xl-h4 text-md-h6">
                  Resources Pricing Calculator
                  <i class="fa fa-calculator" aria-hidden="true"></i>
                </div>
                <span class="link">
                  <a
                    href="https://library.threefold.me/info/threefold/#/tfgrid/pricing/threefold__pricing"
                    target="_blank"
                    >Threefold Pricing</a
                  >
                </span>
              </div>
              <v-tooltip right>
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    class="mx-lg-10 mx-2"
                    placeholder="Enter number of CPUs"
                    :rules="[...inputValidators, cruCheck]"
                    label="CRU"
                    suffix="vCores"
                    v-model="CRU"
                    outlined
                    @input="calculate"
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
                </template>
                <span>CPU</span>
              </v-tooltip>
              <v-tooltip right>
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    class="mx-lg-10 mx-2"
                    placeholder="Memory"
                    :rules="[...inputValidators, mruCheck]"
                    label="MRU"
                    suffix="GB"
                    v-model="MRU"
                    outlined
                    @input="calculate"
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
                </template>
                <span>RAM</span>
              </v-tooltip>
              <v-tooltip right>
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    class="mx-lg-10 mx-2"
                    placeholder="SSD Storage"
                    :rules="[...inputValidators, diskCheck(SRU)]"
                    label="SRU"
                    suffix="GB"
                    v-model="SRU"
                    outlined
                    @input="calculate"
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
                </template>
                <span>SSD</span>
              </v-tooltip>
              <v-tooltip right>
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    class="mx-lg-10 mx-2"
                    placeholder="HDD Storage"
                    :rules="[...inputValidators, diskCheck(HRU)]"
                    label="HRU"
                    suffix="GB"
                    v-model="HRU"
                    outlined
                    @input="calculate"
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
                </template>
                <span>HDD</span>
              </v-tooltip>
              <v-text-field
                class="mx-lg-10 mx-2"
                placeholder="Your Balance"
                :rules="[...inputValidators]"
                label="Your Balance"
                suffix="TFT"
                v-model="balance"
                outlined
                @input="calculate"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="5" class="mx-auto calcRight d-flex pa-4 pa-lg-16">
              <div class="row pb-5 px-4 d-block" v-if="isValidInputs">
                <div
                  class="price-box"
                  v-for="price in prices"
                  :key="price.price"
                  :style="{ color: price.color, background: price.backgroundColor }"
                >
                  <div class="price">
                    <div class="name">
                      {{ price.label !== undefined ? price.label + " " : " " }}
                      {{ price.packageName != "none" ? price.packageName + " Package" : "" }}
                    </div>
                    <div class="priceMonth my-2">${{ price.price }}/month,</div>
                    <div class="tftMonth my-2">{{ price.TFTs }} TFT/month</div>
                  </div>
                </div>
              </div>
            </v-col>
          </v-row>
        </div>
      </v-form>
    </v-card>
  </Layout>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Layout from "../components/Layout.vue";
import { calCU, calSU, getPrices } from "../../portal/lib/nodes";

type priceType = {
  label?: string;
  color: string;
  price: string;
  packageName: any;
  backgroundColor: string;
  TFTs: any;
};

@Component({
  components: {
    Layout,
  },
})
export default class Calculator extends Vue {
  CRU = "1";
  SRU = "25";
  MRU = "1";
  HRU = "100";
  balance = "0";
  prices: priceType[] | [] = [];
  $api: any;
  discountPackages: any = {};
  formHasErrors = false;
  pricing: any;
  TFTPrice: number | undefined;
  isValidInputs = true;
  cruCheck() {
    // eslint-disable-next-line
    const CRURegex = /^\d+$/;
    if (!this.CRU) {
      return "This value is required";
    }
    if (+this.CRU === 0 || +this.CRU > 256) {
      return "CRU value must be between 1 and 256";
    }
    if (CRURegex.test(this.CRU)) {
      return true;
    } else {
      return "CRU value must be a positive integer";
    }
  }
  mruCheck() {
    if (!this.MRU) {
      return "This value is required";
    }
    if (+this.MRU > 1024) {
      return "Maximum allowed MRU value is 1024";
    } else {
      return true;
    }
  }
  diskCheck(val: string) {
    if (+val > 1000000) {
      return "Maximum disk size is 1000000 GB";
    } else if (!val) {
      return "disk field is required";
    } else {
      return true;
    }
  }
  inputValidators = [
    (val: string) => !isNaN(+val) || "This field must be a number",
    (val: string) => +val >= 0 || "This field must be a positive number",
  ];
  get formHasErrrs() {
    return this.$refs.form;
  }
  async created() {
    await this.calculate();
  }

  async calculate() {
    if (!this.isValidInputs) return;
    else if (this.$api) {
      if (
        isNaN(+this.balance) ||
        isNaN(+this.CRU) ||
        isNaN(+this.HRU) ||
        isNaN(+this.SRU) ||
        isNaN(+this.MRU) ||
        +this.balance < 0 ||
        +this.CRU < 0 ||
        +this.HRU < 0 ||
        +this.SRU < 0 ||
        +this.MRU < 0
      ) {
        return;
      }
      this.TFTPrice = await this.getTFTPrice(this.$api);
      const price = await this.calcPrice();
      const CU = calCU(+this.CRU, +this.MRU);
      const SU = calSU(+this.HRU, +this.SRU);
      const musd_month = (CU * price.cu.value + SU * price.su.value) * 24 * 30;
      const usd_month = (musd_month / 10000000).toFixed(2);
      const [priceNumber, selectedPackage] = await this.calDiscount(musd_month);
      this.prices = [
        {
          label: "Dedicated Node Price",
          price: `${priceNumber}`,
          color: this.discountPackages[selectedPackage].color,
          packageName: selectedPackage,
          backgroundColor: this.discountPackages[selectedPackage].backgroundColor,
          TFTs: (+priceNumber / this.TFTPrice).toFixed(2),
        },
        {
          label: "Shared Node Price",
          price: `${usd_month}`,
          color: "#868686",
          packageName: "none",
          backgroundColor: this.discountPackages.none.backgroundColor,
          TFTs: (+usd_month / this.TFTPrice).toFixed(2),
        },
      ];
    } else {
      this.$router.push({
        name: "accounts",
        path: "/",
      });
      return;
    }
  }

  async calcPrice() {
    const price = await getPrices(this.$api);
    return price;
  }

  async calDiscount(price: number) {
    this.pricing = await this.calcPrice();
    // discount for Dedicated Nodes
    const discount = this.pricing.discountForDedicationNodes;
    let totalPrice = price - price * (discount / 100);
    // discount for Twin Balance in TFT
    const balance = (this.TFTPrice ? this.TFTPrice : 1) * +this.balance * 10000000;

    this.discountPackages = {
      none: {
        duration: 0,
        discount: 0,
        backgroundColor: "#CCC",
        color: "rgba(0,0,0)",
      },
      default: {
        duration: 3,
        discount: 20,
        backgroundColor: "#a5e1ff",
        color: "rgba(0,0,0)",
      },
      bronze: {
        duration: 6,
        discount: 30,
        backgroundColor: `linear-gradient(to right, #7f5747, #c5a597, #ffe8d4, #cca68b, #754e3f)`,
        color: "rgba(0,0,0)",
      },
      silver: {
        duration: 12,
        discount: 40,
        backgroundColor: `linear-gradient(to right, #959595, #f5f5f5, #d3d3d3, #e9e9e9, #7f7f7f)`,
        color: "rgba(0,0,0)",
      },
      gold: {
        duration: 36,
        discount: 60,
        backgroundColor: `linear-gradient(to right, #BF953F, #FCF6BA, #d7ae56, #FBF5B7, #AA771C)`,
        color: "rgba(0,0,0)",
      },
    };

    let selectedPackage = "none";
    for (let pkg in this.discountPackages) {
      if (balance > totalPrice * this.discountPackages[pkg].duration) {
        selectedPackage = pkg;
      }
    }
    totalPrice = (totalPrice - totalPrice * (this.discountPackages[selectedPackage].discount / 100)) / 10000000;
    return [totalPrice.toFixed(2), selectedPackage];
  }

  async getTFTPrice(api: { query: { tftPriceModule: { tftPrice: any } } }) {
    const pricing = await api.query.tftPriceModule.tftPrice();
    return pricing.words[0] / 1000;
  }
}
</script>
<style>
.right {
  text-align: right;
  margin-right: 0;
  margin-left: auto;
}
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

.calcRight {
  background-color: #333333;
  align-items: center;
  justify-content: center;
  border-top-right-radius: 4px;
  border-bottom-right-radius: 4px;
  margin: 0px;
  padding: 0px;
}

.price-box {
  font-size: 1.3rem;
  font-weight: bold;
  text-align: center;
  margin: 1rem auto;
  border-radius: 5px;
  box-shadow: 5px 5px 4px #1e1e1e;
}
.price {
  display: block;
  padding: 1.2rem;
  margin: 20px auto;
  text-align: center;
}
.name {
  font-weight: 600;
  font-size: 18px;
  text-transform: capitalize;
  margin: 10px 0;
}

.priceMonth {
  font-size: 35px;
  border-bottom: 1px solid;
}

.tftMonth {
  font-size: 25px;
}
.link {
  align-self: end;
  display: inline-block;
  margin-left: 1rem;
  margin-bottom: 0.3rem;
}
</style>
