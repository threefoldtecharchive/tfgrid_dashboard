<template>
  <div class="container">
    <v-btn
      small
      outlined
      :loading="loading"
      color="#064663"
      v-if="status === 'free'"
      @click="reserveNode(nodeId)"
    >
      Reserve
    </v-btn>
    <v-btn
      small
      outlined
      color="red"
      :loading="loading"
      v-if="status === 'yours'"
      @click="unReserveNode(nodeId)"
    >
      Unreserve
    </v-btn>
    <v-btn
      small
      outlined
      disabled
      color="gray"
      v-if="status === 'taken'"
    >
      Taken
    </v-btn>
  </div>
</template>
<script lang="ts">
import {
  cancelRentContract,
  createRentContract,
  getActiveContracts,
  getRentContractID,
  getRentStatus,
} from "@/portal/lib/nodes";
import { getTwinID } from "@/portal/lib/twin";
import { Component, Prop, Vue } from "vue-property-decorator";

@Component({
  name: "NodeActionBtn",
})
export default class NodeActionBtn extends Vue {
  status = "free";
  loading = false;
  @Prop({ required: true })
  nodeId!: string;
  $api: any;
  async created() {
    this.status = await this.getStatus();
  }
  async getStatus() {
    const currentTwinID = await getTwinID(
      this.$api,
      this.$route.params.accountID
    );
    return await getRentStatus(this.$api, this.nodeId, currentTwinID);
  }
  reserveNode(nodeId: any) {
    this.loading = true;
    console.log(`reserving node ${nodeId}`);
    createRentContract(
      this.$api,
      this.$route.params.accountID,
      nodeId,
      (res: { status: { type: any } }) => {
        console.log(res);
        switch (res.status.type) {
          case "Ready":
            this.$toasted.show(
              `Transaction submitted: Reserving node ${nodeId}`
            );
            break;
          case "Finalized":
            this.$toasted.show(
              `Transaction successed: Node ${nodeId} reserved`
            );
            this.getStatus().then((status) => {
              this.status = status;
              this.loading = false;
            });
            break;
        }
      }
    ).catch((err: { message: any }) => {
      console.log(err.message);
      console.log(`Error:  ${err.message}`, {
        type: "error",
      });
      this.loading = false;
    });
  }

  async unReserveNode(nodeId: any) {
    this.loading = true;
    this.$toasted.show(`check for contracts on node ${nodeId}`);

    const contracts = await getActiveContracts(this.$api, nodeId);
    if (contracts.length > 0) {
      this.$toasted.show(
        `node ${nodeId} has ${contracts.length} active contracts`
      );
      this.loading = false;
    } else {
      this.$toasted.show(`unreserving node ${nodeId}`);
      const rentContractID = await getRentContractID(this.$api, nodeId);
      cancelRentContract(
        this.$api,
        this.$route.params.accountID,
        rentContractID,
        (res: { status: { type: any } }) => {
          console.log(res);
          switch (res.status.type) {
            case "Ready":
              this.$toasted.show(
                `Transaction submitted: Unreserving node ${nodeId}`
              );
              break;
            case "Finalized":
              this.$toasted.show(
                `Transaction successed: Node ${nodeId} Unreserved`
              );
              this.getStatus().then((status) => {
                this.status = status;
                this.loading = false;
              });
              break;
          }
        }
      ).catch((err: { message: any }) => {
        console.log(err.message);
        this.$toasted.show(`Error:  ${err.message}`, {
          type: "error",
        });
        this.loading = false;
      });
    }
  }
}
</script>
