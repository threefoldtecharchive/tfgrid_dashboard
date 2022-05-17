import Vue from "vue";
import VueApollo from "vue-apollo";

import dateFiler from "./filters/date";
import optionTitleFiler from "./filters/optionTitle";
import toTeraOrGigaOrPeta from "./filters/toTeraOrGigaOrPeta";
import secondToRedable from "./filters/secondToRedable";
import apolloProvider from "./filters/optionTitle";

Vue.use(VueApollo);
Vue.filter("date", dateFiler);
Vue.filter("optionTitle", optionTitleFiler);
Vue.filter("toTeraOrGigaOrPeta", toTeraOrGigaOrPeta);
Vue.filter("secondToRedable", secondToRedable);

export const explorerConfigs: any = {
  apolloProvider,
};
