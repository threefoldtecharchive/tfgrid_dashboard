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

          </v-toolbar>
        </v-sheet>
        <v-sheet height="600">
          <v-calendar
            ref="calendar"
            v-model="focus"
            :type='type'
            :events="events"
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
          <!-- <p><b>Period(Days):</b>{{getPeriod(selectedEvent.start, selectedEvent.end)}}</p> -->

        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>
<script lang="ts">
import moment from "moment";
import { VueConstructor } from "vue";
import { Component, Vue, Prop, Ref } from "vue-property-decorator";
import { receiptInterface } from "../lib/nodes";
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
  events: eventInterface[] = [];

  selectedEvent: eventInterface = {
    name: "",
    start: new Date(),
    end: new Date(),
    hash: "",
    color: "",
  };

  mounted() {
    this.$refs.calendar.checkChange(); //.checkChange();
    this.receipts.map((rec: receiptInterface) => {
      if (rec.measuredUptime) {
        this.events.push({
          name: `Minting`,
          start: this.getTime(rec.mintingStart),
          end: this.getTime(rec.mintingEnd),
          color: "green",
          hash: rec.hash,
        });
      } else {
        this.events.push({
          name: "Fixup",
          start: this.getTime(rec.fixupStart),
          end: this.getTime(rec.fixupEnd),
          color: "red",
          hash: rec.hash,
        });
      }
    });
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
  getPeriod(start: Date, end: Date) {
    return moment(end.getMilliseconds() - start.getMilliseconds()).format("DD");
  }
  getTime(num: number | undefined) {
    if (num) {
      return new Date(num);
    }
    return new Date();
  }
}
</script>
