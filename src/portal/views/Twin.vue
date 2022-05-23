<template>

  <v-container v-if="$store.state.portal.accounts.length === 0">
    <v-card>
      <WelcomeWindow />
    </v-card>
  </v-container>

  <div
    style="padding-top:100ox"
    v-else
  >
    <v-container v-if="editingTwin">
      <v-dialog
        transition="dialog-bottom-transition"
        max-width="600"
        v-model="editingTwin"
      >

        <v-card>
          <v-toolbar
            color="primary"
            dark
          >Edit Twin</v-toolbar>
          <v-card-text>
            <div class="text-h2 pa-12">
              <v-text-field
                v-model="ip"
                label="Twin IP ::1"
              ></v-text-field>
            </div>
          </v-card-text>
          <v-card-actions class="justify-end">
            <v-btn
              @click="editingTwin = false"
              text
            >Close</v-btn>
            <v-btn @click="updateTwin">Submit</v-btn>
          </v-card-actions>
        </v-card>

      </v-dialog>
    </v-container>
    <v-container>
      <v-card
        color="#388E3C"
        class="my-3 pa-3 text-center"
      >
        <h2> Congratulations {{$route.query.accountName}} on creating a twin! <br />
          You can now interact with the TF Grid</h2>

      </v-card>
      <v-card
        color="#512DA8"
        class="my-3 pa-3 text-center"
      >
        <h3>Twin Details</h3>

        <v-list>
          <v-list-item>
            ID: {{id}}
          </v-list-item>

          <v-list-item>
            IP: {{ip}}
          </v-list-item>

          <v-list-item>
            ADDRESS: {{address}}
          </v-list-item>
        </v-list>
        <v-card-actions class="justify-end">
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
      <FundsCard :balance="balance" />
    </v-container>
  </div>

</template>

<script lang="ts">
import FundsCard from "@/components/FundsCard.vue";
import WelcomeWindow from "@/components/WelcomeWindow.vue";
import { Component, Vue } from "vue-property-decorator";
import EditTwinPopUp from "../../components/EditTwinPopUp.vue";
import { getBalance } from "../lib/balance";
import { getTwin, getTwinID, updateTwinIP } from "../lib/twin";

@Component({
  name: "Twin",
  components: { WelcomeWindow, EditTwinPopUp, FundsCard },
})
export default class TwinView extends Vue {
  $api: any;
  editingTwin = false;
  ip: any = [];
  id: any = [];
  address = "";
  twin: any;
  accountName: any;
  balance: any = 0;
  async updated() {
    this.address = this.$route.params.accountID;
    if (this.$route.query.twinIP && this.$route.query.twinID) {
      this.ip = this.$route.query.twinIP;
      this.id = this.$route.query.twinID;
      this.accountName = this.$route.query.accountName;
    }
    this.balance = (await getBalance(this.$api, this.address)) / 1e7;
  }
  async mounted() {
    this.address = this.$route.params.accountID;
    if (this.$route.query.twinIP && this.$route.query.twinID) {
      this.ip = this.$route.query.twinIP;
      this.id = this.$route.query.twinID;
      this.accountName = this.$route.query.accountName;
    }
    this.balance = this.$route.query.balance;
  }

  public editTwin() {
    console.log("editing a twin");
    this.editingTwin = true;
  }
  public updateTwin() {
    console.log(this.ip);
    updateTwinIP(
      this.$route.params.accountID,
      this.$api,
      this.ip,
      (res: { events?: never[] | undefined; status: any }) => {
        if (res instanceof Error) {
          console.log(res);
          return;
        }

        const { events = [], status } = res;
        console.log(`Current status is ${status.type}`);
        switch (status.type) {
          case "Ready":
            console.log(`Transaction submitted`);
        }

        if (status.isFinalized) {
          console.log(
            `Transaction included at blockHash ${status.asFinalized}`
          );

          // Loop through Vec<EventRecord> to display all events
          events.forEach(
            async ({ phase, event: { data, method, section } }) => {
              console.log(`\t' ${phase}: ${section}.${method}:: ${data}`);
              if (section === "tfgridModule" && method === "TwinUpdated") {
                console.log("Twin updated!");
                const twinStoredEvent = data[0];
                console.log(twinStoredEvent);
                this.id = await getTwinID(
                  this.$api,
                  this.$route.params.accountID
                );
                this.twin = await getTwin(this.$api, this.id);
                this.ip = this.twin.ip;
                this.editingTwin = false;
              } else if (section === "system" && method === "ExtrinsicFailed") {
                console.log("Twin creation failed!");
              }
            }
          );
        }
      }
    );
  }
  public deleteTwin() {
    console.log("deleting a twin");
  }
}
</script>