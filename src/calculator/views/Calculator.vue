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
            <v-tooltip right>
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  placeholder="Enter number of CPUs"
                  :rules="[...inputValidators]"
                  label="CRU"
                  suffix="Cores"
                  v-model="CRU"
                  outlined
                  @input="calculate"
                  v-bind="attrs"
                  v-on="on"
                ></v-text-field>
              </template>
              <span>CPU</span>
            </v-tooltip>

          </v-col>
          <v-col cols="5" class="mx-auto">
            <v-tooltip right>
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  placeholder="Memory"
                  :rules="[...inputValidators]"
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
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="5" class="mx-auto">
            <v-tooltip right>
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  placeholder="SSD Storage"
                  :rules="[...inputValidators]"
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
          </v-col>
          <v-col cols="5" class="mx-auto">
            <v-tooltip right>
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  placeholder="HDD Storage"
                  :rules="[...inputValidators]"
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
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="5" class="mx-auto">
            <v-text-field
              placeholder="Your Balance"
              :rules="[...inputValidators]"
              label="Your Balance"
              suffix="USD"
              v-model="balance"
              outlined
              @input="calculate"
            ></v-text-field>
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
            <span class="name">
              {{ price.label !== undefined ? price.label + " " : " " }}
              {{ price.packageName != "none" ? price.packageName + " Package" : "" }}</span>
            : ${{ price.price }}
          </span>
          <p class="price">
            <span class="name">TFT Count:</span>
            {{price.TFTs}}
            </p>
        </div>
        <span class="right"
          >learn more about pricing through this <a href="https://library.threefold.me/info/threefold/#/tfgrid/pricing/threefold__pricing" target="_blank">link</a></span
        >
      </div>
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
  inputValidators = [
    (val: string) =>
      !isNaN(+(val)) || "This field must be a number and required",

    (val: string) => +(val) >= 0 || "This field must be a positive number",
  ];
  get formHasErrrs() {
    return this.$refs.form;
  }
  async calculate() {
    if (this.$api) {
      if (
        isNaN(+(this.balance)) ||
        isNaN(+(this.CRU)) ||
        isNaN(+(this.HRU)) ||
        isNaN(+(this.SRU)) ||
        isNaN(+(this.MRU)) ||
        +(this.balance) < 0 ||
        +(this.CRU) < 0 ||
        +(this.HRU) < 0 ||
        +(this.SRU) < 0 ||
        +(this.MRU) < 0
      ) {
        this.prices = [
          {
            price: "0.0",
            color: "black",
            packageName: "none",
            backgroundColor: "#DaDaDa",
            TFTs: 0
          },
        ];        
        return;
      }
      this.TFTPrice = await this.getTFTPrice(this.$api)
      const price = await this.calcPrice();
      const CU = calCU(+this.CRU, +this.MRU);
      const SU = calSU(+this.HRU, +this.SRU);
      const musd_month = (CU * price.cu.value + SU * price.su.value) * 24 * 30;
      const usd_month = (musd_month / 10000000).toFixed(2);
      const [priceNumber, selectedPackage] = await this.calDiscount(musd_month);
      const sharedTFTPrice = `${this.TFTPrice} * ${priceNumber}`;

      this.prices = [
        {
          label: "Dedicated Node Price",
          price: `${priceNumber}`,
          color: this.discountPackages[selectedPackage].color,
          packageName: selectedPackage,
          backgroundColor:
            this.discountPackages[selectedPackage].backgroundColor,
          TFTs: +priceNumber / this.TFTPrice 
            
        },
        {
          label: "Shared Node Price",
          price: `${usd_month}`,
          color: "#868686",
          packageName: "none",
          backgroundColor: this.discountPackages.none.backgroundColor,
          TFTs: +usd_month / this.TFTPrice
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

  async calcPrice(){
    const price = await getPrices(this.$api);
    return price;
  }

  async calDiscount(price: number) {
  this.pricing = await this.calcPrice();
  // discount for Dedicated Nodes
  const discount = this.pricing.discountForDedicationNodes;
  let totalPrice = price - price * (discount / 100);    
  // discount for Twin Balance
  const balance = +(this.balance) * 10000000;
   this.discountPackages = {
    "none": {
      duration: 0,
      discount: 0,
      backgroundColor: "#CCCCCC",
      color: "#868686",
    },
    "default": {
      duration: 3,
      discount: 20,
      backgroundColor: "#3b3b3b",
      color: "black",
    },
    "bronze": {
      duration: 6,
      discount: 30,
      backgroundColor: "#F7B370",
      color: "#C17427",
    },
    "silver": {
      duration: 12,
      discount: 40,
      backgroundColor: "#eeeeee",
      color: "#a9a9a9",
    },
    "gold": {
      duration: 36,
      discount: 60,
      backgroundColor: "#ffed8b",
      color:"rgba(0,0,0,.4)"

    },
  };
  
  let selectedPackage = "none";  
  for (let pkg in this.discountPackages) {
    if (balance > totalPrice * this.discountPackages[pkg].duration) {
      selectedPackage = pkg;
    }
  }  
  totalPrice = (totalPrice - totalPrice * (this.discountPackages[selectedPackage].discount / 100) ) / 10000000;  
  return [totalPrice.toFixed(2), selectedPackage];
}

  async getTFTPrice(api: {query: { tftPriceModule: { tftPrice: any }}}){    
    const pricing = await api.query.tftPriceModule.tftPrice();
    console.log("pricing", pricing.words[0]/1000);
    return pricing.words[0]/1000;
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
