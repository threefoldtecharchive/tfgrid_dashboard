<template>
  <v-container v-if="$store.state.portal.accounts.length === 0">
    <v-card>
      <WelcomeWindow />
    </v-card>
  </v-container>

  <div
    style="padding-top:100ox"
    v-else-if="!editingTwin"
  >
    <v-container>
      <v-card
        color="#388E3C"
        class="my-3 pa-3 text-center"
      >
        <h2> Congratulations {{$route.query.accountName}}! <br />
          You can now interact with the TF Grid</h2>

      </v-card>
      <v-card
        color="#512DA8"
        class="my-3 pa-3 text-center"
      >
        <h3>Twin Details</h3>

        <v-list>
          <v-list-item>
            ID: {{$route.query.twinID}}
          </v-list-item>
          <v-list-item>
            IP: {{$route.query.twinIP}}
          </v-list-item>
          <v-list-item>
            ADDRESS: {{$route.params.accountID}}
          </v-list-item>
        </v-list>
        <v-card-actions>
          <v-btn
            @click="editTwin"
            color="#388E3C"
          >Edit</v-btn>
          <v-btn
            @click="deleteTwin"
            color="red"
          >Delete</v-btn>
        </v-card-actions>

      </v-card>
      <FundsCard />
    </v-container>
  </div>
  <v-container v-else>
    <EditTwinPopUp />
  </v-container>
</template>

<script lang="ts">
import FundsCard from "@/components/FundsCard.vue";
import WelcomeWindow from "@/components/WelcomeWindow.vue";
import { Component, Vue } from "vue-property-decorator";
import EditTwinPopUp from "../../components/EditTwinPopUp.vue";

@Component({
  name: "Twin",
  components: { WelcomeWindow, EditTwinPopUp, FundsCard },
})
export default class TwinView extends Vue {
  $api: any;
  editingTwin = false;
  mounted() {
    console.log(this.$api);
  }
  public editTwin() {
    console.log("editing a twin");
    this.editingTwin = true;
  }
  public deleteTwin() {
    console.log("deleting a twin");
  }
}
</script>