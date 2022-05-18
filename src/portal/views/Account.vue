<template>
  <v-container>

    <v-card
      color="#388E3C"
      class="text-center pa-5 my-3 "
    >
      <h2>
        Welcome aboard {{$route.query.accountName}}, <br>
        Let’s get you connected to the TF Grid !
      </h2>
    </v-card>
    <v-card
      color="#512DA8"
      class="text-center pa-5"
    >
      <h3>Choose your preferred method : </h3>
    </v-card>
    <v-container>
      <v-row>
        <v-col>
          <v-card>
            <p>
              Create a Twin using Planetary
              using Yggdrasil IPV6
            </p>
          </v-card>
        </v-col>
        <v-col>
          <v-card>
            <p>
              Create a Twin automatically
            </p>
          </v-card>
        </v-col>

      </v-row>

    </v-container>
  </v-container>

</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({
  name: "AccountView",
})
export default class AccountView extends Vue {}
</script>