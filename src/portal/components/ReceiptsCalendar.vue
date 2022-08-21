<template >

  <v-container>
    <v-row class="fill-height">
      <v-col>
        <v-sheet height="64">
          <v-toolbar flat>

            <v-btn
              outlined
              @click="setToday"
            >Today</v-btn>
            <v-btn
              fab
              text
              small
              @click="prev"
            >
              <v-icon small>
                mdi-chevron-left
              </v-icon>
            </v-btn>

            <v-toolbar-title v-if="$refs.calendar">
              {{ $refs.calendar.title }}
            </v-toolbar-title>
            <v-btn
              fab
              text
              small
              color="grey darken-2"
              @click="next"
            >
              <v-icon small>
                mdi-chevron-right
              </v-icon>
            </v-btn>
            <v-btn
              class="ml-auto"
              @click="downloadReceipts()"
            >Download Receipts</v-btn>

          </v-toolbar>
        </v-sheet>
        <v-sheet height="600">
          <v-calendar
            ref="calendar"
            v-model="focus"
            :type='type'
            :events="getEvents()"
            @click:event="showEvent"
          ></v-calendar>
        </v-sheet>
      </v-col>
    </v-row>
    <v-dialog
      v-model="selectedOpen"
      max-width="600"
    >
      <v-card>
        <v-card-title>
          {{selectedEvent.name}}

        </v-card-title>
        <v-card-subtitle> {{selectedEvent.hash}}</v-card-subtitle>
        <v-card-text>
          <p> <b>Start:</b>
            {{selectedEvent.start}}</p>
          <p> <b> End:</b>
            {{selectedEvent.end}}</p>

        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>
<script lang="ts">
import { VueConstructor } from "vue";
import { Component, Vue, Prop, Ref, Watch } from "vue-property-decorator";
import { receiptInterface } from "../lib/nodes";
import { jsPDF } from "jspdf";

interface eventInterface {
  start: Date;
  end: Date;
  name: string;
  color: string;
  hash: string;
}
@Component({
  name: "ReceiptsCalendar",
})
export default class ReceiptsCalendar extends Vue {
  $refs!: {
    calendar: any;
  };
  @Ref() calendar!:
    | Vue
    | VueConstructor<Vue>
    | Element
    | (Vue | Element)[]
    | undefined;

  @Prop({ required: true }) receipts!: receiptInterface[];

  focus = "";
  type = "month";
  selectedElement = null;
  selectedOpen = false;

  selectedEvent: eventInterface = {
    name: "",
    start: new Date(),
    end: new Date(),
    hash: "",
    color: "",
  };

  @Watch("receipts") async onPropertyChanged() {
    this.getEvents();
  }
  downloadReceipts() {
    let doc = new jsPDF();
    doc.setFontSize(15);

    let topY = 20;
    const lineOffset = 5;
    const cellOffset = 30;
    let cellX = 15;
    let cellY = topY + lineOffset * 6;

    doc.text("Node Receipts Summary", 80, topY);
    doc.setFontSize(10);
    doc.text(
      `Receipts total: ${this.receipts.length}`,
      cellX,
      topY + lineOffset
    );
    doc.text(
      `Minting total: ${
        this.receipts.filter((receipt) => receipt.measuredUptime).length
      }`,
      cellX,
      topY + lineOffset * 2
    );
    doc.text(
      `Fixup total: ${
        this.receipts.filter((receipt) => receipt.fixupStart).length
      }`,
      cellX,
      topY + lineOffset * 3
    );

    doc.text(
      `TFT total(M): ${this.receipts
        .reduce((total, receipt) => (total += receipt.tft || 0), 0)
        .toFixed(2)}`,
      cellX,
      topY + lineOffset * 4
    );
    doc.line(cellX, topY + lineOffset * 5, cellX + 175, topY + lineOffset * 5);

    this.receipts.map((receipt, i) => {
      if (receipt.measuredUptime) {
        doc.text(`Minting: ${receipt.hash}`, cellX, cellY + cellOffset * i);
        doc.text(
          `start: ${this.getTime(receipt.mintingStart)}`,
          cellX,
          cellY + cellOffset * i + lineOffset
        );
        doc.text(
          `end: ${this.getTime(receipt.mintingEnd)}`,
          cellX,
          cellY + cellOffset * i + lineOffset * 2
        );
        doc.text(
          `TFT(M): ${receipt.tft?.toFixed(2)}`,
          cellX,
          cellY + cellOffset * i + lineOffset * 3
        );
        doc.line(
          cellX,
          cellY + cellOffset * i + lineOffset * 4,
          cellX + 175,
          cellY + cellOffset * i + lineOffset * 4
        );
      } else {
        doc.text(`Fixup: ${receipt.hash}`, cellX, cellY + cellOffset * i);
        doc.text(
          `start: ${this.getTime(receipt.fixupStart)}`,
          cellX,
          cellY + cellOffset * i + lineOffset
        );
        doc.text(
          `end: ${this.getTime(receipt.fixupEnd)}`,
          cellX,
          cellY + cellOffset * i + lineOffset * 2
        );
        doc.line(
          cellX,
          cellY + cellOffset * i + lineOffset * 4,
          cellX + 175,
          cellY + cellOffset * i + lineOffset * 4
        );
      }
    });

    doc.save("receipt.pdf");
  }
  getEvents() {
    let events: eventInterface[] = [];
    this.receipts.map((rec: receiptInterface) => {
      if (rec.measuredUptime) {
        events.push({
          name: `Minting`,
          start: this.getTime(rec.mintingStart),
          end: this.getTime(rec.mintingEnd),
          color: "green",
          hash: rec.hash,
        });
      } else {
        events.push({
          name: "Fixup",
          start: this.getTime(rec.fixupStart),
          end: this.getTime(rec.fixupEnd),
          color: "red",
          hash: rec.hash,
        });
      }
    });
    return events;
  }
  unmounted() {
    this.receipts = [];
  }
  mounted() {
    this.$refs.calendar.checkChange(); //.checkChange();
  }

  showEvent(event: { event: eventInterface }) {
    this.selectedEvent = event.event;
    this.selectedOpen = true;
  }
  setToday() {
    this.focus = "";
  }
  prev() {
    this.$refs.calendar.prev();
  }
  next() {
    this.$refs.calendar.next();
  }

  getTime(num: number | undefined) {
    if (num) {
      return new Date(num);
    }
    return new Date();
  }
}
</script>
